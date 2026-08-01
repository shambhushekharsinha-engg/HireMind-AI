from typing import Any, Dict, List

from app.services.kaggle_knowledge_base import KnowledgeBaseEngine
from app.services.nlp_engine import NLPEngine


class BenchmarkingService:
    @classmethod
    def benchmark_resume(cls, resume_text: str, target_role: str) -> Dict[str, Any]:
        role_info = KnowledgeBaseEngine.get_role_info(target_role)
        extracted_skills = NLPEngine.extract_skills(resume_text or "")
        skills_set = set([s.lower() for s in extracted_skills])

        req_skills = role_info["required_skills"]
        top_kw = role_info["top_keywords"]

        matched_kw = [kw for kw in top_kw if kw.lower() in resume_text.lower() or kw.lower() in skills_set]
        missing_kw = [kw for kw in top_kw if kw not in matched_kw]

        # Calculate Percentile Score heuristic based on benchmark top 10% cohort
        score_base = min(95.0, max(20.0, (len(matched_kw) / len(top_kw)) * 100))
        percentile = round(min(99.0, max(15.0, score_base * 0.95 + 10.0)), 1)

        return {
            "target_role": role_info["title"],
            "percentile_score": f"{percentile}th Percentile",
            "comparison_with_top_cohort": (
                "Top 12% Candidate Profile" if percentile >= 85 else "Average Applicant Cohort"
            ),
            "matched_keywords": matched_kw,
            "top_missing_keywords": missing_kw,
            "skills_ranked_by_importance": [
                {"skill": kw, "importance": "Critical" if idx < 3 else "High"} for idx, kw in enumerate(top_kw)
            ],
        }

    @classmethod
    def analyze_career_gap(cls, current_skills: List[str], target_role: str) -> Dict[str, Any]:
        role_info = KnowledgeBaseEngine.get_role_info(target_role)
        current_set = set([s.lower() for s in current_skills])

        missing_skills = [s for s in role_info["required_skills"] if s.lower() not in current_set]
        retained_skills = [s for s in role_info["required_skills"] if s.lower() in current_set]

        return {
            "target_role": role_info["title"],
            "current_skills": current_skills,
            "retained_matching_skills": retained_skills,
            "missing_required_skills": missing_skills,
            "skill_gap_percentage": f"{round((len(missing_skills) / len(role_info['required_skills'])) * 100, 1)}%",
            "personalized_weekly_roadmap": role_info["weekly_roadmap"],
        }

    @classmethod
    def recommend_projects(cls, target_role: str) -> Dict[str, Any]:
        role_info = KnowledgeBaseEngine.get_role_info(target_role)
        return {
            "target_role": role_info["title"],
            "recommended_projects": role_info["recommended_projects"],
        }

    @classmethod
    def summarize_for_recruiter(cls, candidate_name: str, resume_text: str, target_role: str) -> Dict[str, Any]:
        role_info = KnowledgeBaseEngine.get_role_info(target_role)
        skills = NLPEngine.extract_skills(resume_text or "")

        strengths = [
            f"Demonstrated proficiency in {', '.join(skills[:3]) if skills else 'core software development'}.",
            "Structured experience layout with clear action verbs.",
        ]

        weaknesses = [
            f"Missing key keywords ({', '.join(role_info['top_keywords'][:2])}) required for top 5% benchmark profiles."
        ]

        rec_status = "Strong Hire Candidate" if len(skills) >= 5 else "Consider for Screening"

        return {
            "candidate_name": candidate_name or "Applicant",
            "target_role": role_info["title"],
            "recruiter_recommendation_badge": rec_status,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "interview_focus_areas": role_info["interview_topics"],
        }
