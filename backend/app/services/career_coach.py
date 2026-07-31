from typing import Dict, Any

class CareerCoachService:

    @classmethod
    def ask_coach(cls, question: str) -> Dict[str, Any]:
        q_lower = question.lower()

        if "ml engineer" in q_lower or "machine learning" in q_lower:
            answer = "To become an ML Engineer, master Python, SQL, and linear algebra first. Then build proficiency in PyTorch/TensorFlow, Docker, and FastAPI for model serving. Work on end-to-end projects like real-time anomaly detection or sentiment analysis APIs."
            followups = ["What projects should I build for ML?", "What certifications do top ML companies look for?"]
            resources = ["DeepLearning.AI Specialization", "FastAPI + PyTorch Deployment Guide"]

        elif "ats" in q_lower or "score" in q_lower:
            answer = "ATS scores depend on 5 key factors: 1) Relevant technical skills match, 2) Complete section headers (Summary, Skills, Experience, Education, Projects), 3) Standard 300-1000 word length, 4) Quantifiable metrics in bullet points, and 5) Clean formatting without tables or graphics."
            followups = ["How to write action-verb bullet points?", "Check my resume against a job description."]
            resources = ["HireMind AI Resume Rewriter", "ATS Formatting Hygiene Checklist"]

        elif "project" in q_lower or "portfolio" in q_lower:
            answer = "Top recommended projects for software candidates: 1) Full-Stack SaaS application with OAuth & Payments, 2) Microservice REST API with Docker & CI/CD, 3) AI-powered RAG document search interface, 4) Real-Time WebSocket dashboard."
            followups = ["How do I list open-source contributions on my resume?", "What full-stack tech stack should I choose?"]
            resources = ["GitHub Open-Source Good First Issues", "Full-Stack Portfolio Template"]

        else:
            answer = f"Great question! Focusing on continuous skill acquisition, tailoring your resume with measurable achievements (XYZ formula: Accomplished X by Y using Z), and practicing mock interview questions will significantly increase your callback rate."
            followups = ["What skills are in highest demand for 2026?", "How can I improve my interview performance?"]
            resources = ["HireMind AI Skill Gap Engine", "Mock Interview Simulator"]

        return {
            "answer": answer,
            "suggested_followups": followups,
            "recommended_resources": resources
        }
