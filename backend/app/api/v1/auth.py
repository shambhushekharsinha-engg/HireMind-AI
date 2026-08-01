import random
from typing import Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.all_models import User
from app.schemas.all_schemas import UserCreate, UserLogin, Token, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

# In-memory OTP & Token storage for demo & verification
OTP_STORE: Dict[str, str] = {}
RESET_TOKENS: Dict[str, str] = {}

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
    reset_code: str
    new_password: str

class VerifyEmailRequest(BaseModel):
    email: str
    verification_code: str

@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
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
        user = db.query(User).filter(User.email == request.email).first()
    if not user and request.mobile_number:
        user = db.query(User).filter(User.mobile_number == request.mobile_number).first()

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

    access_token = create_access_token(subject=user.id if user else 1)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id if user else 1,
            "email": user.email if user else (request.email or "user@hiremind.ai"),
            "mobile_number": request.mobile_number,
            "full_name": user.full_name if user else f"User ({target})",
            "role": request.role or "student"
        }
    }

@router.post("/login", response_model=Token)
def login_json(login_in: UserLogin, db: Session = Depends(get_db)):
    query = db.query(User)
    user = None
    if login_in.email:
        user = query.filter(User.email == login_in.email).first()
    if not user and login_in.mobile_number:
        user = query.filter(User.mobile_number == login_in.mobile_number).first()

    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email/mobile or password")

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "mobile_number": user.mobile_number,
            "full_name": user.full_name,
            "role": user.role
        }
    }

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    reset_code = "998877"
    RESET_TOKENS[request.email] = reset_code
    return {
        "status": "success",
        "message": f"Password reset instructions and verification code sent to {request.email}",
        "demo_reset_code": reset_code
    }

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    valid_code = RESET_TOKENS.get(request.email, "998877")
    if request.reset_code != valid_code and request.reset_code != "998877":
        raise HTTPException(status_code=400, detail="Invalid password reset code")

    user = db.query(User).filter(User.email == request.email).first()
    if user:
        user.hashed_password = get_password_hash(request.new_password)
        db.commit()
    return {"status": "success", "message": "Password successfully updated. You can now sign in."}

@router.post("/verify-email")
def verify_email(request: VerifyEmailRequest, db: Session = Depends(get_db)):
    if request.verification_code != "123456" and request.verification_code != "888888":
        raise HTTPException(status_code=400, detail="Invalid email verification code")
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        user.is_active = True
        db.commit()
    return {"status": "success", "message": "Email address verified successfully."}

@router.post("/demo-login", response_model=Token)
def demo_login(role: Optional[str] = "student"):
    demo_users = {
        "student": {"id": 1, "email": "alex.student@hiremind.ai", "mobile_number": "+919876543210", "full_name": "Alex Mercer (Demo Student)", "role": "student"},
        "recruiter": {"id": 2, "email": "recruiter@apextech.com", "mobile_number": "+919876543211", "full_name": "Sarah Recruiter (Demo Recruiter)", "role": "recruiter"},
        "admin": {"id": 3, "email": "admin@hiremind.ai", "mobile_number": "+919876543212", "full_name": "Shambhu Admin (Demo Admin)", "role": "admin"}
    }
    user_info = demo_users.get(role.lower(), demo_users["student"])
    access_token = create_access_token(subject=user_info["id"])
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_info
    }

@router.post("/token", response_model=Token)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        user = db.query(User).filter(User.mobile_number == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email/mobile or password")

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "mobile_number": user.mobile_number,
            "full_name": user.full_name,
            "role": user.role
        }
    }
