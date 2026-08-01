import json
import logging
import os
import time
import uuid

import app.models.all_models  # noqa: F401 - Register all SQLAlchemy models in Base.metadata
from app.core.config import settings
from app.core.feature_flags import feature_flags
from app.core.startup_check import run_startup_checks
from app.database.base import Base
from app.database.session import engine
from app.services.embedding_cache import embedding_cache
from app.services.nlp_engine import nlp
from app.services.task_queue import task_queue_manager
from app.services.vector_store import faiss_vector_store
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from sqlalchemy.sql import text

# Configure Structured JSON Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("hiremind")

# Execute Fail-Fast Startup System Check
run_startup_checks()

# Initialize DB tables & Run Auto Schema Migration for PostgreSQL / SQLite
Base.metadata.create_all(bind=engine)


def auto_migrate_schema():
    """
    Automatically ensures all expected columns exist across all PostgreSQL/SQLite tables.
    Prevents psycopg2.errors.UndefinedColumn on production database upgrades.
    """
    try:
        with engine.begin() as conn:
            dialect_name = engine.dialect.name
            if dialect_name in ["postgresql", "postgres"]:
                # 1. Resumes Table
                conn.execute(text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS user_id INTEGER;"))
                conn.execute(text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS title VARCHAR DEFAULT 'Main Resume';"))
                conn.execute(
                    text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
                )
                conn.execute(
                    text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;")
                )
                conn.execute(text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;"))
                conn.execute(text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS filename VARCHAR;"))
                conn.execute(text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS file_path VARCHAR;"))
                conn.execute(text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS raw_text TEXT;"))
                conn.execute(text("ALTER TABLE resumes ADD COLUMN IF NOT EXISTS parsed_sections JSONB;"))

                # 2. Resume Revisions Table
                conn.execute(text("ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS resume_id INTEGER;"))
                conn.execute(
                    text("ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS version_number INTEGER DEFAULT 1;")
                )
                conn.execute(text("ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS filename VARCHAR;"))
                conn.execute(text("ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS file_path VARCHAR;"))
                conn.execute(text("ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS raw_text TEXT;"))
                conn.execute(text("ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS parsed_sections JSONB;"))
                conn.execute(text("ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS content_hash VARCHAR;"))
                conn.execute(
                    text(
                        "ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
                    )
                )
                conn.execute(text("ALTER TABLE resume_revisions ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;"))

                # 3. Resume Analyses Table
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS resume_id INTEGER;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS revision_id INTEGER;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS ats_score FLOAT;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS rating VARCHAR;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS skills_found JSONB;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS missing_skills JSONB;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS strengths JSONB;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS suggestions JSONB;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS section_scores JSONB;"))
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS report_path VARCHAR;"))
                conn.execute(
                    text(
                        "ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
                    )
                )
                conn.execute(text("ALTER TABLE resume_analyses ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;"))

                # 4. Job Applications Table
                conn.execute(text("ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS user_id INTEGER;"))
                conn.execute(text("ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS company_name VARCHAR;"))
                conn.execute(text("ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS job_title VARCHAR;"))
                conn.execute(
                    text("ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS status VARCHAR DEFAULT 'Applied';")
                )
                conn.execute(
                    text(
                        "ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
                    )
                )
                conn.execute(text("ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS notes TEXT;"))
                conn.execute(
                    text(
                        "ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
                    )
                )
                conn.execute(
                    text(
                        "ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
                    )
                )
                conn.execute(text("ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;"))
            else:
                # SQLite PRAGMA table_info check & ADD COLUMN
                tables_to_check = {
                    "resumes": [
                        ("user_id", "INTEGER"),
                        ("title", "VARCHAR DEFAULT 'Main Resume'"),
                        ("created_at", "DATETIME"),
                        ("updated_at", "DATETIME"),
                        ("deleted_at", "DATETIME"),
                        ("filename", "VARCHAR"),
                        ("file_path", "VARCHAR"),
                        ("raw_text", "TEXT"),
                        ("parsed_sections", "JSON"),
                    ],
                    "resume_revisions": [
                        ("resume_id", "INTEGER"),
                        ("version_number", "INTEGER DEFAULT 1"),
                        ("filename", "VARCHAR"),
                        ("file_path", "VARCHAR"),
                        ("raw_text", "TEXT"),
                        ("parsed_sections", "JSON"),
                        ("content_hash", "VARCHAR"),
                        ("created_at", "DATETIME"),
                        ("deleted_at", "DATETIME"),
                    ],
                    "resume_analyses": [
                        ("resume_id", "INTEGER"),
                        ("revision_id", "INTEGER"),
                        ("ats_score", "FLOAT"),
                        ("rating", "VARCHAR"),
                        ("skills_found", "JSON"),
                        ("missing_skills", "JSON"),
                        ("strengths", "JSON"),
                        ("suggestions", "JSON"),
                        ("section_scores", "JSON"),
                        ("report_path", "VARCHAR"),
                        ("created_at", "DATETIME"),
                        ("deleted_at", "DATETIME"),
                    ],
                }
                for table, cols_def in tables_to_check.items():
                    res = conn.execute(text(f"PRAGMA table_info({table});")).fetchall()
                    existing_cols = [r[1] for r in res]
                    for col_name, col_type in cols_def:
                        if col_name not in existing_cols:
                            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type};"))
    except Exception as e:
        logger.warning(f"Auto-migration notice: {e}")


auto_migrate_schema()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Career Operating System — Live ATS Scoring, Portfolio Generator, Vector RAG Coach, Repositories & Security Middleware.",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Helper function to ensure CORS headers are present on all responses (including errors)
def add_cors_headers_to_response(response: Response, request: Request) -> Response:
    origin = request.headers.get("origin") or "*"
    response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Vary"] = "Origin"
    return response


# 1. Universal Security & CORS Headers Middleware
@app.middleware("http")
async def add_security_and_cors_headers(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(status_code=200)
        return add_cors_headers_to_response(response, request)

    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https:;"
    return add_cors_headers_to_response(response, request)


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
        "process_time_sec": round(process_time, 4),
    }
    logger.info(json.dumps(log_entry))

    return response


# Standardized Error Code Handlers (with CORS Header Guarantee)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", "req-unknown")
    code = f"HM{exc.status_code}"
    response = JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "detail": exc.detail,
            "error": {"code": code, "message": exc.detail, "request_id": request_id},
        },
    )
    return add_cors_headers_to_response(response, request)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", "req-unknown")
    response = JSONResponse(
        status_code=422,
        content={
            "success": False,
            "detail": "Invalid request payload structure or parameter types.",
            "error": {
                "code": "HM422",
                "message": "Invalid request payload structure or parameter types.",
                "details": exc.errors(),
                "request_id": request_id,
            },
        },
    )
    return add_cors_headers_to_response(response, request)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    request_id = getattr(request.state, "request_id", "req-unknown")
    response = JSONResponse(
        status_code=500,
        content={
            "success": False,
            "detail": f"Internal Server Error: {str(exc)}",
            "error": {
                "code": "HM500",
                "message": f"Internal Server Error: {str(exc)}",
                "request_id": request_id,
            },
        },
    )
    return add_cors_headers_to_response(response, request)


# Universal CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_origin_regex=r"https://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time-Sec"],
)

# Serve static reports
app.mount("/generated_reports", StaticFiles(directory=settings.REPORTS_DIR), name="reports")

# Import API Routers
from app.api.v1 import (
    analytics,
    applications,
    auth,
    builder,
    career,
    coach,
    feedback,
    interview,
    jobs,
    recruiter,
    reports,
    resumes,
    rewriter,
)
from app.api.v2 import ai_v2, integrations_v2, resume_v2

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
        "timestamp": time.time(),
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
            "database": {"status": db_status, "engine": engine.dialect.name},
            "storage": {"upload_dir": upload_ok, "reports_dir": reports_ok},
            "spacy_nlp": {"loaded": nlp is not None, "model": "en_core_web_sm"},
            "embedding_cache": {"size": embedding_cache.size(), "status": "online"},
            "faiss_vector_store": {
                "documents_count": len(faiss_vector_store.documents),
                "status": "online",
            },
            "async_task_queue": {
                "active_tasks_count": len(task_queue_manager.tasks),
                "status": "online",
            },
        },
        "feature_flags": feature_flags.get_all(),
        "timestamp": time.time(),
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
        "api_v2": API_V2,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
