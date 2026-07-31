import re
from typing import Dict, Any, List

ACTION_VERBS = {
    "developed", "engineered", "implemented", "spearheaded", "architected", "optimized",
    "designed", "built", "created", "led", "managed", "deployed", "scaled", "reduced",
    "increased", "improved", "automated", "launched", "refactored", "integrated"
}

class ATSEngine:

    @classmethod
    def evaluate(cls, raw_text: str, sections: Dict[str, str], skills: List[str]) -> Dict[str, Any]:
        text_lower = raw_text.lower()
        word_count = len(raw_text.split())

        # 1. Skill Score (max 35)
        skill_score = min(35.0, len(skills) * 3.5)

        # 2. Section Score (max 20)
        section_scores = {}
        section_weights = {
            "summary": 3.0,
            "skills": 4.0,
            "experience": 5.0,
            "education": 4.0,
            "projects": 4.0
        }
        total_section_points = 0.0
        for sec_name, weight in section_weights.items():
            content = sections.get(sec_name, "")
            if content and len(content.strip()) > 15:
                section_scores[sec_name] = weight
                total_section_points += weight
            else:
                section_scores[sec_name] = 0.0

        # 3. Word Count & Length Hygiene Score (max 15)
        if 300 <= word_count <= 1200:
            length_score = 15.0
        elif 150 <= word_count < 300 or 1200 < word_count <= 1800:
            length_score = 10.0
        else:
            length_score = 5.0

        # 4. Action Verbs & Quantifiable Metrics (max 15)
        found_verbs = [word for word in ACTION_VERBS if word in text_lower]
        metrics_matches = re.findall(r"(\b\d+%\b|\$\d+|\b\d+\s*(?:x|x-fold|percent|users|customers|k|m)\b)", text_lower)
        
        impact_score = min(10.0, len(found_verbs) * 1.5) + min(5.0, len(metrics_matches) * 1.5)

        # 5. Formatting & Contact Info Hygiene (max 15)
        contact_score = 0.0
        if re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text):
            contact_score += 5.0
        if re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", raw_text):
            contact_score += 5.0
        if "linkedin.com" in text_lower or "github.com" in text_lower:
            contact_score += 5.0

        total_score = round(skill_score + total_section_points + length_score + impact_score + contact_score, 1)
        total_score = min(100.0, total_score)

        # Rating Badge
        if total_score >= 85:
            rating = "Excellent (ATS Benchmark Passed)"
        elif total_score >= 70:
            rating = "Good (Minor Optimization Needed)"
        elif total_score >= 50:
            rating = "Average (Requires Key Improvements)"
        else:
            rating = "Needs Significant Improvement"

        # Strengths & Suggestions
        strengths = []
        suggestions = []

        if skill_score >= 25:
            strengths.append(f"Strong skill representation ({len(skills)} tech & core skills detected)")
        else:
            suggestions.append("Incorporate more industry-relevant technical & soft skills into your Skills section.")

        if section_scores.get("experience", 0) > 0:
            strengths.append("Structured Work Experience section present")
        else:
            suggestions.append("Add a clear Work Experience or Internship section with company names & dates.")

        if section_scores.get("projects", 0) > 0:
            strengths.append("Key Projects section detected")
        else:
            suggestions.append("Add a dedicated Projects section highlighting technical tools and achievements.")

        if len(metrics_matches) >= 2:
            strengths.append("Quantifiable metrics & achievements included (%, numbers, scale)")
        else:
            suggestions.append("Add measurable outcomes to bullet points (e.g., 'Improved API latency by 35%').")

        if len(found_verbs) >= 4:
            strengths.append(f"Good action verb usage ({', '.join(found_verbs[:4])})")
        else:
            suggestions.append("Start experience & project bullet points with strong action verbs (e.g., Spearheaded, Optimized, Engineered).")

        return {
            "ats_score": total_score,
            "rating": rating,
            "section_scores": {
                "skill_match": round(skill_score, 1),
                "sections_completeness": round(total_section_points, 1),
                "length_hygiene": round(length_score, 1),
                "impact_metrics": round(impact_score, 1),
                "formatting_contact": round(contact_score, 1)
            },
            "strengths": strengths,
            "suggestions": suggestions,
            "found_action_verbs": found_verbs,
            "metrics_count": len(metrics_matches)
        }
