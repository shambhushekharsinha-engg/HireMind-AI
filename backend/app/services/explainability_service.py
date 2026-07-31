from typing import Dict, Any, List

class ExplainabilityService:

    @classmethod
    def explain_ats_score(cls, ats_score: float, section_scores: Dict[str, float], skills_count: int) -> Dict[str, Any]:
        breakdown = []
        
        # Skill Match Points
        skill_pts = section_scores.get("skill_match", min(35.0, skills_count * 3.5))
        breakdown.append({
            "factor": "Technical Skill Match",
            "contribution": f"+{skill_pts:.1f} pts",
            "explanation": f"Detected {skills_count} verified technical skills matching industry keyword taxonomies."
        })

        # Section Completeness Points
        sec_pts = section_scores.get("sections_completeness", 20.0)
        breakdown.append({
            "factor": "Section Structural Completeness",
            "contribution": f"+{sec_pts:.1f} pts",
            "explanation": "Evaluates presence of standard ATS header sections (Summary, Skills, Experience, Education, Projects)."
        })

        # Impact & Quantifiable Action Verbs
        impact_pts = section_scores.get("impact_metrics", 10.0)
        breakdown.append({
            "factor": "Quantifiable Impact & Action Verbs",
            "contribution": f"+{impact_pts:.1f} pts",
            "explanation": "Detects strong action verbs (Engineered, Spearheaded, Optimized) and measurable metrics (%, $, scale)."
        })

        # Word Count & Hygiene
        length_pts = section_scores.get("length_hygiene", 15.0)
        breakdown.append({
            "factor": "Length & Formatting Hygiene",
            "contribution": f"+{length_pts:.1f} pts",
            "explanation": "Assesses optimal word count density (300-1000 words) and text layout readability."
        })

        # Interview Call Probability ML Heuristic
        interview_probability = round(min(96.0, max(15.0, ats_score * 0.92 + (10.0 if skills_count >= 5 else 0))), 1)

        return {
            "ats_score": ats_score,
            "interview_call_probability": f"{interview_probability}%",
            "score_breakdown": breakdown,
            "transparency_note": "AI Explainability model breaks down raw scores into verifiable ATS factor contributions."
        }
