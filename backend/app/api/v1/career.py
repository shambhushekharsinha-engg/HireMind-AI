from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.all_models import Resume
from app.schemas.all_schemas import CareerRoadmapRequest, CareerRoadmapResult
from app.services.career_service import CareerService

router = APIRouter(prefix="/career", tags=["Career Intelligence"])

@router.post("/roadmap", response_model=CareerRoadmapResult)
def generate_career_roadmap(request: CareerRoadmapRequest, db: Session = Depends(get_db)):
    resume_text = request.resume_text

    if not resume_text and request.resume_id:
        resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
        if resume:
            resume_text = resume.raw_text

    roadmap_data = CareerService.generate_roadmap(resume_text or "", request.target_role)
    return roadmap_data
