import pytest
from app.services.career_progress_service import career_progress_service

def test_career_progress_dashboard():
    dash = career_progress_service.get_progress_dashboard(user_id=1)
    assert dash["overall_career_readiness_index"] > 70.0
    assert len(dash["historical_ats_trend"]) == 3
    assert "technical_depth" in dash["interview_performance"]
    assert dash["roadmap_progress"]["completion_percentage"] == 75.0
