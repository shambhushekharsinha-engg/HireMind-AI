import time
import uuid
from typing import Any, Dict


class Span:
    def __init__(self, name: str):
        self.name = name
        self.start_time = time.time()
        self.end_time = None
        self.duration_ms = None

    def finish(self):
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)
        return self.duration_ms


class RequestTracer:
    """
    End-to-End Distributed Request Tracer.
    Tracks lifecycle spans: Request -> Upload -> Parser -> ATS -> Embeddings -> Coach -> Report -> Response.
    """

    def __init__(self, trace_id: str = None):
        self.trace_id = trace_id or f"tr-{uuid.uuid4().hex[:12]}"
        self.spans: Dict[str, Span] = {}

    def start_span(self, span_name: str) -> Span:
        span = Span(span_name)
        self.spans[span_name] = span
        return span

    def end_span(self, span_name: str) -> float:
        if span_name in self.spans:
            return self.spans[span_name].finish()
        return 0.0

    def get_summary(self) -> Dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "spans": {name: span.duration_ms for name, span in self.spans.items() if span.duration_ms is not None},
        }


def get_tracer(trace_id: str = None) -> RequestTracer:
    return RequestTracer(trace_id)
