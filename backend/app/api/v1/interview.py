from app.schemas.all_schemas import (
    AnswerEvalRequest,
    AnswerEvalResult,
    InterviewGenerateRequest,
    InterviewSessionResult,
)
from app.services.interview_service import interview_service
from fastapi import APIRouter

router = APIRouter(prefix="/interview", tags=["Interview Intelligence"])


@router.post("/questions", response_model=InterviewSessionResult)
def generate_questions(request: InterviewGenerateRequest):
    questions_list = interview_service.generate_formatted_questions(
        target_role=request.target_role or "Software Engineer",
        resume_text=request.resume_text,
    )
    return {
        "target_role": request.target_role or "Software Engineer",
        "questions": questions_list,
    }


@router.post("/evaluate", response_model=AnswerEvalResult)
def evaluate_answer(request: AnswerEvalRequest):
    result = interview_service.evaluate_user_answer(
        question=request.question,
        user_answer=request.user_answer,
    )
    return {
        "score": result["overall_score"],
        "feedback": result["final_report"],
        "strengths": [
            f"Strong relevance ({result['scoring_dimensions']['relevance']}%)",
            f"Good communication clarity ({result['scoring_dimensions']['communication']}%)",
        ],
        "improvements": [
            f"Increase technical depth ({result['scoring_dimensions']['technical_depth']}%)",
            result["suggested_follow_up"],
        ],
        "overall_score": result["overall_score"],
        "scoring_dimensions": result["scoring_dimensions"],
    }
