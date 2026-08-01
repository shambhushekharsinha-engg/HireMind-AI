import pytest
from app.services.explainability_service import explainability_service

def test_explainability_skill_recommendation():
    explanation = explainability_service.explain_skill_recommendation("Docker", 85.0)
    assert "Docker" in explanation["recommendation"]
    assert "85.0%" in explanation["reason"]
    assert explanation["impact_score"] == "High"

def test_explainability_bullet_rewrite():
    explanation = explainability_service.explain_bullet_rewrite("worked on python backend")
    assert "worked on python backend" in explanation["original_bullet"]
    assert "reason" in explanation
