import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.config import settings
from app.models.all_models import Resume, ResumeAnalysis
from app.schemas.all_schemas import ResumeAnalysisResult
from app.services.resume_parser import ResumeParser
from app.services.nlp_engine import NLPEngine
from app.services.ats_engine import ATSEngine

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", response_model=ResumeAnalysisResult)
async def upload_and_analyze_resume(
    file: UploadFile = File(...),
    user_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith((".pdf", ".docx", ".doc", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF, DOCX, and TXT files are supported.")

    file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 1. Parse File
    parsed_data = ResumeParser.parse_file(file_path, file.filename)
    raw_text = parsed_data["raw_text"]
    sections = parsed_data["sections"]

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from resume.")

    # 2. Extract Skills
    skills = NLPEngine.extract_skills(raw_text)

    # 3. Compute ATS Metrics
    ats_results = ATSEngine.evaluate(raw_text, sections, skills)

    # 4. Save to Database
    db_resume = Resume(
        user_id=user_id,
        filename=file.filename,
        file_path=file_path,
        raw_text=raw_text,
        parsed_sections=sections
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)

    # Career Suggestions Heuristic
    career_suggestions = []
    if "python" in skills and "sql" in skills:
        career_suggestions.append("Data Science / Software Engineering")
    if "react" in skills or "javascript" in skills:
        career_suggestions.append("Frontend / Full-Stack Web Development")
    if "machine learning" in skills or "tensorflow" in skills:
        career_suggestions.append("AI / Machine Learning Engineering")
    if "fastapi" in skills or "django" in skills:
        career_suggestions.append("Backend API Engineering")

    db_analysis = ResumeAnalysis(
        resume_id=db_resume.id,
        ats_score=ats_results["ats_score"],
        rating=ats_results["rating"],
        skills_found=skills,
        missing_skills=[],
        strengths=ats_results["strengths"],
        suggestions=ats_results["suggestions"],
        section_scores=ats_results["section_scores"]
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    return {
        "filename": file.filename,
        "resume_id": db_resume.id,
        "ats_score": ats_results["ats_score"],
        "rating": ats_results["rating"],
        "skills_found": skills,
        "missing_skills": [],
        "strengths": ats_results["strengths"],
        "suggestions": ats_results["suggestions"],
        "career_suggestions": career_suggestions if career_suggestions else ["Software Engineering", "Full-Stack Development"],
        "section_scores": ats_results["section_scores"],
        "parsed_sections": sections
    }

@router.get("/history")
def get_resume_history(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(ResumeAnalysis, Resume).join(Resume, ResumeAnalysis.resume_id == Resume.id)
    if user_id:
        query = query.filter(Resume.user_id == user_id)
    
    records = query.order_by(ResumeAnalysis.created_at.desc()).all()
    history = []
    for analysis, resume in records:
        history.append({
            "analysis_id": analysis.id,
            "resume_id": resume.id,
            "filename": resume.filename,
            "ats_score": analysis.ats_score,
            "rating": analysis.rating,
            "skills_found": analysis.skills_found,
            "created_at": analysis.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return history
