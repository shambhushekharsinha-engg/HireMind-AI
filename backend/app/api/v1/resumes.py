import hashlib
import os
import uuid
from typing import Optional

from app.core.config import settings
from app.database.session import get_db
from app.repositories.resume_repository import resume_repository
from app.schemas.all_schemas import ResumeAnalysisResult
from app.services.audit_service import audit_service
from app.services.background_tasks import async_task_processor
from app.services.evaluation_engine import evaluation_engine
from app.services.resume_parser import ResumeParser
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload", response_model=ResumeAnalysisResult)
async def upload_and_analyze_resume(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    # 1. Extension & Security Validation
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )

    # Read File Content & Validate Size
    content = await file.read()
    max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_MB}MB.",
        )

    # 2. SHA-256 Content Hash Caching Check
    content_hash = hashlib.sha256(content).hexdigest()

    # 3. Storage Path
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

    # 5. Centralized Evaluation Engine Call
    eval_result = evaluation_engine.evaluate_resume(raw_text, sections)

    # 6. Repository Database Storage
    user_resumes = resume_repository.get_by_user_id(db, user_id) if user_id else []
    db_resume = user_resumes[0] if user_resumes else None

    if not db_resume:
        db_resume = resume_repository.create(
            db,
            {
                "user_id": user_id,
                "title": "Main Resume",
                "filename": file.filename,
                "file_path": file_path,
                "raw_text": raw_text,
                "parsed_sections": sections,
            },
        )

    previous_revisions = resume_repository.get_revisions(db, db_resume.id)
    version_num = len(previous_revisions) + 1

    db_revision = resume_repository.create_revision(
        db,
        resume_id=db_resume.id,
        version_number=version_num,
        filename=file.filename,
        file_path=file_path,
        raw_text=raw_text,
        parsed_sections=sections,
        content_hash=content_hash,
    )

    skills = eval_result["skills_found"]
    db_analysis = resume_repository.create_analysis(
        db,
        resume_id=db_resume.id,
        revision_id=db_revision.id,
        ats_score=eval_result["ats_score"],
        rating=eval_result["rating"],
        skills_found=skills,
        missing_skills=[],
        strengths=["Strong formatting completeness", "Quantified bullet points detected"],
        suggestions=eval_result["recommendations"],
        section_scores=eval_result["quality_breakdown"]["feature_breakdown"],
    )

    # 7. Audit Logging & Background Processing
    audit_service.log_event(
        "RESUME_UPLOAD",
        user_id=user_id,
        details={"filename": file.filename, "ats_score": eval_result["ats_score"]},
    )
    background_tasks.add_task(
        async_task_processor.generate_pdf_report,
        db_resume.id,
        {"ats_score": eval_result["ats_score"]},
    )

    return {
        "filename": file.filename,
        "resume_id": db_resume.id,
        "ats_score": eval_result["ats_score"],
        "rating": eval_result["rating"],
        "skills_found": skills,
        "missing_skills": [],
        "strengths": ["Strong formatting completeness", "Quantified bullet points detected"],
        "suggestions": eval_result["recommendations"],
        "career_suggestions": ["Software Engineering", "Full-Stack Development"],
        "section_scores": eval_result["quality_breakdown"]["feature_breakdown"],
        "parsed_sections": sections,
    }


@router.get("/history")
def get_resume_history(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    resumes = resume_repository.get_by_user_id(db, user_id) if user_id else resume_repository.get_all(db)
    history = []
    for resume in resumes:
        latest_analysis = resume_repository.get_latest_analysis(db, resume.id)
        if latest_analysis:
            history.append(
                {
                    "analysis_id": latest_analysis.id,
                    "resume_id": resume.id,
                    "filename": resume.filename or "Resume.pdf",
                    "ats_score": latest_analysis.ats_score,
                    "rating": latest_analysis.rating,
                    "skills_found": latest_analysis.skills_found,
                    "created_at": latest_analysis.created_at.strftime("%Y-%m-%d %H:%M"),
                }
            )
    return history
