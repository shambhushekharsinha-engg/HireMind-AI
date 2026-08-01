import re
from typing import Any, Dict, List

from app.services.kaggle_dataset_engine import KaggleDatasetEngine

ACTION_VERBS = {
    "developed",
    "engineered",
    "implemented",
    "spearheaded",
    "architected",
    "optimized",
    "designed",
    "built",
    "created",
    "led",
    "managed",
    "deployed",
    "scaled",
    "reduced",
    "increased",
    "improved",
    "automated",
    "launched",
    "refactored",
    "integrated",
}


class ATSEngine:
    @classmethod
    def evaluate(cls, raw_text: str, sections: Dict[str, str], skills: List[str]) -> Dict[str, Any]:
        text_lower = raw_text.lower()
        words = raw_text.split()
        word_count = len(words)

        # Industry Domain Taxonomy
        industry_info = KaggleDatasetEngine.detect_industry_field(skills, raw_text)

        # 1. Skill Score (Max 35.0) — Weighted by skill density
        skill_score = min(35.0, len(skills) * 3.5)

        # 2. Section Completeness Score (Max 20.0)
        section_weights = {
            "summary": 3.0,
            "skills": 4.0,
            "experience": 5.0,
            "education": 4.0,
            "projects": 4.0,
        }
        section_scores = {}
        total_section_points = 0.0
        for sec_name, weight in section_weights.items():
            content = sections.get(sec_name, "")
            if content and len(content.strip()) > 15:
                section_scores[sec_name] = weight
                total_section_points += weight
            else:
                section_scores[sec_name] = 0.0

        # 3. Length Hygiene Score (Max 15.0) — Smooth continuous interpolation
        # Optimal word count window: 350 to 900 words
        if 350 <= word_count <= 900:
            length_score = 15.0
        else:
            deviation = abs(word_count - 625)
            length_score = max(5.0, 15.0 - (deviation * 0.012))

        # 4. Action Verbs & Metrics Score (Max 15.0)
        found_verbs = [word for word in ACTION_VERBS if word in text_lower]
        metrics_matches = re.findall(r"(\b\d+%\b|\$\d+|\b\d+\s*(?:x|x-fold|percent|users|customers|k|m)\b)", text_lower)
        impact_score = min(10.0, len(found_verbs) * 1.5) + min(5.0, len(metrics_matches) * 1.5)

        # 5. Formatting & Contact Hygiene (Max 15.0)
        contact_score = 0.0
        if re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text):
            contact_score += 5.0
        if re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", raw_text):
            contact_score += 5.0
        if "linkedin.com" in text_lower or "github.com" in text_lower:
            contact_score += 5.0

        # Weighted Sum -> Clamp -> Smooth Interpolation
        raw_total = skill_score + total_section_points + length_score + impact_score + contact_score
        clamped_score = min(100.0, max(0.0, raw_total))
        total_score = round(clamped_score, 1)

        # Transparent Rating Badges
        if total_score >= 85:
            rating = "Excellent (ATS Optimization Passed)"
        elif total_score >= 70:
            rating = "Good (Minor Keyword Optimizations Recommended)"
        elif total_score >= 50:
            rating = "Average (Requires Key Improvements)"
        else:
            rating = "Needs Significant Improvement"

        # Explainable Sub-score Dashboard
        subscore_breakdown = {
            "formatting_hygiene": {
                "score": round(contact_score + length_score, 1),
                "max": 30.0,
                "label": "Formatting & Contact Hygiene",
            },
            "projects_impact": {
                "score": round(section_scores.get("projects", 0.0) + (min(5.0, len(metrics_matches) * 1.5)), 1),
                "max": 9.0,
                "label": "Projects & Quantified Results",
            },
            "experience_verbs": {
                "score": round(section_scores.get("experience", 0.0) + (min(10.0, len(found_verbs) * 1.5)), 1),
                "max": 15.0,
                "label": "Work Experience & Action Verbs",
            },
            "skills_match": {
                "score": round(skill_score, 1),
                "max": 35.0,
                "label": "Technical & Core Skill Match",
            },
        }

        # Strengths & Suggestions
        strengths = []
        suggestions = []

        if skill_score >= 25:
            strengths.append(
                f"Strong skill representation ({len(skills)} skills detected for {industry_info['primary_industry_field']})"
            )
        else:
            suggestions.append(
                f"Incorporate more domain-specific skills relevant to {industry_info['primary_industry_field']}."
            )

        if section_scores.get("experience", 0) > 0:
            strengths.append("Structured Work Experience section detected")
        else:
            suggestions.append("Add a dedicated Work Experience section with clear company names and timelines.")

        if len(metrics_matches) >= 2:
            strengths.append("Quantifiable metrics included (percentages, scale, dollar values)")
        else:
            suggestions.append("Add measurable outcomes to experience points (e.g. 'Reduced latency by 40%').")

        if len(found_verbs) >= 4:
            strengths.append(f"Good action verb density ({', '.join(found_verbs[:4])})")
        else:
            suggestions.append("Begin bullet points with strong action verbs (Spearheaded, Engineered, Optimized).")

        return {
            "ats_score": total_score,
            "rating": rating,
            "industry_classification": industry_info,
            "section_scores": {
                "skill_match": round(skill_score, 1),
                "sections_completeness": round(total_section_points, 1),
                "length_hygiene": round(length_score, 1),
                "impact_metrics": round(impact_score, 1),
                "formatting_contact": round(contact_score, 1),
            },
            "explainable_breakdown": subscore_breakdown,
            "strengths": strengths,
            "suggestions": suggestions,
            "found_action_verbs": found_verbs,
            "metrics_count": len(metrics_matches),
        }
