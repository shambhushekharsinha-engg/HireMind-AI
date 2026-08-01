import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_security_headers_present():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert "Content-Security-Policy" in response.headers

def test_request_id_tracing():
    response = client.get("/health")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time-Sec" in response.headers

def test_cors_preflight_request():
    response = client.options("/api/v1/auth/login", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST"
    })
    assert response.status_code in [200, 204]

def test_feature_flags_status():
    from app.core.feature_flags import feature_flags
    all_flags = feature_flags.get_all()
    assert "ENABLE_EXPERIMENTAL_AI" in all_flags
    assert "ENABLE_FAISS_VECTOR_SEARCH" in all_flags
