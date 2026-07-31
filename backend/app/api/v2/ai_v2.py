from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.services.cover_letter_service import CoverLetterService
from app.services.linkedin_service import LinkedInService
from app.services.company_insights_service import CompanyInsightsService
from app.services.explainability_service import ExplainabilityService

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

@router.post("/cover-letter")
def generate_cover_letter(request: CoverLetterRequest):
    return CoverLetterService.generate_cover_letter(
        candidate_name=request.candidate_name,
        company_name=request.company_name,
        job_title=request.job_title,
        resume_text=request.resume_text,
        job_description=request.job_description or ""
    )

@router.post("/linkedin-optimize")
def optimize_linkedin(request: LinkedInOptimizeRequest):
    return LinkedInService.optimize_profile(
        headline=request.headline,
        summary=request.summary,
        target_role=request.target_role or "Software Engineer"
    )

@router.post("/company-blueprint")
def get_company_blueprint(request: CompanyBlueprintRequest):
    return CompanyInsightsService.get_company_blueprint(request.target_company)

@router.post("/explain-ats")
def explain_ats_score(request: ExplainabilityRequest):
    return ExplainabilityService.explain_ats_score(
        ats_score=request.ats_score,
        section_scores=request.section_scores or {},
        skills_count=request.skills_count
    )
