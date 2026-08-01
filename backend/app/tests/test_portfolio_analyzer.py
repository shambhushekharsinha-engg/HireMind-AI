from app.services.portfolio_analyzer import portfolio_analyzer


def test_modular_portfolio_analyzer():
    res = portfolio_analyzer.analyze_candidate_portfolio(
        github_username="alex_dev",
        linkedin_url="linkedin.com/in/alex_dev",
        skills=["Python", "FastAPI", "Docker", "PostgreSQL"],
    )
    assert res["overall_candidate_score"] > 75.0
    modules = res["modules"]
    assert "github_analyzer" in modules
    assert "linkedin_analyzer" in modules
    assert "resume_analyzer" in modules
    assert "project_analyzer" in modules
