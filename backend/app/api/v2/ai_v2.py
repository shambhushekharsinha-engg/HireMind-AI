from typing import Dict, List, Optional

from app.services.benchmarking_service import BenchmarkingService
from app.services.company_insights_service import CompanyInsightsService
from app.services.cover_letter_service import CoverLetterService
from app.services.explainability_service import ExplainabilityService
from app.services.linkedin_service import LinkedInService
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI Engine API v2"])


class CoverLetterRequest(BaseModel):
    candidate_name: str
    company_name: str
    job_title: str
    resume_text: str
    job_description: Optional[str] = ""


class LinkedInOptimizeRequest(BaseModel):
    headline: str
    summary: str
    target_role: Optional[str] = "Software Engineer"


class CompanyBlueprintRequest(BaseModel):
    target_company: str


class ExplainabilityRequest(BaseModel):
    ats_score: float
    skills_count: int
    section_scores: Optional[Dict[str, float]] = {}


class BenchmarkRequest(BaseModel):
    resume_text: str
    target_role: Optional[str] = "Machine Learning Engineer"


class CareerGapRequest(BaseModel):
    current_skills: List[str]
    target_role: Optional[str] = "Machine Learning Engineer"


class RecruiterSummaryRequest(BaseModel):
    candidate_name: str
    resume_text: str
    target_role: Optional[str] = "Software Engineer"


@router.post("/cover-letter")
def generate_cover_letter(request: CoverLetterRequest):
    return CoverLetterService.generate_cover_letter(
        candidate_name=request.candidate_name,
        company_name=request.company_name,
        job_title=request.job_title,
        resume_text=request.resume_text,
        job_description=request.job_description or "",
    )


@router.post("/linkedin-optimize")
def optimize_linkedin(request: LinkedInOptimizeRequest):
    return LinkedInService.optimize_profile(
        headline=request.headline,
        summary=request.summary,
        target_role=request.target_role or "Software Engineer",
    )


@router.post("/company-blueprint")
def get_company_blueprint(request: CompanyBlueprintRequest):
    return CompanyInsightsService.get_company_blueprint(request.target_company)


@router.post("/explain-ats")
def explain_ats_score(request: ExplainabilityRequest):
    return ExplainabilityService.explain_ats_score(
        ats_score=request.ats_score,
        section_scores=request.section_scores or {},
        skills_count=request.skills_count,
    )


@router.post("/benchmark")
def benchmark_resume(request: BenchmarkRequest):
    return BenchmarkingService.benchmark_resume(
        resume_text=request.resume_text,
        target_role=request.target_role or "Machine Learning Engineer",
    )


@router.post("/career-gap")
def analyze_career_gap(request: CareerGapRequest):
    return BenchmarkingService.analyze_career_gap(
        current_skills=request.current_skills,
        target_role=request.target_role or "Machine Learning Engineer",
    )


@router.post("/recommend-projects")
def recommend_projects(target_role: str = "Machine Learning Engineer"):
    return BenchmarkingService.recommend_projects(target_role)


@router.post("/recruiter-summary")
def summarize_for_recruiter(request: RecruiterSummaryRequest):
    return BenchmarkingService.summarize_for_recruiter(
        candidate_name=request.candidate_name,
        resume_text=request.resume_text,
        target_role=request.target_role or "Software Engineer",
    )
