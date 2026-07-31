from typing import Dict, Any
from app.services.nlp_engine import NLPEngine
from app.services.ats_engine import ATSEngine

class VersionControlService:

    @classmethod
    def compare_versions(cls, v1_text: str, v2_text: str) -> Dict[str, Any]:
        v1_skills = set(NLPEngine.extract_skills(v1_text or ""))
        v2_skills = set(NLPEngine.extract_skills(v2_text or ""))

        added_skills = sorted(list(v2_skills.difference(v1_skills)))
        removed_skills = sorted(list(v1_skills.difference(v2_skills)))
        retained_skills = sorted(list(v1_skills.intersection(v2_skills)))

        # ATS Score calculation for both versions
        v1_sections = {"summary": v1_text[:200], "skills": ", ".join(v1_skills), "experience": v1_text[200:600]}
        v2_sections = {"summary": v2_text[:200], "skills": ", ".join(v2_skills), "experience": v2_text[200:600]}

        v1_eval = ATSEngine.evaluate(v1_text or "", v1_sections, list(v1_skills))
        v2_eval = ATSEngine.evaluate(v2_text or "", v2_sections, list(v2_skills))

        score_delta = round(v2_eval["ats_score"] - v1_eval["ats_score"], 1)

        return {
            "v1_ats_score": v1_eval["ats_score"],
            "v2_ats_score": v2_eval["ats_score"],
            "score_delta": score_delta,
            "improvement_status": "Improved ATS Score" if score_delta > 0 else "Neutral / Degraded",
            "added_skills": added_skills,
            "removed_skills": removed_skills,
            "retained_skills": retained_skills,
            "v1_word_count": len((v1_text or "").split()),
            "v2_word_count": len((v2_text or "").split())
        }
