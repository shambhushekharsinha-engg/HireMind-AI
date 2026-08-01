from typing import Any, Dict, Optional

from app.services.ats_engine import ATSEngine
from app.services.nlp_engine import NLPEngine
from app.services.portfolio_service import PortfolioService
from app.services.resume_parser import ResumeParser
from app.services.version_control_service import VersionControlService
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

router = APIRouter(prefix="/resume", tags=["Resume API v2"])


class VersionCompareRequest(BaseModel):
    v1_text: str
    v2_text: str


class LiveATSRequest(BaseModel):
    resume_text: str


class PortfolioGenerateRequest(BaseModel):
    theme: Optional[str] = "dark"
    resume_data: Dict[str, Any]


@router.post("/compare-versions")
def compare_resume_versions(request: VersionCompareRequest):
    return VersionControlService.compare_versions(request.v1_text, request.v2_text)


@router.post("/live-ats-score")
def live_ats_score(request: LiveATSRequest):
    sections = ResumeParser.identify_sections(request.resume_text or "")
    skills = NLPEngine.extract_skills(request.resume_text or "")
    eval_result = ATSEngine.evaluate(request.resume_text or "", sections, skills)
    return eval_result


@router.post("/portfolio-html", response_class=HTMLResponse)
def generate_portfolio_html(request: PortfolioGenerateRequest):
    html = PortfolioService.generate_portfolio_html(request.resume_data, theme=request.theme or "dark")
    return HTMLResponse(content=html)
