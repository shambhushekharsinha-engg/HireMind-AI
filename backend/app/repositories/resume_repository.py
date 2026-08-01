from typing import List, Optional

from app.models.all_models import Resume, ResumeAnalysis, ResumeBuilderDraft, ResumeRevision
from app.repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class ResumeRepository(BaseRepository[Resume]):
    def __init__(self):
        super().__init__(Resume)

    def get_by_user_id(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Resume]:
        return (
            db.query(Resume)
            .filter(Resume.user_id == user_id, Resume.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_revisions(self, db: Session, resume_id: int) -> List[ResumeRevision]:
        return (
            db.query(ResumeRevision)
            .filter(ResumeRevision.resume_id == resume_id, ResumeRevision.deleted_at.is_(None))
            .order_by(ResumeRevision.version_number.desc())
            .all()
        )

    def create_revision(
        self,
        db: Session,
        resume_id: int,
        version_number: int,
        filename: str,
        file_path: str,
        raw_text: str,
        parsed_sections: dict = None,
        content_hash: str = None,
    ) -> ResumeRevision:
        revision = ResumeRevision(
            resume_id=resume_id,
            version_number=version_number,
            filename=filename,
            file_path=file_path,
            raw_text=raw_text,
            parsed_sections=parsed_sections or {},
            content_hash=content_hash,
        )
        db.add(revision)
        db.commit()
        db.refresh(revision)
        return revision

    def create_analysis(
        self,
        db: Session,
        resume_id: int,
        revision_id: Optional[int],
        ats_score: float,
        rating: str,
        skills_found: list = None,
        missing_skills: list = None,
        strengths: list = None,
        suggestions: list = None,
        section_scores: dict = None,
        report_path: str = None,
    ) -> ResumeAnalysis:
        analysis = ResumeAnalysis(
            resume_id=resume_id,
            revision_id=revision_id,
            ats_score=ats_score,
            rating=rating,
            skills_found=skills_found or [],
            missing_skills=missing_skills or [],
            strengths=strengths or [],
            suggestions=suggestions or [],
            section_scores=section_scores or {},
            report_path=report_path,
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis

    def get_latest_analysis(self, db: Session, resume_id: int) -> Optional[ResumeAnalysis]:
        return (
            db.query(ResumeAnalysis)
            .filter(ResumeAnalysis.resume_id == resume_id, ResumeAnalysis.deleted_at.is_(None))
            .order_by(ResumeAnalysis.id.desc())
            .first()
        )

    def get_drafts(self, db: Session, user_id: int) -> List[ResumeBuilderDraft]:
        return (
            db.query(ResumeBuilderDraft)
            .filter(ResumeBuilderDraft.user_id == user_id, ResumeBuilderDraft.deleted_at.is_(None))
            .all()
        )


resume_repository = ResumeRepository()
