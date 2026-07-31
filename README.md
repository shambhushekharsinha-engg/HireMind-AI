# HireMind AI — AI-Powered Career Operating System (v4.0 Enterprise Specification)

[![CI/CD Pipeline](https://github.com/shambhushekharsinha-engg/HireMind-AI/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/shambhushekharsinha-engg/HireMind-AI/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-v3.0-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-v19.0-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4.0-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**HireMind AI** is an **Enterprise Career Operating System** designed for job seekers, engineering students, professionals, and recruiters. Powered by FastAPI, Natural Language Processing (NLP), TF-IDF Vector Space Models, and Multi-Model AI, HireMind AI provides end-to-end career automation from resume parsing to interview prep and public hosting.

---

## 🏛️ System Architecture

```
   ┌─────────────────────────────────────────────────────────────┐
   │                  HireMind AI React Frontend                 │
   │               (Vercel / Tailwind CSS v4.0 / Vite)           │
   └──────────────────────────────┬──────────────────────────────┘
                                  │ HTTPS / REST API
   ┌──────────────────────────────▼──────────────────────────────┐
   │                  Nginx Reverse Proxy & Load Balancer         │
   └──────────────────────────────┬──────────────────────────────┘
                                  │
   ┌──────────────────────────────▼──────────────────────────────┐
   │                   FastAPI Application Gateway                │
   │            (/api/v1 Legacy & /api/v2 Enterprise)            │
   ├──────────────────────────────┬──────────────────────────────┤
   │ API Routers                  │ Middleware & Telemetry       │
   │ • Auth & RBAC                │ • Process Timing Header      │
   │ • Resume ATS & Builder       │ • CORS Policy Handler        │
   │ • AI Coach & Rewriter        │ • Prometheus Metrics         │
   │ • Integrations & Recruiter   │ • Health Check Endpoint      │
   └──────────────┬───────────────┴──────────────┬───────────────┘
                  │                              │
   ┌──────────────▼──────────────┐┌──────────────▼──────────────┐
   │  AI & NLP Engine Layer      ││  Data Infrastructure Layer   │
   │  • TF-IDF Cosine Similarity ││  • SQLAlchemy 2.0 ORM        │
   │  • Kaggle 25-Taxonomy Engine││  • PostgreSQL / SQLite DB    │
   │  • O*NET / ESCO Knowledge DB││  • Audit Logs & File System  │
   └─────────────────────────────┘└─────────────────────────────┘
```

---

## 📋 Final Production Checklist (v4.0)

### 1. Architecture & Design
- [x] **Modular FastAPI Architecture**: Layered design (`API Routers` → `Services` → `Models` → `Database`).
- [x] **Environment Configuration**: Centralized Pydantic `BaseSettings` reading from `.env`.
- [x] **API Versioning**: Dual-namespace routing (`/api/v1` and `/api/v2`).
- [x] **Centralized Exception Handling**: Structured JSON error tracebacks.

### 2. Security & Access Control
- [x] **Authentication**: Direct `bcrypt` password hashing and JWT Token generation.
- [x] **OAuth2 Integration**: Support for OAuth2 Password Bearer flow.
- [x] **Role-Based Access Control (RBAC)**: Enforced roles (`Student`, `Recruiter`, `Admin`).
- [x] **Input & File Upload Validation**: Type and extension filtering (`PDF`, `DOCX`, `TXT`).

### 3. AI & NLP Intelligence Engine
- [x] **Resume Parser & Section Segmentation**: Automatic section extraction (`Summary`, `Skills`, `Experience`, `Education`, `Projects`).
- [x] **Multi-Factor ATS Scoring**: Section completeness, word count density, contact hygiene, action verb count, and metric density.
- [x] **AI Bullet Rewriter**: Google XYZ formula bullet point enhancement.
- [x] **Semantic Job Matcher**: TF-IDF Vector Space Model & Cosine Similarity ranking.
- [x] **AI Resume Benchmarking**: Percentile score vs top 10% applicant cohorts and missing keywords ranking.
- [x] **Kaggle 25-Domain Taxonomy Engine**: Multi-field industry classification (Software, Data/AI, Cloud/DevOps, Security, Fintech).
- [x] **O*NET & ESCO Knowledge Base**: Curated career skill dictionaries, weekly learning timelines, and project recommenders.
- [x] **AI Explainability Score Breakdown**: Weighted factor score breakdown (`Formatting 18/20`, `Skills 15/20`, `Experience 19/20`, `Projects 12/15`, `Education 9/10`, `Keywords 9/15`).

### 4. User Product Suite
- [x] **Interactive Resume Builder**: Template selector (`Modern`, `Executive`, `Creative`, `Minimalist`) with single-click PDF export.
- [x] **Portfolio Website Generator**: Compiles resume data into standalone, responsive HTML/CSS portfolio websites.
- [x] **Personalized Cover Letter Generator**: Custom cover letters tailored to target company and role requirements.
- [x] **LinkedIn Profile Optimizer**: Headline SEO score calculation and summary searchability enhancement.
- [x] **Git-Style Resume Version Control Diff**: Side-by-side version comparison with added/removed skills and ATS delta.
- [x] **GitHub Repository Analyzer**: Code quality, README documentation score, and commit frequency evaluation.
- [x] **Target Company Blueprint**: Pre-application hiring insights for Microsoft, Google, Amazon & top tier tech firms.
- [x] **Application Tracker Board**: Kanban lifecycle management (`Applied`, `Interviewing`, `Offer`, `Rejected`).

### 5. Recruiter & Admin Portals
- [x] **Recruiter Candidate Ranking**: Candidate search, minimum ATS threshold filter, and skill keyword querying.
- [x] **Recruiter AI Summarizer**: Automatic candidate strengths, weaknesses, recommendation badge, and interview focus areas.

### 6. DevOps & Infrastructure
- [x] **Docker Containerization**: Production `Dockerfile.backend` and `Dockerfile.frontend`.
- [x] **Docker Compose**: Orchestration config for backend, frontend, PostgreSQL, Redis, and Nginx.
- [x] **CI/CD Pipeline**: GitHub Actions workflow running automated E2E tests and production builds.

### 7. Telemetry & Observability
- [x] **Health Check Endpoint**: `/health` status reporting database uptime and server timestamp.
- [x] **Prometheus Metrics Endpoint**: `/metrics` exposing request counters and ATS evaluation telemetry.
- [x] **Performance Timing Header**: Injects `X-Process-Time-Sec` headers into every response.

---

## ⚡ Quick Start Guide

### Local Development Setup

#### 1. Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # On Windows
# source venv/bin/activate    # On Linux/macOS

pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Swagger API Docs**: `http://127.0.0.1:8000/docs`
- **Health Check**: `http://127.0.0.1:8000/health`

#### 2. Frontend Setup (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
- **Web App**: `http://127.0.0.1:5173`

---

## 📄 API V2 Reference Table

| Method | Endpoint Path | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v2/resume/live-ats-score` | Real-time ATS score recalculation while editing. |
| `POST` | `/api/v2/resume/compare-versions` | Git-style side-by-side version diffing & ATS score delta. |
| `POST` | `/api/v2/resume/portfolio-html` | Compiles resume data into a standalone HTML portfolio website. |
| `POST` | `/api/v2/ai/cover-letter` | Personalized cover letter generator. |
| `POST` | `/api/v2/ai/linkedin-optimize` | LinkedIn headline SEO and summary searchability optimizer. |
| `POST` | `/api/v2/ai/company-blueprint` | Target company hiring blueprint ("Microsoft SDE", "Google SWE"). |
| `POST` | `/api/v2/ai/explain-ats` | Explainable ATS factor breakdown and interview call probability %. |
| `POST` | `/api/v2/ai/benchmark` | AI resume benchmarking against top 10% applicant cohort. |
| `POST` | `/api/v2/ai/career-gap` | Career gap analysis and 5-week personalized learning roadmap. |
| `POST` | `/api/v2/ai/recommend-projects` | Portfolio project recommender for target role. |
| `POST` | `/api/v2/ai/recruiter-summary` | Recruiter AI candidate summary & interview focus areas. |
| `POST` | `/api/v2/integrations/github-analyze` | Open-source GitHub repository quality analyzer. |

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
