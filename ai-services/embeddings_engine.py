import os
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingsEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")

    def compute_similarity(self, text1: str, text2: str) -> float:
        if not text1 or not text2:
            return 0.0
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(sim)
        except Exception:
            return 0.5

    def rank_documents(self, query: str, documents: List[str]) -> List[Dict[str, Any]]:
        if not query or not documents:
            return []
        try:
            matrix = self.vectorizer.fit_transform([query] + documents)
            query_vec = matrix[0:1]
            doc_vecs = matrix[1:]
            similarities = cosine_similarity(query_vec, doc_vecs)[0]

            ranked = []
            for idx, score in enumerate(similarities):
                ranked.append({"doc_index": idx, "similarity_score": float(score)})
            
            return sorted(ranked, key=lambda x: x["similarity_score"], reverse=True)
        except Exception:
            return [{"doc_index": i, "similarity_score": 0.5} for i in range(len(documents))]

embeddings_service = EmbeddingsEngine()
