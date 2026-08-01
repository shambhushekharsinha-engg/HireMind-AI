from app.database.session import get_db
from app.models.all_models import ResumeBuilderDraft
from app.schemas.all_schemas import ResumeBuilderData
from app.services.resume_builder import ResumeBuilderService
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/builder", tags=["Resume Builder"])


@router.post("/draft")
def save_resume_draft(data: ResumeBuilderData, db: Session = Depends(get_db)):
    draft = ResumeBuilderDraft(
        title=data.title or "My Professional Resume",
        template_name=data.template_name or "Modern",
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        linkedin=data.linkedin,
        github=data.github,
        summary=data.summary,
        experience_json=data.experience,
        education_json=data.education,
        skills_json=data.skills,
        projects_json=data.projects,
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return {"message": "Resume draft saved successfully", "draft_id": draft.id}


@router.post("/download-pdf")
def download_built_resume(data: ResumeBuilderData):
    pdf_path = ResumeBuilderService.generate_resume_pdf(data.dict(), template_name=data.template_name or "Modern")
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"Resume_{data.full_name or 'Draft'}.pdf")
