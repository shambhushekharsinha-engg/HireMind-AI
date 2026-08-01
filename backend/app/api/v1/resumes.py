import os
import uuid
import hashlib
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.config import settings
from app.models.all_models import Resume, ResumeRevision, ResumeAnalysis
from app.schemas.all_schemas import ResumeAnalysisResult
from app.services.resume_parser import ResumeParser
from app.services.nlp_engine import NLPEngine
from app.services.ats_engine import ATSEngine
from app.services.report_service import ReportService

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", response_model=ResumeAnalysisResult)
async def upload_and_analyze_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    # 1. Extension & Security Validation
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Read File Content & Validate Size
    content = await file.read()
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB."
        )

    # 2. SHA-256 Content Hash Caching Check
    content_hash = hashlib.sha256(content).hexdigest()
    existing_revision = db.query(ResumeRevision).filter(
        ResumeRevision.content_hash == content_hash,
        ResumeRevision.deleted_at.is_(None)
    ).first()

    if existing_revision and existing_revision.analyses:
        cached_analysis = existing_revision.analyses[0]
        parsed_sections = existing_revision.parsed_sections or {}
        skills = cached_analysis.skills_found or []

        return {
            "filename": file.filename,
            "resume_id": existing_revision.resume_id,
            "ats_score": cached_analysis.ats_score,
            "rating": cached_analysis.rating,
            "skills_found": skills,
            "missing_skills": cached_analysis.missing_skills or [],
            "strengths": cached_analysis.strengths or [],
            "suggestions": cached_analysis.suggestions or [],
            "career_suggestions": ["Software Engineering", "Full-Stack Development"],
            "section_scores": cached_analysis.section_scores or {},
            "parsed_sections": parsed_sections
        }

    # 3. Randomized Storage Path (Avoid collisions & path traversal)
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    # 4. Parse Resume
    parsed_data = ResumeParser.parse_file(file_path, file.filename)
    raw_text = parsed_data["raw_text"]
    sections = parsed_data["sections"]

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from uploaded file.")

    # 5. NLP Extraction & ATS Scorer
    skills = NLPEngine.extract_skills(raw_text)
    ats_results = ATSEngine.evaluate(raw_text, sections, skills)

    # 6. Database Storage (User -> Resume -> ResumeRevision -> ResumeAnalysis)
    db_resume = None
    if user_id:
        db_resume = db.query(Resume).filter(Resume.user_id == user_id, Resume.deleted_at.is_(None)).first()

    if not db_resume:
        db_resume = Resume(
            user_id=user_id,
            title="Main Resume",
            filename=file.filename,
            file_path=file_path,
            raw_text=raw_text,
            parsed_sections=sections
        )
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)

    # Determine Revision Version Number
    previous_revisions_count = db.query(ResumeRevision).filter(ResumeRevision.resume_id == db_resume.id).count()
    version_num = previous_revisions_count + 1

    db_revision = ResumeRevision(
        resume_id=db_resume.id,
        version_number=version_num,
        filename=file.filename,
        file_path=file_path,
        raw_text=raw_text,
        parsed_sections=sections,
        content_hash=content_hash
    )
    db.add(db_revision)
    db.commit()
    db.refresh(db_revision)

    # Career Suggestions
    career_suggestions = []
    if "Python" in skills and "SQL" in skills:
        career_suggestions.append("Data Science / Software Engineering")
    if "React" in skills or "JavaScript" in skills:
        career_suggestions.append("Frontend / Full-Stack Web Development")
    if "Machine Learning" in skills or "TensorFlow" in skills or "PyTorch" in skills:
        career_suggestions.append("AI / Machine Learning Engineering")
    if "FastAPI" in skills or "Django" in skills:
        career_suggestions.append("Backend API Engineering")

    db_analysis = ResumeAnalysis(
        resume_id=db_resume.id,
        revision_id=db_revision.id,
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

    # Async Background Task: Pre-generate PDF report
    report_payload = {
        "resume_id": db_resume.id,
        "filename": file.filename,
        "ats_score": ats_results["ats_score"],
        "rating": ats_results["rating"],
        "skills_found": skills,
        "strengths": ats_results["strengths"],
        "suggestions": ats_results["suggestions"]
    }
    background_tasks.add_task(ReportService.generate_pdf_report, report_payload)

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
    query = db.query(ResumeAnalysis, Resume).join(Resume, ResumeAnalysis.resume_id == Resume.id).filter(
        Resume.deleted_at.is_(None),
        ResumeAnalysis.deleted_at.is_(None)
    )
    if user_id:
        query = query.filter(Resume.user_id == user_id)
    
    records = query.order_by(ResumeAnalysis.created_at.desc()).all()
    history = []
    for analysis, resume in records:
        history.append({
            "analysis_id": analysis.id,
            "resume_id": resume.id,
            "filename": resume.filename or "Resume.pdf",
            "ats_score": analysis.ats_score,
            "rating": analysis.rating,
            "skills_found": analysis.skills_found,
            "created_at": analysis.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return history

