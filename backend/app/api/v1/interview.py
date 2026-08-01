from app.schemas.all_schemas import (
    AnswerEvalRequest,
    AnswerEvalResult,
    InterviewGenerateRequest,
    InterviewSessionResult,
)
from app.services.interview_service import InterviewService
from fastapi import APIRouter

router = APIRouter(prefix="/interview", tags=["Interview Intelligence"])


@router.post("/questions", response_model=InterviewSessionResult)
def generate_questions(request: InterviewGenerateRequest):
    questions = InterviewService.generate_questions(request.target_role, request.resume_text)
    return {"target_role": request.target_role, "questions": questions}


@router.post("/evaluate", response_model=AnswerEvalResult)
def evaluate_answer(request: AnswerEvalRequest):
    result = InterviewService.evaluate_answer(
        question=request.question,
        user_answer=request.user_answer,
        expected_points=request.expected_points,
    )
    return result
