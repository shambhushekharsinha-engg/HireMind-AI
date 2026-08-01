import os
from typing import Dict

class FeatureFlags:
    """
    Expanded Feature Flag Manager for toggleable platform deployments.
    """
    def __init__(self):
        self._flags: Dict[str, bool] = {
            "ENABLE_EXPERIMENTAL_AI": os.getenv("FLAG_EXPERIMENTAL_AI", "true").lower() == "true",
            "ENABLE_FAISS_VECTOR_SEARCH": os.getenv("FLAG_FAISS_VECTOR_SEARCH", "true").lower() == "true",
            "ENABLE_RAG": os.getenv("FLAG_RAG", "true").lower() == "true",
            "ENABLE_INTERVIEW": os.getenv("FLAG_INTERVIEW", "true").lower() == "true",
            "ENABLE_REWRITER": os.getenv("FLAG_REWRITER", "true").lower() == "true",
            "ENABLE_ANALYTICS": os.getenv("FLAG_ANALYTICS", "true").lower() == "true",
            "ENABLE_PORTFOLIO": os.getenv("FLAG_PORTFOLIO", "true").lower() == "true",
            "ENABLE_BACKGROUND_JOBS": os.getenv("FLAG_BACKGROUND_JOBS", "true").lower() == "true",
            "ENABLE_AUDIT_LOGGING": os.getenv("FLAG_AUDIT_LOGGING", "true").lower() == "true",
            "ENABLE_RATE_LIMITING": os.getenv("FLAG_RATE_LIMITING", "true").lower() == "true"
        }

    def is_enabled(self, flag_name: str) -> bool:
        return self._flags.get(flag_name, False)

    def set_flag(self, flag_name: str, enabled: bool) -> None:
        self._flags[flag_name] = enabled

    def get_all(self) -> Dict[str, bool]:
        return self._flags.copy()

feature_flags = FeatureFlags()
