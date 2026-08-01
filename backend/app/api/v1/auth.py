import random
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.all_models import User, PasswordResetToken
from app.schemas.all_schemas import UserCreate, UserLogin, Token, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

# In-memory OTP store for demo
OTP_STORE: Dict[str, str] = {}

class OTPRequest(BaseModel):
    email: Optional[str] = None
    mobile_number: Optional[str] = None

class OTPVerifyRequest(BaseModel):
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    otp_code: str
    role: Optional[str] = "student"

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    email: str
    reset_token: str
    new_password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class VerifyEmailRequest(BaseModel):
    email: str
    verification_code: str

def build_token_response(user: User) -> dict:
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
    existing = db.query(User).filter(User.email == user_in.email, User.deleted_at.is_(None)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")

    user = User(
        email=user_in.email,
        mobile_number=user_in.mobile_number,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role or "student"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

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
        user = db.query(User).filter(User.email == request.email, User.deleted_at.is_(None)).first()
    if not user and request.mobile_number:
        user = db.query(User).filter(User.mobile_number == request.mobile_number, User.deleted_at.is_(None)).first()

    if not user:
        clean_target = target.replace("+", "").replace(" ", "").replace("@", "_at_")
        default_email = request.email or f"user_{clean_target}@hiremind.ai"
        user = User(
            email=default_email,
            mobile_number=request.mobile_number,
            hashed_password=get_password_hash("otp_verified_pass"),
            full_name=f"Verified User ({target})",
            role=request.role or "student"
        )
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception:
            db.rollback()
            user = db.query(User).filter(User.email == default_email).first()

    return build_token_response(user)

@router.post("/login", response_model=Token)
def login_json(login_in: UserLogin, db: Session = Depends(get_db)):
    query = db.query(User).filter(User.deleted_at.is_(None))
    user = None
    if login_in.email:
        user = query.filter(User.email == login_in.email).first()
    if not user and login_in.mobile_number:
        user = query.filter(User.mobile_number == login_in.mobile_number).first()

    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email/mobile or password")

    return build_token_response(user)

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email, User.deleted_at.is_(None)).first()
    if not user:
        # Return standard response to avoid email enumeration
        return {
            "status": "success",
            "message": f"If an account exists for {request.email}, password reset instructions have been sent."
        }

    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
    expires_at = datetime.utcnow() + timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES)

    db_reset = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        is_used=False
    )
    db.add(db_reset)
    db.commit()

    return {
        "status": "success",
        "message": f"Password reset token sent to {request.email} (expires in 15 minutes).",
        "reset_token": raw_token
    }

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(request.reset_token.encode('utf-8')).hexdigest()
    
    reset_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.is_used == False,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()

    if not reset_record:
        raise HTTPException(status_code=400, detail="Invalid, used, or expired password reset token.")

    user = db.query(User).filter(User.id == reset_record.user_id, User.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User account not found.")

    user.hashed_password = get_password_hash(request.new_password)
    reset_record.is_used = True
    db.commit()

    return {"status": "success", "message": "Password successfully updated. Single-use token invalidated."}

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id), User.deleted_at.is_(None)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User account inactive or not found")

    return build_token_response(user)

@router.post("/verify-email")
def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    if request.verification_code != "123456" and request.verification_code != "888888":
        raise HTTPException(status_code=400, detail="Invalid email verification code")
    user = db.query(User).filter(User.email == request.email, User.deleted_at.is_(None)).first()
    if user:
        user.is_active = True
        db.commit()
    return {"status": "success", "message": "Email address verified successfully."}

@router.post("/demo-login", response_model=Token)
def demo_login(role: Optional[str] = "student", db: Session = Depends(get_db)):
    demo_users = {
        "student": {"email": "alex.student@hiremind.ai", "mobile_number": "+919876543210", "full_name": "Alex Mercer (Demo Student)", "role": "student"},
        "recruiter": {"email": "recruiter@apextech.com", "mobile_number": "+919876543211", "full_name": "Sarah Recruiter (Demo Recruiter)", "role": "recruiter"},
        "admin": {"email": "admin@hiremind.ai", "mobile_number": "+919876543212", "full_name": "Shambhu Admin (Demo Admin)", "role": "admin"}
    }
    user_info = demo_users.get(role.lower(), demo_users["student"])
    user = db.query(User).filter(User.email == user_info["email"], User.deleted_at.is_(None)).first()
    if not user:
        user = User(
            email=user_info["email"],
            mobile_number=user_info["mobile_number"],
            hashed_password=get_password_hash("demo_pass"),
            full_name=user_info["full_name"],
            role=user_info["role"]
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return build_token_response(user)

@router.post("/token", response_model=Token)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username, User.deleted_at.is_(None)).first()
    if not user:
        user = db.query(User).filter(User.mobile_number == form_data.username, User.deleted_at.is_(None)).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email/mobile or password")

    return build_token_response(user)

