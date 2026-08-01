import json
import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger("hiremind.audit")


class AuditService:
    """
    Structured Audit Logger for tracking security and user lifecycle events.
    Events: LOGIN, RESUME_UPLOAD, PASSWORD_RESET, ANALYSIS_GENERATED, REPORT_DOWNLOAD
    """

    @staticmethod
    def log_event(
        event_type: str,
        user_id: Optional[int] = None,
        email: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True,
    ):
        audit_payload = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event_type": event_type,
            "user_id": user_id,
            "email": email,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "success": success,
            "details": details or {},
        }
        logger.info(json.dumps(audit_payload))
        return audit_payload


audit_service = AuditService()
