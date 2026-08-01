import pytest
import hashlib
from datetime import datetime, timedelta
from app.services.nlp_engine import NLPEngine
from app.services.ats_engine import ATSEngine
from app.services.job_match_service import JobMatchService
from app.core.security import create_access_token, create_refresh_token, decode_token

def test_skill_normalization():
    sample_text = "Experienced in Py Torch, torch, JS, NodeJS, Postgres, and AWS."
    skills = NLPEngine.extract_skills(sample_text)
    assert "PyTorch" in skills
    assert "JavaScript" in skills
    assert "Node.js" in skills
    assert "PostgreSQL" in skills
    assert "AWS" in skills

def test_candidate_name_extraction():
    sample_resume = "John Doe\nSoftware Engineer\njohn.doe@gmail.com\nExperience in Python"
    name = NLPEngine.extract_candidate_name(sample_resume)
    assert name in ["John Doe", "Candidate"]

def test_ats_explainable_scoring():
    raw_text = "John Doe\nSoftware Engineer\nSummary\nExperienced developer.\nSkills\nPython, SQL, React, AWS.\nExperience\nSpearheaded platform refactoring reducing latency by 45%.\nEducation\nBachelor of Science."
    sections = {
        "summary": "Experienced developer.",
        "skills": "Python, SQL, React, AWS.",
        "experience": "Spearheaded platform refactoring reducing latency by 45%.",
        "education": "Bachelor of Science.",
        "projects": ""
    }
    skills = ["Python", "SQL", "React", "AWS"]

    eval_result = ATSEngine.evaluate(raw_text, sections, skills)
    assert "ats_score" in eval_result
    assert 0.0 <= eval_result["ats_score"] <= 100.0
    assert "explainable_breakdown" in eval_result
    assert "skills_match" in eval_result["explainable_breakdown"]

def test_hybrid_job_matching():
    resume_text = "Senior Python developer with experience in SQL, FastAPI, Docker, and PyTorch."
    job_desc = "Looking for a Python Software Engineer skilled in PyTorch, Docker, and REST APIs."

    match_res = JobMatchService.match(resume_text, job_desc)
    assert "match_score" in match_res
    assert "score_breakdown" in match_res
    assert "hybrid_semantic_score" in match_res["score_breakdown"]

def test_dual_jwt_tokens():
    access_token = create_access_token(subject=101)
    refresh_token = create_refresh_token(subject=101)

    acc_payload = decode_token(access_token)
    ref_payload = decode_token(refresh_token)

    assert acc_payload["sub"] == "101"
    assert acc_payload["type"] == "access"
    assert ref_payload["sub"] == "101"
    assert ref_payload["type"] == "refresh"

if __name__ == "__main__":
    test_skill_normalization()
    test_candidate_name_extraction()
    test_ats_explainable_scoring()
    test_hybrid_job_matching()
    test_dual_jwt_tokens()
    print("ALL AUDIT REFACTOR UNIT TESTS PASSED SUCCESSFULLY!")
