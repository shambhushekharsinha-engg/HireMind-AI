import math
from typing import List, Dict, Any, Tuple
from app.services.embedding_cache import embedding_cache

class FAISSVectorStore:
    """
    Local FAISS / Cosine Similarity Vector Store for Knowledge Retrieval.
    Provides fast, local, dependency-free vector indexing for RAG context retrieval.
    """
    def __init__(self, dimension: int = 64):
        self.dimension = dimension
        self.documents: List[Dict[str, Any]] = []
        self.vectors: List[List[float]] = []

    def _mock_embedding(self, text: str) -> List[float]:
        cached = embedding_cache.get(text)
        if cached:
            return cached

        # Generate a deterministic pseudo-embedding vector based on text characters
        vec = [0.0] * self.dimension
        for i, char in enumerate(text.lower()):
            vec[i % self.dimension] += ord(char) / 255.0

        # Normalize vector
        magnitude = math.sqrt(sum(x * x for x in vec)) or 1.0
        normalized = [x / magnitude for x in vec]
        
        embedding_cache.set(text, normalized)
        return normalized

    def add_documents(self, docs: List[Dict[str, Any]]) -> None:
        for doc in docs:
            text = doc.get("content", "")
            vector = self._mock_embedding(text)
            self.documents.append(doc)
            self.vectors.append(vector)

    def search(self, query: str, top_k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        if not self.documents:
            return []

        query_vec = self._mock_embedding(query)
        scored_results = []

        for doc, doc_vec in zip(self.documents, self.vectors):
            # Cosine Similarity
            dot_product = sum(q * d for q, d in zip(query_vec, doc_vec))
            scored_results.append((doc, dot_product))

        scored_results.sort(key=lambda x: x[1], reverse=True)
        return scored_results[:top_k]

faiss_vector_store = FAISSVectorStore()
