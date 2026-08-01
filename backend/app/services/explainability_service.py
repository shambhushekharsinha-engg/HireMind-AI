from typing import Any, Dict


class ExplainabilityService:
    """
    Explainability Layer for AI Recommendations.
    Attaches empirical justification and data-driven reasons to recommendations.
    """

    @staticmethod
    def explain_skill_recommendation(skill_name: str, occurrences_pct: float = 72.0) -> Dict[str, Any]:
        return {
            "recommendation": f"Acquire proficiency in {skill_name}",
            "reason": f"Appears in {occurrences_pct}% of matching target job postings.",
            "impact_score": "High",
            "suggested_action": f"Complete a hands-on project demonstrating {skill_name} deployment.",
        }

    @staticmethod
    def explain_bullet_rewrite(
        original_bullet: str, reason: str = "Lacks quantifiable metrics and strong action verbs"
    ) -> Dict[str, Any]:
        return {
            "original_bullet": original_bullet,
            "reason": reason,
            "suggested_enhancement": "Incorporate numerical outcomes ($/%) and strong action verbs like Spearheaded or Architected.",
        }


explainability_service = ExplainabilityService()
