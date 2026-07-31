from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.all_models import User
from app.schemas.all_schemas import UserCreate, UserLogin, Token, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

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

@router.post("/login", response_model=Token)
def login_json(login_in: UserLogin, db: Session = Depends(get_db)):
    query = db.query(User)
    if login_in.email:
        user = query.filter(User.email == login_in.email).first()
    elif login_in.mobile_number:
        user = query.filter(User.mobile_number == login_in.mobile_number).first()
    else:
        raise HTTPException(status_code=400, detail="Please provide email or mobile_number")

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
