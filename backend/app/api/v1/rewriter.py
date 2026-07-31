from fastapi import APIRouter
from app.schemas.all_schemas import BulletRewriteRequest, BulletRewriteResponse
from app.services.resume_rewriter import ResumeRewriter

router = APIRouter(prefix="/rewriter", tags=["Resume Bullet Rewriter"])

@router.post("/rewrite", response_model=BulletRewriteResponse)
def rewrite_bullet(request: BulletRewriteRequest):
    result = ResumeRewriter.rewrite_bullet(request.bullet_point, request.target_role or "Software Engineer")
    return result
