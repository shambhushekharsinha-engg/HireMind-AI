from typing import Any, Dict

from app.services.nlp_engine import NLPEngine


class LinkedInService:
    @classmethod
    def optimize_profile(cls, headline: str, summary: str, target_role: str = "Software Engineer") -> Dict[str, Any]:
        extracted_skills = NLPEngine.extract_skills(f"{headline} {summary}")

        # Headline Optimizer Score
        headline_length = len(headline.strip())
        headline_score = min(100.0, (headline_length / 100.0) * 100.0) if headline else 30.0

        suggested_headlines = [
            f"{target_role} | {', '.join(extracted_skills[:3]).title() if extracted_skills else 'Python, React, Cloud'} | Building High-Throughput Scalable Systems",
            f"Passionate {target_role} @ Tech | Ex-Intern | Specializing in {extracted_skills[0] if extracted_skills else 'Full-Stack'} & AI Automation",
            f"{target_role} | Open to Opportunities | {', '.join(extracted_skills[:2]).title() if extracted_skills else 'Software Engineering'} Specialist",
        ]

        summary_suggestions = []
        if len(summary.split()) < 50:
            summary_suggestions.append(
                "Expand your About section to at least 100-150 words highlighting key engineering achievements and core tech stack."
            )
        if "contact" not in summary.lower() and "email" not in summary.lower():
            summary_suggestions.append(
                "Add a clear Call-to-Action with your email or portfolio link at the end of your About section."
            )
        if not extracted_skills:
            summary_suggestions.append(
                "Include explicit technology keyword tags (e.g. #Python #React #Docker) for recruiter search SEO."
            )

        return {
            "headline_seo_score": round(headline_score, 1),
            "detected_keywords": extracted_skills,
            "suggested_headlines": suggested_headlines,
            "summary_improvements": summary_suggestions
            if summary_suggestions
            else ["Great About summary structure! Keep skills updated."],
            "recruiter_searchability_rating": "High SEO Visibility"
            if headline_score >= 70
            else "Medium SEO Visibility",
        }
