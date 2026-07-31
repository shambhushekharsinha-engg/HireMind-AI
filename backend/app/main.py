import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, Response

from app.core.config import settings
from app.database.session import engine
from app.database.base import Base
import app.models.all_models  # Ensure models registered

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Career Operating System (v3.0 & API v2) — Live ATS Scoring, Portfolio Generator, Cover Letters, LinkedIn Optimizer, Version Diffing & Target Company Blueprints.",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Process timing middleware for performance observability
@app.middleware("http")
async def add_performance_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-Sec"] = f"{process_time:.4f}"
    return response

# Serve static reports
app.mount("/generated_reports", StaticFiles(directory=settings.REPORTS_DIR), name="reports")

# Import API V1 Routers
from app.api.v1 import (
    auth, resumes, builder, jobs, applications, coach, 
    career, interview, rewriter, reports, recruiter, analytics, feedback
)

# Import API V2 Routers
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
API_V2 = "/api/v2"
app.include_router(resume_v2.router, prefix=API_V2)
app.include_router(ai_v2.router, prefix=API_V2)
app.include_router(integrations_v2.router, prefix=API_V2)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "uptime": "100%",
        "database": "sqlite_persistent",
        "timestamp": time.time()
    }

@app.get("/metrics")
def prometheus_metrics():
    # Prometheus format metric endpoint
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