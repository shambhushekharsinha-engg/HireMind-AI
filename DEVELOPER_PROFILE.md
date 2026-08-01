# 👨‍💻 Developer Profile & System Architecture Showcase — HireMind AI

> **HireMind AI** is an enterprise-grade **Career Intelligence Operating System** engineered by a Lead AI Systems Architect. The project demonstrates production-grade software engineering, repository isolation, deterministic AI feature pipelines, RAG vector search, domain event dispatching, system security, and automated CI/CD.

---

## 🚀 Lead Developer & Engineer Overview

- **Role**: Lead Systems Architect & Senior AI Software Engineer
- **Core Domain**: Enterprise Web Architecture, Deterministic Machine Learning Pipelines, Vector RAG Search Engines, Distributed API Systems, and Security Engineering.
- **Key Philosophy**: *"Beyond MVP into Software Engineering — Clean Repositories, Fail-Fast Reliability, Explainable AI, and Zero-Downtime Telemetry."*

---

## 🏛️ Comprehensive Architecture & Updates (v3.0.0 Release Candidate)

### 1. Repository-Layer Database Architecture
- Replaced direct `SessionLocal()` queries across service endpoints with a structured **Repository Pattern**:
  - `UserRepository`: User management, credential verification, password reset tokens.
  - `ResumeRepository`: Resume documents, revisions, ATS score history, builder drafts.
  - `JobRepository`: Job descriptions, required skills matrix, candidate matching.
  - `ApplicationRepository`: Job application tracking lifecycle.
- **Alembic DB Migrations**: Managed database schema evolution with SQLite batch mode (`render_as_batch=True`).

### 2. Deterministic AI Quality Pipeline (Feature Engineering)
- Avoided black-box unexplainable ML models in favor of a **5-Factor Feature Engineering Pipeline**:
  - **Readability**: Flesch Reading Ease analysis.
  - **Action Verbs**: Detection of high-impact executive verbs.
  - **Bullet Density**: Bullet point structure and length optimization.
  - **Quantified Achievements**: Detection of numerical metrics ($/%/x throughput).
  - **Formatting Hygiene**: Clean section header detection and table avoidance.

### 3. FAISS Vector RAG Engine & Session Memory
- **Local RAG Pipeline**: `Knowledge Base` $\rightarrow$ `Embedding Cache` $\rightarrow$ `FAISS Vector Store` $\rightarrow$ `RAG Prompt Builder` $\rightarrow$ `LLM` $\rightarrow$ `Answer Validator`.
- **Session Memory**: Turn-by-turn conversation context history retaining previous user interactions for adaptive advice.

### 4. Lightweight Internal Domain Event Dispatcher
- Publisher-subscriber event bus decoupling system services:
  - `ResumeUploadedEvent` $\rightarrow$ `ResumeParsedEvent` $\rightarrow$ `ATSCalculatedEvent` $\rightarrow$ `ReportGeneratedEvent` $\rightarrow$ `NotificationSentEvent`.

### 5. Fail-Fast Startup System Validation
- `StartupValidator` executes before accepting traffic:
  - Secret Key presence and length check.
  - Storage directories (`uploads/`, `generated_reports/`) writability.
  - Database connectivity test (`SELECT 1`).
  - spaCy NLP model loading.
  - FAISS Vector Store readiness.

### 6. Centralized Standardized Error Catalog
- Enforced `HM1000` series standardized error responses:
  - `HM1001`: Resume text parsing failed.
  - `HM1002`: File size exceeds upload limit.
  - `HM1003`: Unsupported extension or MIME type.
  - `HM2001`: Authentication failure.
  - `HM3001`: Centralized AI Evaluation Engine error.
  - `HM429`: Rate limit exceeded.

### 7. Advanced Feature Modules
- **3-Option Selective Bullet Rewriter**: Detects weak bullets and provides `Professional`, `Executive`, and `Metrics-Driven` rewrite choices with Before/After/Reason structures.
- **Timed Multi-Personality Interview Simulator**: Presets (`Strict Tech Lead`, `Supportive HR`, `VP of Engineering`), target timers (60s/90s), dynamic follow-up questions, and 4D evaluation.
- **Modular Portfolio Analyzer**: `GitHub Analyzer` + `LinkedIn Analyzer` + `Resume Analyzer` + `Project Analyzer` $\rightarrow$ `Overall Candidate Score`.
- **Adaptive Personalized Roadmap Engine**: Dynamically adapts learning steps using current ATS score, target role, missing skills, and learning pace.
- **AI Career Progress Dashboard**: Aggregates ATS trends, skill growth over time, interview performance, and overall career readiness.

### 8. System Security & Telemetry
- Security Headers Middleware: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Content-Security-Policy`.
- In-memory sliding-window Rate Limiter.
- Distributed Request Lifecycle Tracing (`X-Trace-ID` and micro-spans).
- Prometheus Metrics endpoint (`/metrics`) and Operational Health Dashboard (`/health/dashboard`).
- Commit-tagged load benchmark history (`benchmark_history.json`).

### 9. Quality Assurance & CI/CD
- **46 Automated Pytest Cases** passing with 100% success rate across Unit, Integration, API, Security, Performance, and AI Pipeline categories.
- Black, Ruff, and isort formatting enforced via pre-commit hooks and GitHub Actions CI workflow.

---

## 🛠️ Technology Stack Overview

| Layer | Technologies & Tools |
| :--- | :--- |
| **Backend Core** | Python 3.11+, FastAPI, Pydantic v2, Uvicorn |
| **Data Access** | SQLAlchemy ORM, Repository Pattern, Alembic Migrations, SQLite / PostgreSQL |
| **AI & NLP** | spaCy (`en_core_web_sm`), Sentence Transformers, Scikit-Learn, FAISS Vector Search |
| **Feature Engineering**| Deterministic ATS Scorer, Quality Pipeline, Selective Rewriter, RAG Coach |
| **Security & Middleware**| Python-Jose (JWT), Bcrypt, Security Headers, Sliding-Window Rate Limiter |
| **Testing & CI/CD** | Pytest, Pytest-Cov, Ruff, Black, isort, GitHub Actions Pipeline |
| **Containerization** | Docker, Docker-Compose, Multi-Stage Builds |

---

## 📈 System Metrics & Quality Summary

- **Total Test Cases**: 46 Automated Tests (100% Pass Rate)
- **API Latency (p95)**: ~27 ms (10 Concurrent Users), ~28 ms (100 Concurrent Users)
- **Error Rate**: 0.0% under load
- **Code Hygiene**: Clean Ruff linting, zero warnings, Black compliant
