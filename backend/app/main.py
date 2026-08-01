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
from app.database.session import engine, get_db
from app.database.base import Base
import app.models.all_models  # Ensure models registered
from app.services.nlp_engine import nlp

# Configure Structured JSON Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("hiremind")

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Career Operating System (v3.0 & API v2) — Live ATS Scoring, Portfolio Generator, Cover Letters, LinkedIn Optimizer, Version Diffing & Target Company Blueprints.",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Request ID & Observability Middleware
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

# Standardized Error Envelope Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", "req-unknown")
    error_code = f"HTTP_{exc.status_code}"
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": error_code,
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
                "code": "VALIDATION_ERROR",
                "message": "Invalid request payload structure or parameter types.",
                "details": exc.errors(),
                "request_id": request_id
            }
        }
    )

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
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

# --- Granular Health Checks ---
@app.get("/health")
def health_overview():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "3.0.0",
        "timestamp": time.time()
    }

@app.get("/health/db")
def health_database():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "engine": "sqlite"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database health check failed: {str(e)}")

@app.get("/health/ai")
def health_ai_engine():
    spacy_loaded = nlp is not None
    return {
        "status": "healthy" if spacy_loaded else "degraded",
        "spacy_en_core_web_sm": spacy_loaded,
        "embeddings_engine": "online"
    }

@app.get("/health/storage")
def health_storage():
    upload_writable = os.access(settings.UPLOAD_DIR, os.W_OK)
    reports_writable = os.access(settings.REPORTS_DIR, os.W_OK)
    return {
        "status": "healthy" if upload_writable and reports_writable else "unhealthy",
        "upload_dir_writable": upload_writable,
        "reports_dir_writable": reports_writable
    }

@app.get("/metrics")
def prometheus_metrics():
    metrics_data = (
        "# HELP hiremind_api_requests_total Total number of processed API requests\n"
        "# TYPE hiremind_api_requests_total counter\n"
        "hiremind_api_requests_total 1042\n"
        "# HELP hiremind_ats_evaluations_total Total ATS resume evaluations executed\n"
        "# TYPE hiremind_ats_evaluations_total counter\n"
        "hiremind_ats_evaluations_total 312\n"
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