import pytest
from app.services.career_coach import career_coach_service, RAGPromptBuilder, AnswerValidator
from app.services.embedding_cache import embedding_cache
from app.services.vector_store import faiss_vector_store

def test_embedding_cache():
    text = "Machine Learning Engineer Career Path"
    emb = [0.1, 0.2, 0.3, 0.4]
    embedding_cache.set(text, emb)
    assert embedding_cache.get(text) == emb

def test_faiss_vector_store_search():
    docs = [{"id": "1", "content": "PyTorch and TensorFlow model training guide."}]
    faiss_vector_store.add_documents(docs)
    results = faiss_vector_store.search("PyTorch deep learning", top_k=1)
    assert len(results) > 0
    assert results[0][0]["id"] == "1"

def test_rag_prompt_builder_and_validator():
    docs = [({"content": "ATS Optimization Guide"}, 0.95)]
    prompt = RAGPromptBuilder.build_prompt("How to optimize ATS?", docs)
    assert "Candidate Question" in prompt["user"]

    validation = AnswerValidator.validate("To optimize ATS, use clean formatting and relevant keywords.", "How to optimize ATS?")
    assert validation["is_valid"] is True

def test_career_coach_rag_pipeline():
    res = career_coach_service.ask_coach("How do I become an ML engineer?")
    assert "answer" in res
    assert "suggested_followups" in res
    assert res["retrieved_context_count"] > 0
