from typing import Any, Dict, List

# Industry-Grade Multi-Domain Taxonomy Matrix (Inspired by Kaggle 25+ Category IT & Engineering Datasets)
INDUSTRY_FIELDS_TAXONOMY = {
    "software_engineering": {
        "domain_name": "Software Engineering & Architecture",
        "core_skills": [
            "Python",
            "Java",
            "C++",
            "C#",
            "Go",
            "Rust",
            "System Design",
            "Microservices",
            "REST API",
            "GraphQL",
            "Data Structures",
            "Algorithms",
            "Git",
        ],
        "benchmark_ats_weight": 0.35,
    },
    "data_science_ai": {
        "domain_name": "Data Science, Machine Learning & AI",
        "core_skills": [
            "Python",
            "PyTorch",
            "TensorFlow",
            "Scikit-Learn",
            "Pandas",
            "NumPy",
            "NLP",
            "Computer Vision",
            "LLMs",
            "RAG",
            "SQL",
            "Spark",
            "MLOps",
        ],
        "benchmark_ats_weight": 0.40,
    },
    "cloud_devops": {
        "domain_name": "Cloud Engineering, DevOps & SRE",
        "core_skills": [
            "AWS",
            "Azure",
            "GCP",
            "Docker",
            "Kubernetes",
            "Terraform",
            "Ansible",
            "CI/CD",
            "Linux",
            "Bash",
            "Prometheus",
            "Grafana",
            "Networking",
        ],
        "benchmark_ats_weight": 0.38,
    },
    "cybersecurity": {
        "domain_name": "Cybersecurity & InfoSec",
        "core_skills": [
            "Penetration Testing",
            "Ethical Hacking",
            "SIEM",
            "Wireshark",
            "Network Security",
            "Cryptography",
            "SOC",
            "OWASP",
            "Firewalls",
            "Incident Response",
        ],
        "benchmark_ats_weight": 0.36,
    },
    "mobile_development": {
        "domain_name": "Mobile Application Engineering",
        "core_skills": [
            "React Native",
            "Flutter",
            "Swift",
            "Kotlin",
            "Android SDK",
            "iOS Development",
            "Mobile UI/UX",
            "SQLite",
            "Firebase",
            "App Store Deployment",
        ],
        "benchmark_ats_weight": 0.35,
    },
    "fintech_hft": {
        "domain_name": "Quantitative Finance & High-Frequency Trading",
        "core_skills": [
            "C++",
            "Python",
            "Quantitative Modeling",
            "Low-Latency Systems",
            "Financial Engineering",
            "SQL",
            "Risk Analysis",
            "Multithreading",
            "Order Execution",
        ],
        "benchmark_ats_weight": 0.42,
    },
    "product_management": {
        "domain_name": "Technical Product Management & Analytics",
        "core_skills": [
            "Product Roadmap",
            "Agile/Scrum",
            "User Stories",
            "A/B Testing",
            "Mixpanel",
            "Jira",
            "SQL",
            "Product Analytics",
            "Market Research",
            "Stakeholder Management",
        ],
        "benchmark_ats_weight": 0.32,
    },
}


class KaggleDatasetEngine:
    @classmethod
    def detect_industry_field(cls, resume_skills: List[str], text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        skills_set = set([s.lower() for s in resume_skills])

        domain_scores = {}
        for domain_key, domain_info in INDUSTRY_FIELDS_TAXONOMY.items():
            matched_count = 0
            for skill in domain_info["core_skills"]:
                if skill.lower() in skills_set or skill.lower() in text_lower:
                    matched_count += 1
            domain_scores[domain_key] = matched_count

        # Pick primary domain
        best_domain_key = max(domain_scores, key=domain_scores.get)
        best_domain = INDUSTRY_FIELDS_TAXONOMY[best_domain_key]
        matched_skills = [s for s in best_domain["core_skills"] if s.lower() in skills_set or s.lower() in text_lower]

        return {
            "primary_industry_field": best_domain["domain_name"],
            "field_code": best_domain_key,
            "detected_domain_skills": matched_skills,
            "domain_coverage_percentage": round((len(matched_skills) / len(best_domain["core_skills"])) * 100, 1),
            "benchmark_dataset_reference": "Kaggle 25-Category IT & Engineering Benchmark v3.0",
        }
