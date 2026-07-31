from typing import Dict, Any, List
from app.services.nlp_engine import NLPEngine

ROLE_DATABASE = {
    "AI / Machine Learning Engineer": {
        "required_skills": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "sql"],
        "salary_range": "$95,000 - $160,000 / year",
        "certifications": ["AWS Certified Machine Learning - Specialty", "TensorFlow Developer Certificate", "DeepLearning.AI Specialization"],
        "projects": ["End-to-End Image Classification Pipeline", "NLP Sentiment & Summarization API", "Real-Time Fraud Detection Model"]
    },
    "Full-Stack Web Developer": {
        "required_skills": ["react", "javascript", "typescript", "node.js", "fastapi", "html", "css", "postgresql", "git"],
        "salary_range": "$85,000 - $140,000 / year",
        "certifications": ["Meta Front-End / Back-End Developer Certificate", "AWS Certified Developer - Associate"],
        "projects": ["SaaS Application with Auth & Billing", "Real-Time Chat App with WebSockets", "E-Commerce Dashboard"]
    },
    "Backend Engineer": {
        "required_skills": ["python", "java", "fastapi", "django", "postgresql", "redis", "docker", "rest api", "git"],
        "salary_range": "$90,000 - $150,000 / year",
        "certifications": ["CKAD: Certified Kubernetes Application Developer", "AWS Solution Architect Associate"],
        "projects": ["High-Throughput Microservice Architecture", "Distributed Caching & Task Queue Engine", "REST API with JWT Auth"]
    },
    "Data Scientist / Data Analyst": {
        "required_skills": ["python", "sql", "pandas", "numpy", "matplotlib", "seaborn", "data analysis", "r"],
        "salary_range": "$80,000 - $135,000 / year",
        "certifications": ["Google Data Analytics Professional Certificate", "IBM Data Science Professional Certificate"],
        "projects": ["Customer Churn Predictive Modeling", "Interactive Business Intelligence Dashboard", "Exploratory Data Analysis Report"]
    },
    "DevOps / Cloud Engineer": {
        "required_skills": ["aws", "docker", "kubernetes", "linux", "terraform", "ci/cd", "python", "bash"],
        "salary_range": "$95,000 - $155,000 / year",
        "certifications": ["AWS Certified Solutions Architect", "Docker Certified Associate", "HashiCorp Certified Terraform Associate"],
        "projects": ["Automated CI/CD Pipeline with GitHub Actions", "Infrastructure as Code with Terraform & AWS", "Kubernetes Cluster Deployment"]
    }
}

class CareerService:

    @classmethod
    def generate_roadmap(cls, resume_text: str, target_role: str = None) -> Dict[str, Any]:
        skills = set(NLPEngine.extract_skills(resume_text or ""))

        # If no target role specified, auto-predict best role fit
        recommended_roles = []
        best_role = "Full-Stack Web Developer"
        highest_match_count = 0

        for role_name, info in ROLE_DATABASE.items():
            match_count = len(skills.intersection(set(info["required_skills"])))
            if match_count > 0:
                recommended_roles.append(role_name)
            if match_count > highest_match_count:
                highest_match_count = match_count
                best_role = role_name

        if not target_role or target_role not in ROLE_DATABASE:
            target_role = best_role

        role_info = ROLE_DATABASE.get(target_role, ROLE_DATABASE["Full-Stack Web Developer"])
        required_skills = set(role_info["required_skills"])
        acquired_skills = skills.intersection(required_skills)
        skill_gaps = list(required_skills.difference(acquired_skills))

        # Generate 4-Step Structured Learning Roadmap
        roadmap = [
            {
                "step": 1,
                "title": "Phase 1: Core Fundamentals & Language Mastery",
                "duration": "4 - 6 Weeks",
                "focus": f"Master fundamental tools and syntax required for {target_role}.",
                "key_skills": list(required_skills)[:3],
                "recommended_projects": [role_info["projects"][0]],
                "recommended_certifications": [role_info["certifications"][0]]
            },
            {
                "step": 2,
                "title": "Phase 2: Frameworks, Libraries & System Architecture",
                "duration": "6 - 8 Weeks",
                "focus": "Build production-ready components and understand backend/data architectures.",
                "key_skills": skill_gaps[:2] if skill_gaps else list(required_skills)[3:5],
                "recommended_projects": [role_info["projects"][1]],
                "recommended_certifications": [role_info["certifications"][-1]]
            },
            {
                "step": 3,
                "title": "Phase 3: Real-World Portfolio Project & Deployment",
                "duration": "4 - 6 Weeks",
                "focus": "Develop an end-to-end full-stack application and deploy it publicly on Cloud (AWS/Vercel/Render).",
                "key_skills": ["Git", "Docker", "CI/CD", "Testing"],
                "recommended_projects": [role_info["projects"][-1]],
                "recommended_certifications": ["Git & GitHub Certification"]
            },
            {
                "step": 4,
                "title": "Phase 4: Resume Optimization & Technical Interview Prep",
                "duration": "2 - 3 Weeks",
                "focus": "Tailor resume bullet points with metrics, practice coding interviews, and apply for roles.",
                "key_skills": ["System Design", "Behavioral Interview", "LeetCode / Problem Solving"],
                "recommended_projects": ["Open Source Contribution"],
                "recommended_certifications": ["HireMind AI Career Readiness Badge"]
            }
        ]

        return {
            "target_role": target_role,
            "recommended_roles": recommended_roles if recommended_roles else list(ROLE_DATABASE.keys())[:3],
            "skill_gaps": skill_gaps,
            "estimated_salary": {
                "range": role_info["salary_range"],
                "growth_projection": "+18% Annual Demand Growth"
            },
            "roadmap": roadmap
        }
