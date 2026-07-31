from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.all_models import JobApplication
from app.schemas.all_schemas import ApplicationCreate, ApplicationUpdate, ApplicationResponse

router = APIRouter(prefix="/applications", tags=["Job Application Tracker"])

@router.get("", response_model=List[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    apps = db.query(JobApplication).order_by(JobApplication.created_at.desc()).all()
    return apps

@router.post("", response_model=ApplicationResponse)
def create_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    app_obj = JobApplication(
        company=app_in.company,
        position=app_in.position,
        status=app_in.status or "Saved",
        location=app_in.location,
        salary_range=app_in.salary_range,
        notes=app_in.notes
    )
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj

@router.patch("/{app_id}", response_model=ApplicationResponse)
def update_application(app_id: int, app_update: ApplicationUpdate, db: Session = Depends(get_db)):
    app_obj = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found.")
    
    if app_update.status:
        app_obj.status = app_update.status
    if app_update.notes is not None:
        app_obj.notes = app_update.notes

    db.commit()
    db.refresh(app_obj)
    return app_obj

@router.delete("/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    app_obj = db.query(JobApplication).filter(JobApplication.id == app_id).first()
    if app_obj:
        db.delete(app_obj)
        db.commit()
    return {"message": "Application deleted successfully"}
