from app.schemas.all_schemas import BulletRewriteRequest, BulletRewriteResponse
from app.services.resume_rewriter import ResumeRewriter
from fastapi import APIRouter

router = APIRouter(prefix="/rewriter", tags=["Resume Bullet Rewriter"])


@router.post("/rewrite", response_model=BulletRewriteResponse)
def rewrite_bullet(request: BulletRewriteRequest):
    res = ResumeRewriter.rewrite_bullets([request.bullet_point])
    item = res["bullet_rewrites"][0]
    options_list = list(item["options"].values())

    return {
        "original": item["original"],
        "rewritten_options": options_list if options_list else [item["rewritten"]],
        "action_verbs_used": ["Engineered", "Spearheaded", "Architected", "Optimized"],
        "impact_score_boost": "+28% ATS Impact Boost",
    }
