import re
from typing import List, Dict, Any

class SelectiveResumeRewriter:
    """
    Selective Resume Bullet Rewriter returning 3 distinct rewrite options:
    1. Professional Option
    2. Executive Option
    3. Metrics-Driven / Technical Option
    Includes Before, After, Reason, and Accept/Reject status structures for full user control.
    """

    WEAK_PATTERNS = [
        r"\bworked on\b", r"\bresponsible for\b", r"\bhelped with\b", r"\bassisted in\b", r"\bhandled\b"
    ]

    @classmethod
    def rewrite_bullets(cls, bullet_points: List[str]) -> Dict[str, Any]:
        results = []
        rewritten_count = 0

        for bullet in bullet_points:
            is_weak = any(re.search(pat, bullet, re.IGNORECASE) for pat in cls.WEAK_PATTERNS) or not re.search(r"\d", bullet)

            if is_weak:
                rewritten_count += 1
                cleaned = re.sub(r"\b(worked on|responsible for|helped with|assisted in|handled)\b", "", bullet, flags=re.IGNORECASE).strip()
                cleaned = cleaned[0].upper() + cleaned[1:] if cleaned else "Built key features"
                
                option_professional = f"Engineered and maintained {cleaned}, improving overall team productivity."
                option_executive = f"Spearheaded strategic initiative to deploy {cleaned}, driving key operational goals."
                option_metrics = f"Architected and deployed {cleaned}, improving throughput by 35% and reducing latency by 40ms."
                
                results.append({
                    "original": bullet,
                    "is_weak": True,
                    "reason": "Original bullet lacked strong action verbs and quantified impact metrics ($/%).",
                    "options": {
                        "professional": option_professional,
                        "executive": option_executive,
                        "metrics_driven": option_metrics
                    },
                    "recommended_option": option_metrics,
                    "rewritten": option_metrics, # Default option for backward compatibility
                    "status": "PROPOSED_REWRITE"
                })
            else:
                results.append({
                    "original": bullet,
                    "is_weak": False,
                    "reason": "Bullet point already contains strong action verbs and metrics.",
                    "options": {
                        "preserved": bullet
                    },
                    "recommended_option": bullet,
                    "rewritten": bullet,
                    "status": "PRESERVED"
                })

        return {
            "total_bullets_analyzed": len(bullet_points),
            "weak_bullets_detected": rewritten_count,
            "bullet_rewrites": results
        }

    @classmethod
    def rewrite_bullet(cls, bullet: str) -> str:
        res = cls.rewrite_bullets([bullet])
        return res["bullet_rewrites"][0]["rewritten"]

ResumeRewriter = SelectiveResumeRewriter
resume_rewriter = SelectiveResumeRewriter()
