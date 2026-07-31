from typing import Dict, Any, List
from app.services.nlp_engine import NLPEngine

INTERVIEW_QUESTION_BANK = {
    "AI / Machine Learning Engineer": [
        {
            "id": 1,
            "category": "Technical",
            "question": "Explain the difference between overfitting and underfitting in ML, and how do you mitigate both?",
            "hints": ["Talk about model complexity, regularization (L1/L2), cross-validation, and training data size."],
            "key_points_expected": ["overfitting", "underfitting", "regularization", "cross validation", "data augmentation"]
        },
        {
            "id": 2,
            "category": "Technical",
            "question": "How does the Attention Mechanism work in Transformer architectures?",
            "hints": ["Mention Query, Key, Value vectors, Softmax normalization, and Self-Attention."],
            "key_points_expected": ["query", "key", "value", "softmax", "self attention", "transformer"]
        },
        {
            "id": 3,
            "category": "Project-based",
            "question": "Walk me through an ML model you deployed to production. How did you handle latency and model drift?",
            "hints": ["Highlight API wrapper (FastAPI/Flask), Docker containerization, caching, and model monitoring."],
            "key_points_expected": ["fastapi", "docker", "latency", "monitoring", "metrics", "deployment"]
        },
        {
            "id": 4,
            "category": "Behavioral",
            "question": "Describe a scenario where your machine learning model performed poorly in production. How did you troubleshoot it?",
            "hints": ["Use STAR method (Situation, Task, Action, Result). Focus on data quality and debugging."],
            "key_points_expected": ["data drift", "debugging", "validation", "collaboration", "resolution"]
        }
    ],
    "Full-Stack Web Developer": [
        {
            "id": 1,
            "category": "Technical",
            "question": "How does the Virtual DOM work in React, and how does React optimize re-renders?",
            "hints": ["Mention reconciliation algorithm, diffing, useMemo, and useCallback."],
            "key_points_expected": ["virtual dom", "diffing", "reconciliation", "state", "usememo", "usecallback"]
        },
        {
            "id": 2,
            "category": "Technical",
            "question": "Explain how CORS (Cross-Origin Resource Sharing) works and how to resolve CORS errors in FastAPI/Express.",
            "hints": ["Explain browser security policy, preflight OPTIONS requests, and middleware configuration."],
            "key_points_expected": ["origin", "preflight", "headers", "middleware", "security"]
        },
        {
            "id": 3,
            "category": "System Design",
            "question": "How would you design a scalable authentication system using JWT and Refresh Tokens?",
            "hints": ["Explain token storage (HttpOnly cookies), access token expiration, and database session revoking."],
            "key_points_expected": ["jwt", "httponly", "refresh token", "access token", "security", "database"]
        },
        {
            "id": 4,
            "category": "HR / Behavioral",
            "question": "Why do you want to join our engineering team, and what is your approach to handling tight project deadlines?",
            "hints": ["Focus on task prioritization, agile sprints, clear team communication, and pragmatic trade-offs."],
            "key_points_expected": ["prioritization", "communication", "agile", "problem solving", "ownership"]
        }
    ]
}

DEFAULT_QUESTIONS = [
    {
        "id": 1,
        "category": "Technical",
        "question": "Explain the architectural flow of a web request from client browser to backend database.",
        "hints": ["Mention DNS lookup, HTTP request, load balancer, API router, ORM, and database query."],
        "key_points_expected": ["dns", "http", "api", "orm", "database", "json"]
    },
    {
        "id": 2,
        "category": "Project-based",
        "question": "Describe the most challenging technical project listed on your resume. What key engineering decisions did you make?",
        "hints": ["Highlight your personal contribution, technologies used, trade-offs, and final impact."],
        "key_points_expected": ["architecture", "technologies", "challenge", "optimization", "result"]
    },
    {
        "id": 3,
        "category": "Behavioral",
        "question": "Give an example of a conflict or technical disagreement you had with a team member and how you resolved it.",
        "hints": ["Use STAR method. Emphasize data-driven decision making, listening, and respectful consensus."],
        "key_points_expected": ["communication", "collaboration", "data driven", "resolution", "teamwork"]
    }
]

class InterviewService:

    @classmethod
    def generate_questions(cls, target_role: str, resume_text: str = None) -> List[Dict[str, Any]]:
        questions = INTERVIEW_QUESTION_BANK.get(target_role, DEFAULT_QUESTIONS)
        
        # Customize hints based on extracted resume skills if present
        if resume_text:
            skills = NLPEngine.extract_skills(resume_text)
            if skills:
                custom_q = {
                    "id": len(questions) + 1,
                    "category": "Resume Specific",
                    "question": f"I noticed skills like {', '.join(skills[:3])} on your resume. How have you applied these together in a real project?",
                    "hints": [f"Focus specifically on your practical experience with {skills[0]} and {skills[1]}."],
                    "key_points_expected": [s.lower() for s in skills[:4]]
                }
                questions = list(questions) + [custom_q]

        return questions

    @classmethod
    def evaluate_answer(cls, question: str, user_answer: str, expected_points: List[str] = None) -> Dict[str, Any]:
        if not user_answer or len(user_answer.strip()) < 10:
            return {
                "score": 20.0,
                "feedback": "Your answer is very short. Provide more technical detail, context, and examples.",
                "strengths": [],
                "improvements": ["Elaborate with specific technical concepts and practical examples."]
            }

        answer_lower = user_answer.lower()
        matched_points = []
        missing_points = []

        if expected_points:
            for pt in expected_points:
                if pt.lower() in answer_lower:
                    matched_points.append(pt)
                else:
                    missing_points.append(pt)
            
            coverage = len(matched_points) / len(expected_points)
        else:
            coverage = 0.7 if len(user_answer.split()) > 40 else 0.4

        # Score calculation (word count quality + expected point coverage)
        word_count = len(user_answer.split())
        length_factor = min(1.0, word_count / 50.0)
        
        score = round((0.7 * coverage + 0.3 * length_factor) * 100.0, 1)
        score = min(100.0, max(15.0, score))

        strengths = []
        improvements = []

        if matched_points:
            strengths.append(f"Good technical coverage of key terms: {', '.join(matched_points)}.")
        if word_count > 40:
            strengths.append("Clear detail and depth in response length.")

        if missing_points:
            improvements.append(f"Consider addressing these core concepts in your answer: {', '.join(missing_points[:4])}.")
        if word_count < 30:
            improvements.append("Use the STAR technique (Situation, Task, Action, Result) to structure a longer, impactful response.")

        return {
            "score": score,
            "feedback": "Strong effort! " + ("Good coverage of technical details." if score >= 70 else "Include more specific architectural details and outcomes."),
            "strengths": strengths if strengths else ["Clear communication"],
            "improvements": improvements if improvements else ["Keep practicing with real project metrics."]
        }
