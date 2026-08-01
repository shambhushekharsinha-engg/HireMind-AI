from typing import Optional, List
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.all_models import JobApplication

class ApplicationRepository(BaseRepository[JobApplication]):
    def __init__(self):
        super().__init__(JobApplication)

    def get_by_user_id(self, db: Session, user_id: int, status: str = None, skip: int = 0, limit: int = 100) -> List[JobApplication]:
        q = db.query(JobApplication).filter(
            JobApplication.user_id == user_id,
            JobApplication.deleted_at.is_(None)
        )
        if status:
            q = q.filter(JobApplication.status == status)
        return q.offset(skip).limit(limit).all()

    def update_status(self, db: Session, application_id: int, new_status: str) -> Optional[JobApplication]:
        app_obj = self.get_by_id(db, application_id)
        if not app_obj:
            return None
        app_obj.status = new_status
        db.add(app_obj)
        db.commit()
        db.refresh(app_obj)
        return app_obj

application_repository = ApplicationRepository()
