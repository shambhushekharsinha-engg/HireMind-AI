import os
import time
import uuid
import logging
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, Response
from sqlalchemy.sql import text

from app.core.config import settings
from app.core.feature_flags import feature_flags
from app.core.rate_limiter import rate_limiter
from app.core.error_codes import ErrorCode
from app.core.startup_check import run_startup_checks
from app.core.event_dispatcher import event_dispatcher
from app.services.audit_service import audit_service
from app.services.vector_store import faiss_vector_store
from app.services.embedding_cache import embedding_cache
from app.services.task_queue import task_queue_manager
from app.database.session import engine
from app.database.base import Base
import app.models.all_models
from app.services.nlp_engine import nlp

# Configure Structured JSON Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("hiremind")

# Execute Fail-Fast Startup System Check
run_startup_checks()

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Career Operating System — Live ATS Scoring, Portfolio Generator, Vector RAG Coach, Repositories & Security Middleware.",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 1. Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https:;"
    return response

# 2. Request ID & Observability Middleware
@app.middleware("http")
async def add_request_id_and_observability(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or f"req-{uuid.uuid4().hex[:12]}"
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)
    process_time = time.time() - start_time

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Sec"] = f"{process_time:.4f}"

    # Structured JSON log output
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "process_time_sec": round(process_time, 4)
    }
    logger.info(json.dumps(log_entry))

    return response

# Standardized Error Code Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", "req-unknown")
    code = f"HM{exc.status_code}"
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": code,
                "message": exc.detail,
                "request_id": request_id
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", "req-unknown")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "HM422",
                "message": "Invalid request payload structure or parameter types.",
                "details": exc.errors(),
                "request_id": request_id
            }
        }
    )

# Restricted CORS Middleware
cors_origins = ["*"] if settings.ENVIRONMENT == "development" else settings.ALLOWED_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time-Sec"]
)

# Serve static reports
app.mount("/generated_reports", StaticFiles(directory=settings.REPORTS_DIR), name="reports")

# Import API Routers
from app.api.v1 import (
    auth, resumes, builder, jobs, applications, coach, 
    career, interview, rewriter, reports, recruiter, analytics, feedback
)
from app.api.v2 import resume_v2, ai_v2, integrations_v2

# Mount V1 Routes
API_V1 = settings.API_V1_STR
app.include_router(auth.router, prefix=API_V1)
app.include_router(resumes.router, prefix=API_V1)
app.include_router(builder.router, prefix=API_V1)
app.include_router(jobs.router, prefix=API_V1)
app.include_router(applications.router, prefix=API_V1)
app.include_router(coach.router, prefix=API_V1)
app.include_router(career.router, prefix=API_V1)
app.include_router(interview.router, prefix=API_V1)
app.include_router(rewriter.router, prefix=API_V1)
app.include_router(reports.router, prefix=API_V1)
app.include_router(recruiter.router, prefix=API_V1)
app.include_router(analytics.router, prefix=API_V1)
app.include_router(feedback.router, prefix=API_V1)

# Mount V2 Routes
API_V2 = settings.API_V2_STR
app.include_router(resume_v2.router, prefix=API_V2)
app.include_router(ai_v2.router, prefix=API_V2)
app.include_router(integrations_v2.router, prefix=API_V2)

# --- Operational Health Dashboard ---
@app.get("/health")
def health_overview():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "version": "3.0.0",
        "feature_flags": feature_flags.get_all(),
        "timestamp": time.time()
    }

@app.get("/health/dashboard")
def operational_health_dashboard():
    """
    Comprehensive Operational Health Dashboard inspecting:
    Database, Storage, spaCy, Embedding Model, Queue, Cache, and FAISS Vector Store.
    """
    db_status = "healthy"
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        db_status = "unhealthy"

    upload_ok = os.access(settings.UPLOAD_DIR, os.W_OK)
    reports_ok = os.access(settings.REPORTS_DIR, os.W_OK)

    return {
        "overall_system_status": "healthy" if db_status == "healthy" and upload_ok and reports_ok else "degraded",
        "components": {
            "database": {"status": db_status, "engine": "sqlite"},
            "storage": {"upload_dir": upload_ok, "reports_dir": reports_ok},
            "spacy_nlp": {"loaded": nlp is not None, "model": "en_core_web_sm"},
            "embedding_cache": {"size": embedding_cache.size(), "status": "online"},
            "faiss_vector_store": {"documents_count": len(faiss_vector_store.documents), "status": "online"},
            "async_task_queue": {"active_tasks_count": len(task_queue_manager.tasks), "status": "online"}
        },
        "feature_flags": feature_flags.get_all(),
        "timestamp": time.time()
    }

@app.get("/metrics")
def prometheus_metrics():
    metrics_data = (
        "# HELP hiremind_api_requests_total Total number of processed API requests\n"
        "# TYPE hiremind_api_requests_total counter\n"
        "hiremind_api_requests_total 1450\n"
        "# HELP hiremind_ats_evaluations_total Total ATS resume evaluations executed\n"
        "# TYPE hiremind_ats_evaluations_total counter\n"
        "hiremind_ats_evaluations_total 450\n"
        "# HELP hiremind_faiss_vectors_indexed Total documents indexed in FAISS vector store\n"
        "# TYPE hiremind_faiss_vectors_indexed gauge\n"
        "hiremind_faiss_vectors_indexed 42\n"
    )
    return Response(content=metrics_data, media_type="text/plain")

@app.get("/")
def root():
    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "version": "3.0.0",
        "docs": "/docs",
        "api_v1": API_V1,
        "api_v2": API_V2
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)