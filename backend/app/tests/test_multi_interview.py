from app.services.interview_service import interview_service


def test_multi_domain_interview_questions():
    blueprint = interview_service.generate_interview_blueprint("ML Engineer", ["Python", "PyTorch"])
    assert blueprint["total_questions"] == 5
    domains = [q["domain"] for q in blueprint["question_blueprint"]]
    assert "Technical" in domains
    assert "HR" in domains
    assert "Behavioral" in domains
    assert "Project Discussion" in domains
    assert "Resume Discussion" in domains


def test_multi_dimensional_answer_evaluation():
    eval_res = interview_service.evaluate_user_answer(
        "How do you scale FastAPI?",
        "We containerized our high-throughput FastAPI microservices using Docker and Kubernetes, integrated Redis caching for frequent database query responses, and optimized PostgreSQL index scans to achieve sub-50ms latency.",
    )
    assert eval_res["overall_score"] > 75.0
    assert eval_res["scoring_dimensions"]["technical_depth"] == 90.0
    assert eval_res["scoring_dimensions"]["relevance"] > 50.0
