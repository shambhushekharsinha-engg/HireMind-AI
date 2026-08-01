from app.schemas.all_schemas import CoachAskRequest, CoachAskResponse
from app.services.career_coach import CareerCoachService
from fastapi import APIRouter

router = APIRouter(prefix="/coach", tags=["AI Career Coach"])


@router.post("/ask", response_model=CoachAskResponse)
def ask_career_coach(request: CoachAskRequest):
    result = CareerCoachService.ask_coach(request.question)
    return result
