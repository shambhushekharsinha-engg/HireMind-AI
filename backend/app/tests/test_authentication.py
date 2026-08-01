import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login_flow():
    # Test Registration
    email = f"test_user_{pytest.__name__}@hiremind.ai"
    reg_res = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "Password123!",
        "full_name": "Test User",
        "role": "student"
    })
    assert reg_res.status_code == 200
    data = reg_res.json()
    assert data["email"] == email

    # Test Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    assert "refresh_token" in token_data

def test_login_invalid_credentials():
    res = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@hiremind.ai",
        "password": "WrongPassword"
    })
    assert res.status_code == 401

def test_otp_generation_and_verification():
    otp_req = client.post("/api/v1/auth/generate-otp", json={"email": "otpuser@hiremind.ai"})
    assert otp_req.status_code == 200
    assert otp_req.json()["demo_otp"] == "123456"

    verify_req = client.post("/api/v1/auth/verify-otp", json={
        "email": "otpuser@hiremind.ai",
        "otp_code": "123456"
    })
    assert verify_req.status_code == 200
    assert "access_token" in verify_req.json()

def test_forgot_and_reset_password():
    forgot_res = client.post("/api/v1/auth/forgot-password", json={"email": "alex.student@hiremind.ai"})
    assert forgot_res.status_code == 200
    reset_token = forgot_res.json().get("reset_token")

    if reset_token:
        reset_res = client.post("/api/v1/auth/reset-password", json={
            "email": "alex.student@hiremind.ai",
            "reset_token": reset_token,
            "new_password": "NewSecurePassword123!"
        })
        assert reset_res.status_code == 200

def test_demo_login_endpoint():
    res = client.post("/api/v1/auth/demo-login?role=recruiter")
    assert res.status_code == 200
    assert res.json()["user"]["role"] == "recruiter"
