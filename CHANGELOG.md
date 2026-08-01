# Changelog

All notable changes to **HireMind AI** will be documented in this file.

## [3.0.0] - 2026-08-01

### Added
- **Repository Pattern**: Introduced `UserRepository`, `ResumeRepository`, `JobRepository`, and `ApplicationRepository` with clean CRUD abstraction.
- **Centralized AI Evaluation Engine**: Created single entry point (`evaluation_engine.py`) coordinating ATS scoring, job matching, and roadmap generation.
- **Resume Quality Feature Engineering Pipeline**: Deterministic scoring based on Readability, Action Verbs, Bullet Density, Quantified Achievements, and Formatting Completeness.
- **FAISS Vector Store & RAG Pipeline**: Context-aware Career Coach powered by local FAISS vector search, embedding cache, prompt builder, and answer validator.
- **Security & Rate Limiting**: Added `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `CSP`, restricted CORS origins, and token-bucket rate limiter.
- **Structured Audit Logging**: JSON audit log service for tracking authentication, resume upload, and report generation events.
- **Alembic Database Migrations**: Configured Alembic with SQLite batch support for versioned schema changes.
- **Prometheus Metrics**: Metrics endpoint `/metrics` for system observability.
- **Docker & Containerization**: Added `backend/Dockerfile` and `docker-compose.yml`.
- **Pre-commit & CI/CD Pipeline**: Integrated Black, Ruff, isort, pre-commit hooks, and GitHub Actions workflow.
- **Documentation Suite**: Added `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, and updated `README.md`.
