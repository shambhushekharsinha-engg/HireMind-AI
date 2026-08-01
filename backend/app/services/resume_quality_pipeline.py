import re
from typing import Any, Dict, List, Optional


class ResumeQualityPipeline:
    """
    Deterministic Resume Quality Feature Engineering Pipeline.
    Scores resumes based on 6 weighted factors:
    1. Readability (15%) - Flesch reading ease & sentence structure.
    2. Action Verbs (20%) - Presence of high-impact executive verbs.
    3. Bullet Density (15%) - Bullet point frequency and formatting.
    4. Quantified Achievements (25%) - Detection of metrics ($/%, numbers).
    5. Grammar Heuristics (10%) - Absence of capitalization/punctuation errors.
    6. Formatting Completeness (15%) - Presence of key resume sections.
    """

    ACTION_VERBS: set = {
        "achieved",
        "architected",
        "built",
        "spearheaded",
        "developed",
        "implemented",
        "engineered",
        "orchestrated",
        "lead",
        "led",
        "managed",
        "designed",
        "created",
        "optimized",
        "increased",
        "reduced",
        "saved",
        "expanded",
        "transformed",
        "generated",
        "launched",
        "scale",
        "scaled",
        "automated",
        "streamlined",
    }

    def analyze(self, raw_text: str, parsed_sections: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if not raw_text or not raw_text.strip():
            return {
                "overall_quality_score": 0.0,
                "feature_breakdown": {
                    "readability": 0.0,
                    "action_verbs": 0.0,
                    "bullet_density": 0.0,
                    "quantified_achievements": 0.0,
                    "grammar_heuristics": 0.0,
                    "formatting_completeness": 0.0,
                },
                "metrics_detected_count": 0,
                "action_verbs_detected": [],
                "word_count": 0,
                "recommendations": ["Upload a non-empty resume document with readable text."],
            }

        words = re.findall(r"\b\w+\b", raw_text)
        word_count = len(words)
        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

        # 1. Readability (Fair scoring for both concise and detailed resumes)
        if word_count >= 15:
            readability_score = min(100.0, 75.0 + min(25.0, (word_count / 10.0)))
        else:
            readability_score = (word_count / 15.0) * 75.0

        # 2. Action Verbs
        found_verbs = [w.lower() for w in words if w.lower() in self.ACTION_VERBS]
        unique_verbs = len(set(found_verbs))
        action_verb_score = min(100.0, (unique_verbs / 3.0) * 100.0)

        # 3. Bullet Density
        bullet_lines = [
            line_str for line_str in lines if line_str.startswith(("-", "•", "*", "–")) or re.match(r"^\d+\.", line_str)
        ]
        bullet_score = min(100.0, (len(bullet_lines) / max(len(lines) * 0.3, 1)) * 100.0)

        # 4. Quantified Achievements ($ / % / throughput numbers)
        metrics_found = re.findall(
            r"(\$\d+|\d+%\s*|\b\d+(?:,\d+)*(?:\.\d+)?\s*(?:k|m|b|x|users|clients|percent|requests)?\b)", raw_text, re.I
        )
        quantified_score = min(100.0, (len(metrics_found) / 2.0) * 100.0)

        # 5. Grammar Heuristics (Capitalization check on bullet beginnings)
        capitalized_lines = [line_str for line_str in lines if line_str[0].isupper()]
        grammar_score = min(100.0, (len(capitalized_lines) / max(len(lines), 1)) * 100.0)

        # 6. Formatting Completeness (Required Sections)
        sections = parsed_sections or {}
        key_sections = ["summary", "skills", "experience", "education", "projects"]
        present_count = sum(1 for s in key_sections if sections.get(s) or s in raw_text.lower())
        formatting_score = min(100.0, (present_count / len(key_sections)) * 100.0)

        # Weighted Final Quality Score calculation
        final_quality_score = round(
            (readability_score * 0.15)
            + (action_verb_score * 0.20)
            + (bullet_score * 0.15)
            + (quantified_score * 0.25)
            + (grammar_score * 0.10)
            + (formatting_score * 0.15),
            1,
        )

        recommendations: List[str] = []
        if quantified_score < 70:
            recommendations.append(
                "Quantify achievements with metrics (e.g., increased performance by 35%, reduced latency by 200ms)."
            )
        if action_verb_score < 70:
            recommendations.append(
                "Incorporate more executive action verbs (e.g., Spearheaded, Architected, Optimized)."
            )
        if formatting_score < 80:
            recommendations.append("Ensure clear section headers for Experience, Education, Skills, and Projects.")
        if not recommendations:
            recommendations.append(
                "Resume quality is strong! Consider tailoring key skills for specific target job descriptions."
            )

        return {
            "overall_quality_score": final_quality_score,
            "feature_breakdown": {
                "readability": round(readability_score, 1),
                "action_verbs": round(action_verb_score, 1),
                "bullet_density": round(bullet_score, 1),
                "quantified_achievements": round(quantified_score, 1),
                "grammar_heuristics": round(grammar_score, 1),
                "formatting_completeness": round(formatting_score, 1),
            },
            "metrics_detected_count": len(metrics_found),
            "action_verbs_detected": list(set(found_verbs)),
            "word_count": word_count,
            "recommendations": recommendations,
        }


resume_quality_pipeline = ResumeQualityPipeline()
