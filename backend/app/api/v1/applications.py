from typing import List

from app.database.session import get_db
from app.repositories.application_repository import application_repository
from app.schemas.all_schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/applications", tags=["Job Application Tracker"])


@router.get("", response_model=List[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    return application_repository.get_all(db)


@router.post("", response_model=ApplicationResponse)
def create_application(app_in: ApplicationCreate, db: Session = Depends(get_db)):
    return application_repository.create(
        db,
        {
            "company": app_in.company,
            "position": app_in.position,
            "status": app_in.status or "Saved",
            "location": app_in.location,
            "salary_range": app_in.salary_range,
            "notes": app_in.notes,
        },
    )


@router.patch("/{app_id}", response_model=ApplicationResponse)
def update_application(app_id: int, app_update: ApplicationUpdate, db: Session = Depends(get_db)):
    app_obj = application_repository.get_by_id(db, app_id)
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found.")

    update_data = {}
    if app_update.status:
        update_data["status"] = app_update.status
    if app_update.notes is not None:
        update_data["notes"] = app_update.notes

    return application_repository.update(db, app_obj, update_data)


@router.delete("/{app_id}")
def delete_application(app_id: int, db: Session = Depends(get_db)):
    success = application_repository.delete(db, app_id)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found.")
    return {"message": "Application deleted successfully"}
