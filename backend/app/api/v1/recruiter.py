from typing import Optional

from app.database.session import get_db
from app.services.recruiter_service import RecruiterService
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

router = APIRouter(prefix="/recruiter", tags=["Recruiter Candidate Portal"])


@router.get("/candidates")
def get_candidates(
    min_ats: float = Query(0.0, ge=0.0, le=100.0),
    skills: Optional[str] = Query(None, description="Comma-separated skills list e.g. python,react"),
    db: Session = Depends(get_db),
):
    skill_list = [s.strip() for s in skills.split(",") if s.strip()] if skills else None
    candidates = RecruiterService.search_candidates(db, skills=skill_list, min_ats=min_ats)
    return candidates
