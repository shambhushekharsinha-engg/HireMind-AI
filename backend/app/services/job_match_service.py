from typing import Any, Dict

from app.services.nlp_engine import NLPEngine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Try importing SentenceTransformer for dense embeddings
try:
    from sentence_transformers import SentenceTransformer

    EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    HAS_SENTENCE_TRANSFORMER = True
except Exception:
    EMBEDDING_MODEL = None
    HAS_SENTENCE_TRANSFORMER = False


class JobMatchService:
    @classmethod
    def match(cls, resume_text: str, job_description: str) -> Dict[str, Any]:
        if not resume_text or not job_description:
            return {
                "match_score": 0.0,
                "matched_skills": [],
                "missing_skills": [],
                "recommendations": ["Provide both resume text and job description."],
                "role_fit": "Low Fit",
            }

        # 1. Skill Extraction & Overlap
        resume_skills = set(NLPEngine.extract_skills(resume_text))
        job_skills = set(NLPEngine.extract_skills(job_description))

        matched_skills = sorted(list(resume_skills.intersection(job_skills)))
        missing_skills = sorted(list(job_skills.difference(resume_skills)))

        # 2. Sparse TF-IDF Cosine Similarity (40% weight of semantic score)
        try:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
            tfidf_sim = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]) * 100.0
        except Exception:
            tfidf_sim = 50.0

        # 3. Dense Embedding Cosine Similarity (60% weight of semantic score)
        if HAS_SENTENCE_TRANSFORMER and EMBEDDING_MODEL:
            try:
                embeddings = EMBEDDING_MODEL.encode([resume_text[:2000], job_description[:2000]])
                embedding_sim = float(cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]) * 100.0
            except Exception:
                embedding_sim = tfidf_sim
        else:
            embedding_sim = tfidf_sim

        # Hybrid Semantic Score = 40% TF-IDF + 60% Dense Embeddings
        hybrid_semantic_score = (0.40 * tfidf_sim) + (0.60 * embedding_sim)

        # Skill Overlap Ratio
        if job_skills:
            skill_score = (len(matched_skills) / len(job_skills)) * 100.0
        else:
            skill_score = hybrid_semantic_score

        # Composite Final Match Score: 50% Skill Match + 50% Hybrid Semantic
        final_score = round((0.50 * skill_score) + (0.50 * hybrid_semantic_score), 1)
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
            recommendations.append(f"Incorporate missing key job skills: {', '.join(top_missing)}.")

        if final_score < 70:
            recommendations.append("Tailor work experience bullet points using exact phrases from the job description.")

        if not matched_skills and job_skills:
            recommendations.append("High skill discrepancy. Consider taking courses for target role prerequisites.")

        return {
            "match_score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "score_breakdown": {
                "skill_overlap_score": round(skill_score, 1),
                "tfidf_similarity": round(tfidf_sim, 1),
                "dense_embedding_similarity": round(embedding_sim, 1),
                "hybrid_semantic_score": round(hybrid_semantic_score, 1),
            },
            "recommendations": recommendations,
            "role_fit": role_fit,
        }
