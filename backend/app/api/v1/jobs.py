from app.database.session import get_db
from app.repositories.job_repository import job_repository
from app.repositories.resume_repository import resume_repository
from app.schemas.all_schemas import JobMatchRequest, JobMatchResult
from app.services.job_match_service import JobMatchService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/jobs", tags=["Job Matching"])


@router.post("/match", response_model=JobMatchResult)
def match_job(request: JobMatchRequest, db: Session = Depends(get_db)):
    resume_text = request.resume_text

    if not resume_text and request.resume_id:
        resume = resume_repository.get_by_id(db, request.resume_id)
        if resume:
            resume_text = resume.raw_text

    if not resume_text:
        raise HTTPException(status_code=400, detail="Either resume_text or valid resume_id must be provided.")

    match_result = JobMatchService.match(resume_text, request.job_description)

    # Save match to DB using JobRepository
    if request.resume_id:
        job_desc = job_repository.create(
            db,
            {
                "title": request.job_title or "Target Position",
                "description_text": request.job_description,
                "required_skills": match_result["matched_skills"] + match_result["missing_skills"],
            },
        )

        job_repository.create_match(
            db,
            resume_id=request.resume_id,
            job_id=job_desc.id,
            match_score=match_result["match_score"],
            matched_skills=match_result["matched_skills"],
            missing_skills=match_result["missing_skills"],
            recommendations=match_result["recommendations"],
        )

    return match_result
