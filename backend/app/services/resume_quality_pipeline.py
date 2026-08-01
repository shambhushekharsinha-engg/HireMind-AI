import re
from typing import Any, Dict


class ResumeQualityPipeline:
    """
    Deterministic Feature Engineering Pipeline to evaluate Resume Quality.
    Evaluates:
    1. Readability Score
    2. Action Verbs Density
    3. Bullet Point Density & Structure
    4. Quantified Achievements Ratio (numbers, $, %)
    5. Grammar & Spelling Heuristics
    6. Formatting & Section Completeness
    Returns explainable weighted score (0 - 100).
    """

    ACTION_VERBS = {
        "built",
        "developed",
        "architected",
        "engineered",
        "implemented",
        "managed",
        "led",
        "designed",
        "created",
        "increased",
        "decreased",
        "reduced",
        "optimized",
        "spearheaded",
        "transformed",
        "orchestrated",
        "automated",
        "streamlined",
        "expanded",
        "generated",
        "launched",
        "maximized",
        "pioneered",
        "scaled",
    }

    SECTION_KEYWORDS = ["experience", "education", "skills", "projects", "summary"]

    def analyze(self, raw_text: str, parsed_sections: Dict[str, Any] = None) -> Dict[str, Any]:
        text = raw_text or ""
        words = re.findall(r"\b\w+\b", text)
        word_count = len(words)
        sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
        sentence_count = max(len(sentences), 1)

        # 1. Readability (Simplified Flesch Reading Ease Heuristic)
        avg_sentence_len = word_count / sentence_count
        readability_score = max(0.0, min(100.0, 100 - (avg_sentence_len * 1.5)))

        # 2. Action Verbs Density
        found_verbs = [w.lower() for w in words if w.lower() in self.ACTION_VERBS]
        action_verb_count = len(set(found_verbs))
        action_verb_score = min(100.0, (action_verb_count / 10.0) * 100.0)

        # 3. Bullet Point Density
        bullet_count = len(re.findall(r"^[\s]*[-•*]\s", text, re.MULTILINE))
        bullet_score = min(100.0, (bullet_count / 8.0) * 100.0)

        # 4. Quantified Achievements Ratio
        metrics_found = re.findall(
            r"\b(?:\d+%\b|\$\d+|\d+\s*k|\d+\+|\d+\s*million|\d+\s*percent|\d+)\b",
            text,
            re.IGNORECASE,
        )
        quantified_score = min(100.0, (len(metrics_found) / 5.0) * 100.0)

        # 5. Grammar & Spelling Heuristics (Check common typos/low quality patterns)
        typos = re.findall(r"\b(teh|recieve|managerial|seperate|responsable)\b", text, re.IGNORECASE)
        grammar_score = max(0.0, 100.0 - (len(typos) * 15.0))

        # 6. Formatting & Section Completeness
        present_sections = 0
        if parsed_sections:
            present_sections = sum(
                1 for sec in self.SECTION_KEYWORDS if sec in parsed_sections and parsed_sections[sec]
            )
        else:
            present_sections = sum(1 for sec in self.SECTION_KEYWORDS if re.search(rf"\b{sec}\b", text, re.IGNORECASE))
        formatting_score = (present_sections / len(self.SECTION_KEYWORDS)) * 100.0

        # Weighted Final Score Calculation
        # Readability (15%), Action Verbs (20%), Bullet Density (15%), Quantified Achievements (25%), Grammar (10%), Formatting (15%)
        final_quality_score = round(
            (readability_score * 0.15)
            + (action_verb_score * 0.20)
            + (bullet_score * 0.15)
            + (quantified_score * 0.25)
            + (grammar_score * 0.10)
            + (formatting_score * 0.15),
            1,
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
        }


resume_quality_pipeline = ResumeQualityPipeline()
