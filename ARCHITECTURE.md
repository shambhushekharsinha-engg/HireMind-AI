# Architecture & System Design Document — HireMind AI

## System Overview

HireMind AI is an enterprise-grade Career Intelligence Operating System designed with clean software engineering principles, modular service layers, repository isolation, FAISS vector search, and unified AI evaluation.

```mermaid
graph TD
    Client[Frontend PWA / Web Client] --> RateLimit[Rate Limiting Middleware]
    RateLimit --> Audit[Structured Audit Logger Middleware]
    Audit --> Router[FastAPI Router v1 & v2]
    Router --> Dep[FastAPI Dependency Injection]
    Dep --> Service[Service Layer + Feature Flags]
    Service --> Repos[Entity Repositories: User, Resume, Job, Application]
    Repos --> DB[(SQLAlchemy DB + Alembic Migrations)]
    Service --> EvalEngine[Centralized AI Evaluation Engine]
    EvalEngine --> FeatPipe[Resume Quality Feature Pipeline]
    Service --> RAG[RAG Engine: KB -> Cache -> Retriever -> PromptBuilder -> LLM -> Validator]
    RAG --> FAISS[FAISS Vector Store + Embedding Cache]
    Service --> Background[FastAPI Async Background Tasks]
```

---

## Architectural Layering

### 1. API Layer (`app/api/`)
- Handles HTTP requests, payload validation via Pydantic schemas, and response formatting.
- Enforces strict security headers, CORS origins, and OpenAPI example documentation.

### 2. Dependency Injection & Middleware (`app/core/`)
- `get_db`: Grants clean database session scopes per request.
- `SecurityHeadersMiddleware`: Injects `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and `CSP`.
- `RateLimiter`: Sliding-window rate limiting protecting sensitive auth and AI endpoints.
- `FeatureFlags`: Config-driven feature switches (`ENABLE_EXPERIMENTAL_AI`, `ENABLE_FAISS_VECTOR_SEARCH`).

### 3. Service Layer & AI Engines (`app/services/`)
- **Centralized AI Evaluation Engine** (`evaluation_engine.py`): Single source of truth for ATS scoring, resume quality evaluation, job matching, and roadmap generation.
- **Resume Quality Feature Pipeline** (`resume_quality_pipeline.py`): Feature engineering pipeline computing Readability, Action Verbs Density, Bullet Structure, Quantified Achievements Ratio, and Formatting Completeness.
- **FAISS Vector RAG Engine** (`career_coach.py` & `vector_store.py`):
  `Knowledge Base` $\rightarrow$ `Embedding Cache` $\rightarrow$ `FAISS Retriever` $\rightarrow$ `Prompt Builder` $\rightarrow$ `LLM` $\rightarrow$ `Answer Validator`.

### 4. Repository Pattern (`app/repositories/`)
- Isolates raw database interactions from business logic.
- Implements generic CRUD operations via `BaseRepository[T]` for:
  - `UserRepository`
  - `ResumeRepository`
  - `JobRepository`
  - `ApplicationRepository`

### 5. Database & Migrations (`app/database/` & `alembic/`)
- SQLAlchemy ORM with SQLite (development) and PostgreSQL (production).
- Alembic database migration scripts with SQLite batch mode support (`render_as_batch=True`).

---

## Database Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o{ RESUMES : owns
    USERS ||--o{ JOB_APPLICATIONS : tracks
    USERS ||--o{ PASSWORD_RESET_TOKENS : has
    RESUMES ||--o{ RESUME_REVISIONS : versioned_by
    RESUMES ||--o{ RESUME_ANALYSES : evaluated_in
    RESUMES ||--o{ JOB_MATCHES : matched_in
    JOB_DESCRIPTIONS ||--o{ JOB_MATCHES : target_of
```

---

## Observability & Prometheus Metrics

Exposed metrics at `/metrics`:
- `hiremind_api_requests_total`: Counter tracking API requests.
- `hiremind_ats_evaluations_total`: Counter tracking ATS scoring executions.
- `hiremind_faiss_vectors_indexed`: Gauge of indexed knowledge base vectors.
