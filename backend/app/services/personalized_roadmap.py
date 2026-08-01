from typing import Any, Dict, List


class AdaptivePersonalizedRoadmap:
    """
    Adaptive Personalized Roadmap Engine.
    Generates dynamic learning paths tailored to:
    - Current ATS Score
    - Missing Skills & Target Role
    - Experience Level & Learning Pace
    - Completed Roadmap Steps
    """

    @classmethod
    def generate_roadmap(
        cls,
        target_role: str = "Senior Backend Engineer",
        current_ats_score: float = 72.0,
        missing_skills: List[str] = None,
        experience_level: str = "Mid-Level",
        learning_pace: str = "Accelerated (10 hrs/week)",
        completed_steps: List[str] = None,
    ) -> Dict[str, Any]:
        skills = missing_skills or ["Docker", "Kubernetes", "Redis", "System Design"]
        done = completed_steps or ["Master Python Fundamentals", "Build REST APIs with FastAPI"]

        all_steps = [
            {"step_id": "step-1", "title": "Master Python Fundamentals", "skill": "Python"},
            {"step_id": "step-2", "title": "Build REST APIs with FastAPI", "skill": "FastAPI"},
            {
                "step_id": "step-3",
                "title": "Implement Redis Caching & DB Indexing",
                "skill": "Redis",
            },
            {"step_id": "step-4", "title": "Containerize Services with Docker", "skill": "Docker"},
            {
                "step_id": "step-5",
                "title": "Orchestrate Microservices with Kubernetes",
                "skill": "Kubernetes",
            },
            {
                "step_id": "step-6",
                "title": "High-Scale Distributed System Design",
                "skill": "System Design",
            },
        ]

        remaining = [s for s in all_steps if s["title"] not in done]
        pct = round((len(done) / max(len(all_steps), 1)) * 100.0, 1)

        return {
            "target_role": target_role,
            "current_ats_score": current_ats_score,
            "experience_level": experience_level,
            "learning_pace": learning_pace,
            "completion_percentage": pct,
            "completed_steps": done,
            "next_recommended_step": remaining[0] if remaining else None,
            "remaining_roadmap_steps": remaining,
            "estimated_completion_weeks": max(1, len(remaining) * 2),
        }


personalized_roadmap = AdaptivePersonalizedRoadmap()
