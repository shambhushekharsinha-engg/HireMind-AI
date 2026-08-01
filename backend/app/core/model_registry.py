from typing import Dict, Any

class ModelRegistry:
    """
    Centralized Model Registry managing metadata, versions, and hyper-parameters
    for spaCy, Sentence Transformers, and LLM integrations.
    """
    def __init__(self):
        self._models: Dict[str, Dict[str, Any]] = {
            "nlp_spacy": {
                "name": "en_core_web_sm",
                "version": "3.8.0",
                "provider": "spaCy",
                "purpose": "Entity extraction, POS tagging, skill parsing"
            },
            "embedding_transformer": {
                "name": "all-MiniLM-L6-v2",
                "version": "2.2.2",
                "provider": "Hugging Face / SentenceTransformers",
                "dimension": 384,
                "purpose": "Local dense vector embeddings"
            },
            "faiss_vector_store": {
                "name": "FAISS-IndexFlatIP",
                "version": "1.7.4",
                "provider": "FAISS Local",
                "purpose": "Fast cosine similarity context retrieval"
            },
            "llm_coach_engine": {
                "name": "HireMind-CareerCoach-v3",
                "version": "3.0.0",
                "provider": "HireMind AI Native RAG",
                "purpose": "Contextual career advice & prompt synthesis"
            }
        }

    def get_model_info(self, model_key: str) -> Dict[str, Any]:
        return self._models.get(model_key, {"error": "Model key not registered"})

    def list_all_models(self) -> Dict[str, Dict[str, Any]]:
        return self._models.copy()

model_registry = ModelRegistry()
