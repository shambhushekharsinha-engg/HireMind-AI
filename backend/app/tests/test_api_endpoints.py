import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_and_metrics_endpoints():
    h_res = client.get("/health")
    assert h_res.status_code == 200
    assert h_res.json()["status"] == "healthy"

    m_res = client.get("/metrics")
    assert m_res.status_code == 200
    assert "hiremind_api_requests_total" in m_res.text

def test_job_match_api():
    res = client.post("/api/v1/jobs/match", json={
        "resume_text": "Experienced Python Software Engineer proficient in FastAPI, SQL, and Docker.",
        "job_description": "We need a Python developer who knows FastAPI and Docker.",
        "job_title": "Backend Software Engineer"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["match_score"] > 50.0

def test_applications_tracker_api():
    create_res = client.post("/api/v1/applications", json={
        "company": "Google",
        "position": "Staff AI Engineer",
        "status": "Applied",
        "salary_range": "$200,000 - $250,000"
    })
    assert create_res.status_code == 200
    app_id = create_res.json()["id"]

    get_res = client.get("/api/v1/applications")
    assert get_res.status_code == 200
    assert any(a["id"] == app_id for a in get_res.json())

    patch_res = client.patch(f"/api/v1/applications/{app_id}", json={"status": "Interviewing"})
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "Interviewing"

    del_res = client.delete(f"/api/v1/applications/{app_id}")
    assert del_res.status_code == 200
