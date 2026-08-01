from typing import Any, Dict

COMPANY_DATABASE = {
    "microsoft": {
        "company_name": "Microsoft",
        "role": "Software Development Engineer (SDE)",
        "interview_difficulty": "Hard (4.1 / 5.0)",
        "expected_skills": ["C#", "C++", "Python", "Data Structures", "System Design", "Azure"],
        "salary_range": "$135,000 - $185,000 / year",
        "hiring_trends": "Strong demand for Cloud (Azure), AI Integration, and Distributed Microservices.",
        "interview_rounds": [
            "Online Assessment: 2 LeetCode Medium/Hard Problem Solving",
            "Round 1: Data Structures & Algorithms (Trees, Graphs, Dynamic Programming)",
            "Round 2: Low-Level Design (Object Oriented Design & Clean Code)",
            "Round 3: High-Level System Design (Scalability, Caching, DB Partitioning)",
            "Round 4: As-Appropriate (AA) Interview (Culture, Past Projects & System Leadership)",
        ],
    },
    "google": {
        "company_name": "Google",
        "role": "Software Engineer (SWE)",
        "interview_difficulty": "Very Hard (4.6 / 5.0)",
        "expected_skills": ["C++", "Python", "Java", "Algorithms", "Distributed Systems", "GCP"],
        "salary_range": "$145,000 - $210,000 / year",
        "hiring_trends": "Aggressive recruitment for ML Infra, Search AI, and Cloud Platform.",
        "interview_rounds": [
            "Technical Phone Screen: 45-min Algorithmic Problem Solving",
            "Onsite 1-3: Advanced Algorithms, Graph Traversals & Optimization",
            "Onsite 4: System Design & Distributed Data Storage",
            "Googleyness: Leadership, Ambiguity & Behavioral Scenarios",
        ],
    },
    "amazon": {
        "company_name": "Amazon",
        "role": "Software Development Engineer (SDE I/II)",
        "interview_difficulty": "Hard (4.2 / 5.0)",
        "expected_skills": ["Java", "Python", "AWS", "Object Oriented Design", "REST APIs"],
        "salary_range": "$130,000 - $175,000 / year",
        "hiring_trends": "Continuous hiring for AWS Infrastructure and E-Commerce Logistics.",
        "interview_rounds": [
            "Online Assessment: Debugging + 2 Coding Questions + Work Simulation",
            "Onsite Technical: Object Oriented Design + Data Structures",
            "Leadership Principles: 16 Leadership Principles Behavioral Deep-Dive",
        ],
    },
}


class CompanyInsightsService:
    @classmethod
    def get_company_blueprint(cls, target: str) -> Dict[str, Any]:
        key = target.lower().strip()
        for comp_key, data in COMPANY_DATABASE.items():
            if comp_key in key:
                return data

        # Fallback default blueprint
        return {
            "company_name": target.title(),
            "role": "Software Engineer",
            "interview_difficulty": "Moderate to Hard (3.8 / 5.0)",
            "expected_skills": [
                "Python",
                "JavaScript",
                "SQL",
                "Data Structures",
                "System Design",
                "Git",
            ],
            "salary_range": "$100,000 - $150,000 / year",
            "hiring_trends": "High demand for Full-Stack development and Cloud Microservices.",
            "interview_rounds": [
                "Round 1: Coding & Data Structures Screening",
                "Round 2: System Design & Architecture Review",
                "Round 3: Past Experience & Cultural Fit Interview",
            ],
        }
