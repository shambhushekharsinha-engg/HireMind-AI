import requests

BASE_V1 = "http://127.0.0.1:8000/api/v1"
BASE_V2 = "http://127.0.0.1:8000/api/v2"

def run_tests():
    print("--- 1. Testing Root, Health & Prometheus Metrics Endpoints ---")
    res = requests.get("http://127.0.0.1:8000/")
    print("Root Response:", res.json())
    assert res.status_code == 200

    res_health = requests.get("http://127.0.0.1:8000/health")
    print("Health Check:", res_health.json())
    assert res_health.status_code == 200

    res_metrics = requests.get("http://127.0.0.1:8000/metrics")
    print("Prometheus Metrics Header:", res_metrics.text[:60])
    assert res_metrics.status_code == 200

    print("\n--- 2. Testing API v2 Cover Letter Generator ---")
    cover_req = {
        "candidate_name": "Alex Mercer",
        "company_name": "Microsoft",
        "job_title": "Software Engineer",
        "resume_text": "Python React FastAPI Machine Learning SQL"
    }
    res_cover = requests.post(f"{BASE_V2}/ai/cover-letter", json=cover_req)
    print("Cover Letter Output:", res_cover.json()["cover_letter_text"][:120] + "...")
    assert res_cover.status_code == 200

    print("\n--- 3. Testing API v2 LinkedIn Profile Optimizer ---")
    li_req = {
        "headline": "Software Engineer at Tech Co | Python & React",
        "summary": "Passionate software developer building cloud applications."
    }
    res_li = requests.post(f"{BASE_V2}/ai/linkedin-optimize", json=li_req)
    print("LinkedIn SEO Score:", res_li.json()["headline_seo_score"])
    assert res_li.status_code == 200

    print("\n--- 4. Testing API v2 Target Company Blueprint ---")
    blueprint_req = {"target_company": "microsoft"}
    res_bp = requests.post(f"{BASE_V2}/ai/company-blueprint", json=blueprint_req)
    print("Company Blueprint:", res_bp.json()["company_name"], "| Difficulty:", res_bp.json()["interview_difficulty"])
    assert res_bp.status_code == 200

    print("\n--- 5. Testing API v2 ATS Explainability Engine ---")
    explain_req = {
        "ats_score": 84.5,
        "skills_count": 8,
        "section_scores": {"skill_match": 28.0, "sections_completeness": 20.0, "length_hygiene": 15.0}
    }
    res_ex = requests.post(f"{BASE_V2}/ai/explain-ats", json=explain_req)
    print("Interview Call Probability:", res_ex.json()["interview_call_probability"])
    assert res_ex.status_code == 200

    print("\n--- 6. Testing API v2 Version Control Diff ---")
    diff_req = {
        "v1_text": "Alex Mercer. Developer with Python and SQL.",
        "v2_text": "Alex Mercer. Software Engineer. Skills: Python, SQL, FastAPI, React, Docker, ML."
    }
    res_diff = requests.post(f"{BASE_V2}/resume/compare-versions", json=diff_req)
    print("Version ATS Delta:", res_diff.json()["score_delta"], "pts | Added Skills:", res_diff.json()["added_skills"])
    assert res_diff.status_code == 200

    print("\n--- 7. Testing API v2 GitHub Repo Analyzer ---")
    github_req = {"repo_url": "https://github.com/shambhushekharsinha-engg/HireMind-AI"}
    res_gh = requests.post(f"{BASE_V2}/integrations/github-analyze", json=github_req)
    print("GitHub Repo Score:", res_gh.json()["overall_repo_quality_score"])
    assert res_gh.status_code == 200

    print("\n--- ALL ENTERPRISE API V1 & V2 TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_tests()
