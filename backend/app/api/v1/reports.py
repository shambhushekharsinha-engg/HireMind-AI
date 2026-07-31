import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.all_models import ResumeAnalysis, Resume
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["PDF Reports"])

@router.get("/download/{analysis_id}")
def download_pdf_report(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(ResumeAnalysis, Resume).join(Resume, ResumeAnalysis.resume_id == Resume.id).filter(ResumeAnalysis.id == analysis_id).first()
    
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found.")

    analysis, resume = record
    
    analysis_data = {
        "analysis_id": analysis.id,
        "resume_id": resume.id,
        "filename": resume.filename,
        "ats_score": analysis.ats_score,
        "rating": analysis.rating,
        "skills_found": analysis.skills_found or [],
        "strengths": analysis.strengths or [],
        "suggestions": analysis.suggestions or []
    }

    pdf_path = ReportService.generate_pdf_report(analysis_data, filename_prefix="HireMind_Report")
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail="Failed to generate PDF report.")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=os.path.basename(pdf_path)
    )
