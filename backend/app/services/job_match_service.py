from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.services.nlp_engine import NLPEngine

class JobMatchService:

    @classmethod
    def match(cls, resume_text: str, job_description: str) -> Dict[str, Any]:
        if not resume_text or not job_description:
            return {
                "match_score": 0.0,
                "matched_skills": [],
                "missing_skills": [],
                "recommendations": ["Provide both resume text and job description."],
                "role_fit": "Low Fit"
            }

        # 1. Skill Extraction
        resume_skills = set(NLPEngine.extract_skills(resume_text))
        job_skills = set(NLPEngine.extract_skills(job_description))

        matched_skills = sorted(list(resume_skills.intersection(job_skills)))
        missing_skills = sorted(list(job_skills.difference(resume_skills)))

        # 2. Semantic Similarity using TF-IDF + Cosine Similarity
        try:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            semantic_score = float(cos_sim) * 100.0
        except Exception:
            semantic_score = 50.0

        # 3. Skill Overlap Ratio
        if job_skills:
            skill_score = (len(matched_skills) / len(job_skills)) * 100.0
        else:
            skill_score = semantic_score

        # Composite Score: 60% Skill Match + 40% Semantic TF-IDF Similarity
        final_score = round(0.6 * skill_score + 0.4 * semantic_score, 1)
        final_score = min(100.0, max(0.0, final_score))

        # Role Fit Classification
        if final_score >= 80:
            role_fit = "Strong Candidate Fit"
        elif final_score >= 60:
            role_fit = "Moderate Candidate Fit"
        else:
            role_fit = "Skill Gap Identified"

        # Recommendations
        recommendations = []
        if missing_skills:
            top_missing = missing_skills[:5]
            recommendations.append(f"Incorporate missing key job skills into your resume: {', '.join(top_missing)}.")
        
        if final_score < 70:
            recommendations.append("Tailor your work experience and project descriptions using exact keywords from the Job Description.")

        if not matched_skills and job_skills:
            recommendations.append("High skill discrepancy. Consider acquiring core domain skills before applying.")

        return {
            "match_score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
            "role_fit": role_fit
        }
