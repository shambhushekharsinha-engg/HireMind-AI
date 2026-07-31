from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.all_models import ResumeAnalysis, Resume, User

class RecruiterService:

    @classmethod
    def search_candidates(cls, db: Session, skills: List[str] = None, min_ats: float = 0.0) -> List[Dict[str, Any]]:
        query = db.query(ResumeAnalysis, Resume, User).join(Resume, ResumeAnalysis.resume_id == Resume.id).outerjoin(User, Resume.user_id == User.id)

        if min_ats > 0:
            query = query.filter(ResumeAnalysis.ats_score >= min_ats)

        results = query.order_by(ResumeAnalysis.ats_score.desc()).all()

        candidates = []
        for analysis, resume, user in results:
            found_skills = analysis.skills_found or []
            
            # If skills filter provided, check matching count
            if skills:
                matched_count = len(set(s.lower() for s in skills).intersection(set(s.lower() for s in found_skills)))
                if matched_count == 0:
                    continue
            else:
                matched_count = len(found_skills)

            candidates.append({
                "analysis_id": analysis.id,
                "resume_id": resume.id,
                "candidate_name": user.full_name if user and user.full_name else f"Candidate #{resume.id}",
                "email": user.email if user else "N/A",
                "filename": resume.filename,
                "ats_score": analysis.ats_score,
                "rating": analysis.rating,
                "skills": found_skills,
                "matched_skill_count": matched_count,
                "uploaded_at": resume.uploaded_at.strftime("%Y-%m-%d %H:%M") if resume.uploaded_at else ""
            })

        return candidates
