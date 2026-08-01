from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Generic Base Repository providing standard CRUD methods over SQLAlchemy models.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id, self.model.deleted_at.is_(None)).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).filter(self.model.deleted_at.is_(None)).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: Any) -> ModelType:
        if isinstance(obj_in, dict):
            db_obj = self.model(**obj_in)
        else:
            db_obj = obj_in
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: Any) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.__dict__
        
        for field in update_data:
            if hasattr(db_obj, field) and field != "id":
                setattr(db_obj, field, update_data[field])
                
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: Any, soft: bool = True) -> bool:
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return False
        
        if soft and hasattr(db_obj, "deleted_at"):
            import datetime
            db_obj.deleted_at = datetime.datetime.utcnow()
            db.add(db_obj)
        else:
            db.delete(db_obj)
            
        db.commit()
        return True
