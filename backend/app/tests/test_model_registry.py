from app.core.model_registry import model_registry


def test_model_registry_list():
    models = model_registry.list_all_models()
    assert "nlp_spacy" in models
    assert "embedding_transformer" in models
    assert "faiss_vector_store" in models
    assert "llm_coach_engine" in models


def test_model_registry_info():
    info = model_registry.get_model_info("embedding_transformer")
    assert info["provider"] == "Hugging Face / SentenceTransformers"
    assert info["dimension"] == 384
