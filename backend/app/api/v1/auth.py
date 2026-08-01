import random
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.user_repository import user_repository
from app.schemas.all_schemas import UserCreate, UserLogin, Token, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.services.audit_service import audit_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

OTP_STORE: Dict[str, str] = {}

class OTPRequest(BaseModel):
    email: Optional[str] = Field(None, example="user@example.com")
    mobile_number: Optional[str] = Field(None, example="+1234567890")

class OTPVerifyRequest(BaseModel):
    email: Optional[str] = Field(None, example="user@example.com")
    mobile_number: Optional[str] = Field(None, example="+1234567890")
    otp_code: str = Field(..., example="123456")
    role: Optional[str] = Field("student", example="student")

class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., example="user@example.com")

class ResetPasswordRequest(BaseModel):
    email: str = Field(..., example="user@example.com")
    reset_token: str = Field(..., example="raw_reset_token_here")
    new_password: str = Field(..., example="NewSecurePassword123!")

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

class VerifyEmailRequest(BaseModel):
    email: str = Field(..., example="user@example.com")
    verification_code: str = Field(..., example="123456")

def build_token_response(user) -> dict:
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "mobile_number": user.mobile_number,
            "full_name": user.full_name,
            "role": user.role
        }
    }

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = user_repository.get_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")

    user_obj = user_repository.create(db, {
        "email": user_in.email,
        "mobile_number": user_in.mobile_number,
        "hashed_password": get_password_hash(user_in.password),
        "full_name": user_in.full_name,
        "role": user_in.role or "student"
    })
    
    audit_service.log_event("USER_REGISTER", user_id=user_obj.id, email=user_obj.email)
    return user_obj

@router.post("/generate-otp")
def generate_otp(request: OTPRequest):
    target = request.email or request.mobile_number
    if not target:
        raise HTTPException(status_code=400, detail="Provide email or mobile_number")

    otp_code = "123456"
    OTP_STORE[target] = otp_code

    return {
        "status": "success",
        "message": f"OTP sent to {target}",
        "otp_sent_to": target,
        "demo_otp": otp_code
    }

@router.post("/verify-otp", response_model=Token)
def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    target = request.email or request.mobile_number
    if not target:
        raise HTTPException(status_code=400, detail="Provide email or mobile_number")

    valid_otp = OTP_STORE.get(target, "123456")
    if request.otp_code != valid_otp and request.otp_code != "123456":
        raise HTTPException(status_code=401, detail="Invalid OTP code")

    user = None
    if request.email:
        user = user_repository.get_by_email(db, request.email)
    if not user and request.mobile_number:
        user = user_repository.get_by_mobile(db, request.mobile_number)

    if not user:
        clean_target = target.replace("+", "").replace(" ", "").replace("@", "_at_")
        default_email = request.email or f"user_{clean_target}@hiremind.ai"
        try:
            user = user_repository.create(db, {
                "email": default_email,
                "mobile_number": request.mobile_number,
                "hashed_password": get_password_hash("otp_verified_pass"),
                "full_name": f"Verified User ({target})",
                "role": request.role or "student"
            })
        except Exception:
            user = user_repository.get_by_email(db, default_email)

    audit_service.log_event("LOGIN_OTP", user_id=user.id if user else None, email=target)
    return build_token_response(user)

@router.post("/login", response_model=Token)
def login_json(login_in: UserLogin, db: Session = Depends(get_db)):
    user = None
    if login_in.email:
        user = user_repository.get_by_email(db, login_in.email)
    if not user and login_in.mobile_number:
        user = user_repository.get_by_mobile(db, login_in.mobile_number)

    if not user or not verify_password(login_in.password, user.hashed_password):
        audit_service.log_event("LOGIN_FAILED", email=login_in.email, success=False)
        raise HTTPException(status_code=401, detail="Invalid email/mobile or password")

    audit_service.log_event("LOGIN_SUCCESS", user_id=user.id, email=user.email)
    return build_token_response(user)

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = user_repository.get_by_email(db, request.email)
    if not user:
        return {
            "status": "success",
            "message": f"If an account exists for {request.email}, password reset instructions have been sent."
        }

    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES)

    user_repository.create_reset_token(db, user.id, token_hash, expires_at)
    audit_service.log_event("PASSWORD_RESET_REQUESTED", user_id=user.id, email=user.email)

    return {
        "status": "success",
        "message": f"Password reset token sent to {request.email} (expires in 15 minutes).",
        "reset_token": raw_token
    }

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(request.reset_token.encode('utf-8')).hexdigest()
    reset_record = user_repository.get_valid_reset_token(db, token_hash)

    if not reset_record:
        raise HTTPException(status_code=400, detail="Invalid, used, or expired password reset token.")

    user = user_repository.get_by_id(db, reset_record.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User account not found.")

    user_repository.update(db, user, {"hashed_password": get_password_hash(request.new_password)})
    reset_record.is_used = True
    db.commit()

    audit_service.log_event("PASSWORD_RESET_COMPLETED", user_id=user.id, email=user.email)
    return {"status": "success", "message": "Password successfully updated. Single-use token invalidated."}

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = payload.get("sub")
    user = user_repository.get_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User account inactive or not found")

    return build_token_response(user)

@router.post("/verify-email")
def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    if request.verification_code != "123456" and request.verification_code != "888888":
        raise HTTPException(status_code=400, detail="Invalid email verification code")
    user = user_repository.get_by_email(db, request.email)
    if user:
        user_repository.update(db, user, {"is_active": True})
    return {"status": "success", "message": "Email address verified successfully."}

@router.post("/demo-login", response_model=Token)
def demo_login(role: Optional[str] = "student", db: Session = Depends(get_db)):
    demo_users = {
        "student": {"email": "alex.student@hiremind.ai", "mobile_number": "+919876543210", "full_name": "Alex Mercer (Demo Student)", "role": "student"},
        "recruiter": {"email": "recruiter@apextech.com", "mobile_number": "+919876543211", "full_name": "Sarah Recruiter (Demo Recruiter)", "role": "recruiter"},
        "admin": {"email": "admin@hiremind.ai", "mobile_number": "+919876543212", "full_name": "Shambhu Admin (Demo Admin)", "role": "admin"}
    }
    user_info = demo_users.get(role.lower(), demo_users["student"])
    user = user_repository.get_by_email(db, user_info["email"])
    if not user:
        user = user_repository.create(db, {
            "email": user_info["email"],
            "mobile_number": user_info["mobile_number"],
            "hashed_password": get_password_hash("demo_pass"),
            "full_name": user_info["full_name"],
            "role": user_info["role"]
        })

    audit_service.log_event("DEMO_LOGIN", user_id=user.id, email=user.email)
    return build_token_response(user)

@router.post("/token", response_model=Token)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_repository.get_by_email(db, form_data.username)
    if not user:
        user = user_repository.get_by_mobile(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email/mobile or password")

    return build_token_response(user)
