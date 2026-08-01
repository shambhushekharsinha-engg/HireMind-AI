from app.services.github_service import GitHubService
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/integrations", tags=["Integrations API v2"])


class GitHubAnalyzeRequest(BaseModel):
    repo_url: str


@router.post("/github-analyze")
def analyze_github_repo(request: GitHubAnalyzeRequest):
    return GitHubService.analyze_repo_url(request.repo_url)
