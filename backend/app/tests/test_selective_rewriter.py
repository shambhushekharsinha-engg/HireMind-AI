import pytest
from app.services.resume_rewriter import resume_rewriter

def test_selective_bullet_rewriting():
    bullets = [
        "Worked on backend python code and fixed bugs.",
        "Architected scalable microservices using FastAPI and Docker, processing 500,000 requests/day."
    ]
    res = resume_rewriter.rewrite_bullets(bullets)
    assert res["total_bullets_analyzed"] == 2
    assert res["weak_bullets_detected"] == 1

    rewrites = res["bullet_rewrites"]
    assert rewrites[0]["is_weak"] is True
    assert rewrites[0]["status"] == "PROPOSED_REWRITE"
    assert rewrites[1]["is_weak"] is False
    assert rewrites[1]["status"] == "PRESERVED"
