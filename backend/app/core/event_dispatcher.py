import logging
import time
from typing import Dict, List, Callable, Any

logger = logging.getLogger("hiremind.events")

class DomainEvent:
    def __init__(self, event_name: str, payload: Dict[str, Any]):
        self.event_name = event_name
        self.payload = payload
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

# Pre-defined Domain Event Types
class ResumeUploadedEvent(DomainEvent):
    def __init__(self, resume_id: int, filename: str, user_id: int = None):
        super().__init__("ResumeUploadedEvent", {"resume_id": resume_id, "filename": filename, "user_id": user_id})

class ResumeParsedEvent(DomainEvent):
    def __init__(self, resume_id: int, sections_count: int):
        super().__init__("ResumeParsedEvent", {"resume_id": resume_id, "sections_count": sections_count})

class ATSCalculatedEvent(DomainEvent):
    def __init__(self, resume_id: int, ats_score: float):
        super().__init__("ATSCalculatedEvent", {"resume_id": resume_id, "ats_score": ats_score})

class ReportGeneratedEvent(DomainEvent):
    def __init__(self, resume_id: int, report_path: str):
        super().__init__("ReportGeneratedEvent", {"resume_id": resume_id, "report_path": report_path})

class NotificationSentEvent(DomainEvent):
    def __init__(self, user_id: int, message: str):
        super().__init__("NotificationSentEvent", {"user_id": user_id, "message": message})

class InternalEventDispatcher:
    """
    Lightweight In-Memory Domain Event Dispatcher.
    Decouples services via Publisher-Subscriber pattern:
    ResumeUploadedEvent -> ResumeParsedEvent -> ATSCalculatedEvent -> ReportGeneratedEvent -> NotificationSentEvent.
    """
    def __init__(self):
        self._listeners: Dict[str, List[Callable[[DomainEvent], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[DomainEvent], None]) -> None:
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(handler)

    def publish(self, event: DomainEvent) -> None:
        logger.info(f"[Domain Event] Publishing {event.event_name} (timestamp: {event.timestamp})")
        handlers = self._listeners.get(event.event_name, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"[Domain Event Error] Handler {handler.__name__} failed for {event.event_name}: {e}")

event_dispatcher = InternalEventDispatcher()
