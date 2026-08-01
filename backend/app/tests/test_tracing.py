import time

from app.core.tracing import get_tracer


def test_request_tracer_spans():
    tracer = get_tracer("test-trace-123")
    assert tracer.trace_id == "test-trace-123"

    tracer.start_span("Upload")
    time.sleep(0.01)
    duration = tracer.end_span("Upload")
    assert duration > 0.0

    summary = tracer.get_summary()
    assert "Upload" in summary["spans"]
    assert summary["trace_id"] == "test-trace-123"
