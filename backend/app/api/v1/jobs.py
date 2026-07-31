from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.all_models import Resume, JobMatch, JobDescription
from app.schemas.all_schemas import JobMatchRequest, JobMatchResult
from app.services.job_match_service import JobMatchService

router = APIRouter(prefix="/jobs", tags=["Job Matching"])

@router.post("/match", response_model=JobMatchResult)
def match_job(request: JobMatchRequest, db: Session = Depends(get_db)):
    resume_text = request.resume_text

    if not resume_text and request.resume_id:
        resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
        if resume:
            resume_text = resume.raw_text

    if not resume_text:
        raise HTTPException(status_code=400, detail="Either resume_text or valid resume_id must be provided.")

    match_result = JobMatchService.match(resume_text, request.job_description)

    # Save match to DB
    if request.resume_id:
        job_desc = JobDescription(
            title=request.job_title or "Target Position",
            description_text=request.job_description,
            required_skills=match_result["matched_skills"] + match_result["missing_skills"]
        )
        db.add(job_desc)
        db.commit()
        db.refresh(job_desc)

        job_match = JobMatch(
            resume_id=request.resume_id,
            job_id=job_desc.id,
            match_score=match_result["match_score"],
            matched_skills=match_result["matched_skills"],
            missing_skills=match_result["missing_skills"],
            recommendations=match_result["recommendations"]
        )
        db.add(job_match)
        db.commit()

    return match_result
