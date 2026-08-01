from app.services.ai_memory_service import ai_memory_service


def test_ai_memory_score_evolution():
    history = [
        {"created_at": "2026-07-01", "ats_score": 68.0},
        {"created_at": "2026-07-15", "ats_score": 76.0},
        {"created_at": "2026-08-01", "ats_score": 84.0},
    ]
    res = ai_memory_service.analyze_score_evolution(history)
    assert res["initial_score"] == 68.0
    assert res["latest_score"] == 84.0
    assert res["net_improvement"] == 16.0
    assert len(res["explainable_notes"]) > 0
