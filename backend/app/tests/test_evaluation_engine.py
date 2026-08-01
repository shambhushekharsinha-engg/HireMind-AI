import pytest
from app.services.evaluation_engine import evaluation_engine
from app.services.resume_quality_pipeline import resume_quality_pipeline

def test_resume_quality_pipeline():
    sample_text = """
    John Doe
    Software Engineer | Python & Cloud Architecture
    
    Experience:
    - Built and architected high-performance FastAPI microservices serving over 1,000,000 requests per day.
    - Spearheaded legacy migration to Docker and Kubernetes, reducing infrastructure costs by 35%.
    - Developed automated CI/CD pipelines increasing deployment frequency by 40%.
    
    Education:
    Bachelor of Science in Computer Science
    
    Skills:
    Python, FastAPI, Docker, Kubernetes, PostgreSQL, Git, CI/CD
    """
    res = resume_quality_pipeline.analyze(sample_text)
    assert res["overall_quality_score"] > 60.0
    assert res["feature_breakdown"]["quantified_achievements"] > 50.0
    assert "built" in res["action_verbs_detected"] or "architected" in res["action_verbs_detected"]

def test_unified_evaluation_engine():
    sample_text = """
    Jane Smith
    Senior Backend Engineer | Python & Distributed Systems
    
    Experience:
    - Designed and implemented scalable RESTful microservices using Python, FastAPI, and PostgreSQL.
    - Containerized microservices with Docker and Kubernetes, scaling active instances by 200%.
    - Reduced database query latency by 45% using Redis caching and index optimizations.
    
    Education:
    Master of Science in Computer Science
    
    Skills:
    Python, FastAPI, Docker, Kubernetes, PostgreSQL, Redis, REST APIs, Git
    """
    sample_jd = "Looking for Python, FastAPI, Docker, and Kubernetes developer."
    
    eval_res = evaluation_engine.evaluate_resume(sample_text, job_description_text=sample_jd)
    assert "ats_score" in eval_res
    assert eval_res["ats_score"] >= 50.0
    assert "job_match" in eval_res
    assert "Python" in eval_res["job_match"]["matched_skills"]
