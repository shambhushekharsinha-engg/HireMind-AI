import pytest
from app.database.session import SessionLocal
from app.repositories.user_repository import user_repository
from app.repositories.resume_repository import resume_repository
from app.repositories.job_repository import job_repository
from app.repositories.application_repository import application_repository

def test_user_repository_crud():
    db = SessionLocal()
    try:
        user = user_repository.create(db, {
            "email": "repo_user@hiremind.ai",
            "hashed_password": "hashed_pass_123",
            "full_name": "Repo User"
        })
        assert user.id is not None
        fetched = user_repository.get_by_email(db, "repo_user@hiremind.ai")
        assert fetched.id == user.id

        updated = user_repository.update(db, user, {"full_name": "Updated Repo User"})
        assert updated.full_name == "Updated Repo User"

        deleted = user_repository.delete(db, user.id, soft=True)
        assert deleted is True
        assert user_repository.get_by_email(db, "repo_user@hiremind.ai") is None
    finally:
        db.close()

def test_resume_repository_crud():
    db = SessionLocal()
    try:
        resume = resume_repository.create(db, {
            "title": "Repo Resume",
            "filename": "repo_resume.pdf",
            "raw_text": "Experienced Python Software Engineer skilled in FastAPI and Docker."
        })
        assert resume.id is not None

        rev = resume_repository.create_revision(
            db, resume_id=resume.id, version_number=1, filename="repo_resume.pdf", file_path="/tmp/path", raw_text=resume.raw_text
        )
        assert rev.id is not None

        analysis = resume_repository.create_analysis(
            db, resume_id=resume.id, revision_id=rev.id, ats_score=88.5, rating="Strong"
        )
        assert analysis.id is not None
        latest = resume_repository.get_latest_analysis(db, resume.id)
        assert latest.ats_score == 88.5
    finally:
        db.close()

def test_job_and_application_repositories():
    db = SessionLocal()
    try:
        job = job_repository.create(db, {
            "title": "Senior Backend Developer",
            "company": "HireMind Inc",
            "description_text": "Looking for FastAPI, Python, PostgreSQL, and Docker expert."
        })
        assert job.id is not None

        app_obj = application_repository.create(db, {
            "company": "HireMind Inc",
            "position": "Senior Backend Developer",
            "status": "Applied"
        })
        assert app_obj.id is not None
        updated_app = application_repository.update_status(db, app_obj.id, "Interviewing")
        assert updated_app.status == "Interviewing"
    finally:
        db.close()
