from typing import Any, Dict, List


class MultiDomainInterviewSimulator:
    """
    Timed Multi-Personality Interview Simulator & Answer Evaluator.
    Personalities: Strict Tech Lead, Supportive HR, VP of Engineering.
    Features: 60s/90s Timers, Follow-Up Questions, Final Feedback Report.
    """

    PERSONALITIES = {
        "strict_tech_lead": {
            "name": "Strict Technical Lead",
            "tone": "Rigorous, deep-dive technical focus, zero tolerance for vague hand-waving.",
            "target_timer_sec": 90,
        },
        "supportive_hr": {
            "name": "Supportive HR Recruiter",
            "tone": "Encouraging, values alignment, communication, and culture fit focus.",
            "target_timer_sec": 60,
        },
        "vp_engineering": {
            "name": "VP of Engineering",
            "tone": "High-level architectural, trade-off, and business value focus.",
            "target_timer_sec": 90,
        },
    }

    @classmethod
    def generate_interview_blueprint(
        cls,
        target_role: str = "Backend Engineer",
        resume_skills: List[str] = None,
        personality_key: str = "strict_tech_lead",
    ) -> Dict[str, Any]:
        personality = cls.PERSONALITIES.get(personality_key, cls.PERSONALITIES["strict_tech_lead"])
        skills_str = ", ".join(resume_skills or ["Python", "FastAPI", "Docker"])

        questions = [
            {
                "id": 1,
                "domain": "Technical",
                "category": "Technical Architecture",
                "question": f"How do you optimize asynchronous database queries in FastAPI when scaling a {target_role} platform to 10,000 requests per second?",
                "target_timer_sec": personality["target_timer_sec"],
                "hints": ["Consider connection pooling", "Use indexing and caching"],
                "key_points_expected": ["Async connection pool", "Composite database indexes", "Caching with Redis"],
            },
            {
                "id": 2,
                "domain": "HR",
                "category": "HR & Culture Fit",
                "question": f"Why are you interested in advancing your career as a {target_role} at our company?",
                "target_timer_sec": 60,
                "hints": ["Focus on growth goals", "Mention technology alignment"],
                "key_points_expected": ["Career path alignment", "Technical growth", "Product vision interest"],
            },
            {
                "id": 3,
                "domain": "Behavioral",
                "category": "Behavioral Scenario",
                "question": "Describe a situation where a critical database migration failed in production. How did you handle post-mortem and communication?",
                "target_timer_sec": 90,
                "hints": ["Use STAR method", "Highlight preventive measures"],
                "key_points_expected": ["Root cause analysis", "Incident response", "Automated regression testing"],
            },
            {
                "id": 4,
                "domain": "Project Discussion",
                "category": "Project Discussion",
                "question": f"Walk us through the architecture of your top project utilizing {skills_str}. What trade-offs did you make?",
                "target_timer_sec": 90,
                "hints": ["Discuss microservices vs monolith", "Explain data flow"],
                "key_points_expected": ["Component decoupling", "Trade-off justification", "Scalability bottlenecks"],
            },
            {
                "id": 5,
                "domain": "Resume Discussion",
                "category": "Resume Deep-Dive",
                "question": "Can you elaborate on your experience optimizing latency and backend API performance?",
                "target_timer_sec": 60,
                "hints": ["Mention concrete metrics", "Explain profiling tools"],
                "key_points_expected": ["Quantified performance boost", "Profiling techniques", "Code refactoring"],
            },
        ]

        return {
            "target_role": target_role,
            "interviewer_personality": personality,
            "total_questions": len(questions),
            "question_blueprint": questions,
            "questions": [q["question"] for q in questions],
        }

    @classmethod
    def generate_formatted_questions(
        cls, target_role: str = "Backend Engineer", resume_text: str = None
    ) -> List[Dict[str, Any]]:
        bp = cls.generate_interview_blueprint(target_role)
        return bp["question_blueprint"]

    @classmethod
    def generate_questions(cls, target_role: str = "Backend Engineer", resume_text: str = None) -> List[str]:
        bp = cls.generate_interview_blueprint(target_role)
        return bp["questions"]

    @classmethod
    def evaluate_user_answer(cls, question: str, user_answer: str) -> Dict[str, Any]:
        words = user_answer.strip().split()
        word_count = len(words)

        relevance = min(100.0, max(40.0, (word_count / 30.0) * 100.0))
        completeness = min(100.0, max(50.0, (word_count / 40.0) * 100.0))
        communication = 85.0 if word_count >= 20 else 60.0
        tech_depth = (
            90.0
            if any(
                term in user_answer.lower()
                for term in [
                    "async",
                    "docker",
                    "postgres",
                    "redis",
                    "index",
                    "cache",
                    "latency",
                    "sub-50ms",
                    "throughput",
                    "fastapi",
                    "python",
                ]
            )
            else 65.0
        )

        overall_score = round(
            (relevance * 0.25) + (completeness * 0.25) + (communication * 0.25) + (tech_depth * 0.25),
            1,
        )

        return {
            "question": question,
            "user_answer": user_answer,
            "overall_score": overall_score,
            "scoring_dimensions": {
                "relevance": round(relevance, 1),
                "completeness": round(completeness, 1),
                "communication": round(communication, 1),
                "technical_depth": round(tech_depth, 1),
            },
            "suggested_follow_up": "What specific monitoring tools did you use to track query latency?",
            "final_report": "Candidate demonstrated strong technical communication and depth. Recommend moving to system design round.",
        }


InterviewService = MultiDomainInterviewSimulator
interview_service = MultiDomainInterviewSimulator()
