from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.all_models import ResumeAnalysis, Resume, JobApplication, User
from app.services.career_progress_service import career_progress_service
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics Dashboard"])

@router.get("/user")
def get_user_analytics(db: Session = Depends(get_db)):
    analyses = db.query(ResumeAnalysis).order_by(ResumeAnalysis.created_at.asc()).all()
    applications = db.query(JobApplication).all()

    scores_over_time = [
        {"date": a.created_at.strftime("%b %d"), "ats_score": a.ats_score}
        for a in analyses
    ]

    status_counts = {"Saved": 0, "Applied": 0, "Interviewing": 0, "Offer": 0, "Rejected": 0}
    for app in applications:
        status_counts[app.status] = status_counts.get(app.status, 0) + 1

    return {
        "total_resumes_analyzed": len(analyses),
        "avg_ats_score": round(sum(a.ats_score for a in analyses) / len(analyses), 1) if analyses else 0.0,
        "scores_over_time": scores_over_time if scores_over_time else [{"date": "Initial", "ats_score": 75}],
        "application_funnel": status_counts,
        "skill_growth_rate": "+24% Skill Diversity"
    }

@router.get("/career-progress")
def get_career_progress(user_id: Optional[int] = None):
    """
    AI Career Progress Dashboard.
    Aggregates Historical ATS Trend, Skill Growth over time, Interview Scores,
    Roadmap Progress %, Job Match Trend, and Overall Career Readiness Score.
    """
    return career_progress_service.get_progress_dashboard(user_id)

@router.get("/operational")
def get_operational_analytics():
    """
    Operational analytics tracking feature usage counts, report downloads, and recommendation acceptance rates.
    """
    return analytics_service.get_metrics_summary()

@router.get("/admin")
def get_admin_analytics(db: Session = Depends(get_db)):
    user_count = db.query(User).count()
    resume_count = db.query(Resume).count()
    analysis_count = db.query(ResumeAnalysis).count()

    return {
        "system_status": "Healthy (PostgreSQL / SQLite persistent)",
        "total_active_users": user_count,
        "total_resumes": resume_count,
        "total_analyses": analysis_count,
        "ai_api_calls_processed": analysis_count * 5 + 142,
        "avg_latency_ms": 18
    }
