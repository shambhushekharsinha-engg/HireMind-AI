from app.services.personalized_roadmap import personalized_roadmap


def test_adaptive_personalized_roadmap():
    res = personalized_roadmap.generate_roadmap(
        target_role="Lead Cloud Architect",
        current_ats_score=78.5,
        missing_skills=["Kubernetes", "Terraform"],
        completed_steps=["Master Python Fundamentals", "Build REST APIs with FastAPI"],
    )
    assert res["target_role"] == "Lead Cloud Architect"
    assert res["current_ats_score"] == 78.5
    assert len(res["completed_steps"]) == 2
    assert res["completion_percentage"] > 0.0
    assert res["next_recommended_step"]["skill"] == "Redis"
