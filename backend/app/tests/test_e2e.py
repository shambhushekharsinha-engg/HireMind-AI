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

    print("\n--- 2. Testing API v2 AI Resume Benchmarking ---")
    bench_req = {
        "resume_text": "Python SQL Pandas Scikit-Learn Docker Machine Learning",
        "target_role": "Machine Learning Engineer"
    }
    res_bench = requests.post(f"{BASE_V2}/ai/benchmark", json=bench_req)
    print("Percentile Score:", res_bench.json()["percentile_score"], "| Cohort:", res_bench.json()["comparison_with_top_cohort"])
    assert res_bench.status_code == 200

    print("\n--- 3. Testing API v2 Career Gap Analysis ---")
    gap_req = {
        "current_skills": ["Python", "SQL", "FastAPI"],
        "target_role": "Machine Learning Engineer"
    }
    res_gap = requests.post(f"{BASE_V2}/ai/career-gap", json=gap_req)
    print("Missing Skills:", res_gap.json()["missing_required_skills"])
    assert res_gap.status_code == 200

    print("\n--- 4. Testing API v2 AI Project Recommender ---")
    res_proj = requests.post(f"{BASE_V2}/ai/recommend-projects?target_role=Machine%20Learning%20Engineer")
    print("Recommended Project:", res_proj.json()["recommended_projects"][0]["name"])
    assert res_proj.status_code == 200

    print("\n--- 5. Testing API v2 Recruiter AI Summarizer ---")
    rec_req = {
        "candidate_name": "Alex Mercer",
        "resume_text": "Python React FastAPI Machine Learning SQL",
        "target_role": "Software Engineer"
    }
    res_rec = requests.post(f"{BASE_V2}/ai/recruiter-summary", json=rec_req)
    print("Recruiter Badge:", res_rec.json()["recruiter_recommendation_badge"])
    assert res_rec.status_code == 200

    print("\n--- ALL ENTERPRISE API V1 & V2 TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_tests()
