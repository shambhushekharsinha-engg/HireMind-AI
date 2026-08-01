from app.core.error_codes import ErrorCode
from app.core.event_dispatcher import DomainEvent, ResumeUploadedEvent, event_dispatcher
from app.core.startup_check import StartupValidator
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_startup_validator():
    assert StartupValidator.validate_all() is True


def test_operational_health_dashboard_api():
    res = client.get("/health/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert data["overall_system_status"] in ["healthy", "degraded"]
    assert "components" in data
    assert "database" in data["components"]
    assert "faiss_vector_store" in data["components"]


def test_internal_event_dispatcher():
    received = []

    def handle_resume_uploaded(event: DomainEvent):
        received.append(event.payload["filename"])

    event_dispatcher.subscribe("ResumeUploadedEvent", handle_resume_uploaded)
    event_dispatcher.publish(ResumeUploadedEvent(resume_id=101, filename="test_resume.pdf"))

    assert len(received) == 1
    assert received[0] == "test_resume.pdf"


def test_error_code_formatting():
    formatted = ErrorCode.format_error(ErrorCode.HM1001, request_id="req-test-1")
    assert formatted["code"] == "HM1001"
    assert "Resume text parsing failed" in formatted["message"]
    assert formatted["request_id"] == "req-test-1"
