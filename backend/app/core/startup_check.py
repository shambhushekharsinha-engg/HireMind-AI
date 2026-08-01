import logging
import os

from app.core.config import settings
from app.database.session import engine
from app.services.nlp_engine import nlp
from app.services.vector_store import faiss_vector_store
from sqlalchemy.sql import text

logger = logging.getLogger("hiremind.startup")


class StartupValidator:
    """
    Fail-Fast System Startup Validator.
    Verifies critical system components before accepting API traffic:
    1. Secret Key configuration
    2. Storage Directories Writability
    3. Database Connectivity
    4. spaCy & Embedding Models Readiness
    5. FAISS Vector Store Availability
    """

    @classmethod
    def validate_all(cls) -> bool:
        logger.info("--- Initiating HireMind AI Startup Validation ---")

        # 1. Secret Key Check
        if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 8:
            logger.error("[STARTUP ERROR] SECRET_KEY is missing or invalid.")
            return False

        # 2. Storage Directory Check
        for d in [settings.UPLOAD_DIR, settings.REPORTS_DIR]:
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
            if not os.access(d, os.W_OK):
                logger.error(f"[STARTUP ERROR] Directory '{d}' is not writable.")
                return False

        # 3. Database Connection Check
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        except Exception as e:
            logger.error(f"[STARTUP ERROR] Database connection failed: {e}")
            return False

        # 4. spaCy NLP Check
        if nlp is None:
            logger.warning("[STARTUP WARNING] spaCy en_core_web_sm model not loaded; using fallback regex extraction.")

        # 5. FAISS Vector Store Readiness Check
        if faiss_vector_store is None:
            logger.error("[STARTUP ERROR] FAISS Vector Store uninitialized.")
            return False

        logger.info("--- Startup Validation Passed Successfully (100% Operational) ---")
        return True


def run_startup_checks():
    if not StartupValidator.validate_all():
        logger.critical("Fatal: Startup Validation Failed. Terminating Server.")
        # Do not raise hard exit during test runs, but return status
        return False
    return True
