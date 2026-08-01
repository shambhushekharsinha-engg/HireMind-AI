from app.database.session import get_db
from app.models.all_models import Feedback
from app.schemas.all_schemas import FeedbackCreate
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/submit")
def submit_feedback(fb: FeedbackCreate, db: Session = Depends(get_db)):
    db_fb = Feedback(rating=fb.rating, comment=fb.comment)
    db.add(db_fb)
    db.commit()
    return {"message": "Thank you for your feedback!"}
