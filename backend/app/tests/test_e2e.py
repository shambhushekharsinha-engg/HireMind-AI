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

    print("\n--- 2. Testing OTP Generation & Verification ---")
    gen_res = requests.post(f"{BASE_V1}/auth/generate-otp", json={"mobile_number": "+919876543299"})
    print("Generate OTP Output:", gen_res.json())
    assert gen_res.status_code == 200
    assert gen_res.json()["demo_otp"] == "123456"

    verify_res = requests.post(
        f"{BASE_V1}/auth/verify-otp",
        json={"mobile_number": "+919876543299", "otp_code": "123456", "role": "recruiter"},
    )
    print("Verify OTP Token Output:", verify_res.json()["user"])
    assert verify_res.status_code == 200
    assert verify_res.json()["user"]["role"] == "recruiter"

    print("\n--- 3. Testing Forgot Password & Reset Password ---")
    forgot_res = requests.post(f"{BASE_V1}/auth/forgot-password", json={"email": "alex.student@hiremind.ai"})
    print("Forgot Password Output:", forgot_res.json())
    assert forgot_res.status_code == 200

    reset_res = requests.post(
        f"{BASE_V1}/auth/reset-password",
        json={
            "email": "alex.student@hiremind.ai",
            "reset_code": "998877",
            "new_password": "newpassword123",
        },
    )
    print("Reset Password Output:", reset_res.json())
    assert reset_res.status_code == 200

    email_ver_res = requests.post(
        f"{BASE_V1}/auth/verify-email",
        json={"email": "alex.student@hiremind.ai", "verification_code": "123456"},
    )
    print("Email Verification Output:", email_ver_res.json())
    assert email_ver_res.status_code == 200

    print("\n--- 4. Testing API v2 AI Resume Benchmarking ---")
    bench_req = {
        "resume_text": "Python SQL Pandas Scikit-Learn Docker Machine Learning",
        "target_role": "Machine Learning Engineer",
    }
    res_bench = requests.post(f"{BASE_V2}/ai/benchmark", json=bench_req)
    print(
        "Percentile Score:",
        res_bench.json()["percentile_score"],
        "| Cohort:",
        res_bench.json()["comparison_with_top_cohort"],
    )
    assert res_bench.status_code == 200

    print("\n--- ALL ENTERPRISE AUDIT & FEATURE TESTS PASSED SUCCESSFULLY! ---")


if __name__ == "__main__":
    run_tests()
