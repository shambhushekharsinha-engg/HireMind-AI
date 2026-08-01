import hashlib
from typing import Dict, List, Optional


class EmbeddingCache:
    """
    In-Memory & Hash-indexed Embedding Cache to eliminate redundant vector computations.
    """

    def __init__(self):
        self._cache: Dict[str, List[float]] = {}

    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()

    def get(self, text: str) -> Optional[List[float]]:
        key = self._hash_text(text)
        return self._cache.get(key)

    def set(self, text: str, embedding: List[float]) -> None:
        key = self._hash_text(text)
        self._cache[key] = embedding

    def size(self) -> int:
        return len(self._cache)


embedding_cache = EmbeddingCache()
