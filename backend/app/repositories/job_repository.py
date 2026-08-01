from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.all_models import JobDescription, JobMatch

class JobRepository(BaseRepository[JobDescription]):
    def __init__(self):
        super().__init__(JobDescription)

    def search_jobs(self, db: Session, query: str = None, skip: int = 0, limit: int = 100) -> List[JobDescription]:
        q = db.query(JobDescription).filter(JobDescription.deleted_at.is_(None))
        if query:
            q = q.filter(
                (JobDescription.title.ilike(f"%{query}%")) |
                (JobDescription.company.ilike(f"%{query}%")) |
                (JobDescription.description_text.ilike(f"%{query}%"))
            )
        return q.offset(skip).limit(limit).all()

    def create_match(self, db: Session, resume_id: int, job_id: Optional[int], match_score: float, matched_skills: list = None, missing_skills: list = None, recommendations: list = None) -> JobMatch:
        job_match = JobMatch(
            resume_id=resume_id,
            job_id=job_id,
            match_score=match_score,
            matched_skills=matched_skills or [],
            missing_skills=missing_skills or [],
            recommendations=recommendations or []
        )
        db.add(job_match)
        db.commit()
        db.refresh(job_match)
        return job_match

    def get_matches_for_resume(self, db: Session, resume_id: int) -> List[JobMatch]:
        return db.query(JobMatch).filter(
            JobMatch.resume_id == resume_id,
            JobMatch.deleted_at.is_(None)
        ).all()

job_repository = JobRepository()
