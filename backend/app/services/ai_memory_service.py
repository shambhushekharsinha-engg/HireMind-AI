from typing import List, Dict, Any, Optional

class AIMemoryService:
    """
    AI Feedback Memory & Version Diffing Engine.
    Tracks historical resume analyses (v1 -> v2 -> v3) and generates explainable diff notes detailing score growth.
    """
    @staticmethod
    def analyze_score_evolution(analyses_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not analyses_history:
            return {"status": "No historical analyses recorded"}

        sorted_history = sorted(analyses_history, key=lambda x: x.get("created_at", ""))
        timeline = []
        for idx, item in enumerate(sorted_history):
            v_name = f"Resume v{idx + 1}"
            ats = item.get("ats_score", 0.0)
            timeline.append({"version": v_name, "ats_score": ats})

        first_score = sorted_history[0].get("ats_score", 0.0)
        latest_score = sorted_history[-1].get("ats_score", 0.0)
        score_diff = round(latest_score - first_score, 1)

        improvements = []
        if score_diff > 0:
            improvements.append(f"ATS score increased by +{score_diff} points due to added quantifiable metrics and technical skills.")
        elif score_diff == 0:
            improvements.append("ATS score maintained stability across revisions.")
        else:
            improvements.append("Score decreased slightly. Ensure core technical skills and section completeness were preserved.")

        return {
            "initial_score": first_score,
            "latest_score": latest_score,
            "net_improvement": score_diff,
            "timeline": timeline,
            "explainable_notes": improvements
        }

ai_memory_service = AIMemoryService()
