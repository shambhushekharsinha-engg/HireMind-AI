# HireMind AI v3.0 – Enterprise Career Operating System

[![CI/CD Pipeline](https://github.com/shambhushekharsinha-engg/HireMind-AI/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/shambhushekharsinha-engg/HireMind-AI/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-v3.0-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-v19.0-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4.0-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Positioning Statement**: HireMind AI is an **Enterprise AI-Powered Career Operating System** that empowers students, software engineers, and professionals to optimize resumes, match jobs using hybrid vector embeddings, practice interviews, track learning roadmaps, generate portfolio websites, and manage their entire career journey through production-grade intelligent automation.

---

## 🌐 Live Production Deployments & Access

- **⚡ Production Web Application (Vercel)**: [https://hiremind-ai-resume.vercel.app](https://hiremind-ai-resume.vercel.app)
- **⚙️ Backend REST API Documentation (Render)**: [https://hiremind-ai-au7b.onrender.com/docs](https://hiremind-ai-au7b.onrender.com/docs)
- **📊 System Health Check Overview**: [https://hiremind-ai-au7b.onrender.com/health](https://hiremind-ai-au7b.onrender.com/health)
- **🗄️ Database Health**: [https://hiremind-ai-au7b.onrender.com/health/db](https://hiremind-ai-au7b.onrender.com/health/db)
- **🧠 AI Engine Health**: [https://hiremind-ai-au7b.onrender.com/health/ai](https://hiremind-ai-au7b.onrender.com/health/ai)
- **📈 Prometheus Metrics Telemetry**: [https://hiremind-ai-au7b.onrender.com/metrics](https://hiremind-ai-au7b.onrender.com/metrics)

---

## 🔑 Quick Demo Credentials (Email / Mobile No.)

Try out HireMind AI instantly with pre-configured demo credentials:

| Role | Email Login | Mobile No. Login | Password | Access Level |
| :--- | :--- | :--- | :--- | :--- |
| **Student** | `alex.student@hiremind.ai` | `+919876543210` | `demo1234` | Full Resume, ATS, Job Matcher & Coach |
| **Recruiter** | `recruiter@apextech.com` | `+919876543211` | `demo1234` | Candidate Ranking & Resume Search |
| **Admin** | `admin@hiremind.ai` | `+919876543212` | `demo1234` | System Analytics & Metrics Dashboard |

---

## 🏛️ Enterprise Architecture Specification

```
                          ┌───────────────────────────┐
                          │    API Gateway & Router   │
                          │   (Request IDs & CORS)    │
                          └─────────────┬─────────────┘
                                        │
    ┌────────────────┬──────────────────┼──────────────────┬────────────────┐
    │                │                  │                  │                │
┌───▼───┐        ┌───▼───┐          ┌───▼───┐          ┌───▼───┐        ┌───▼───┐
│ Auth  │        │Resume │          │  AI   │          │Report │        │  Job  │
│Service│        │Service│          │Engine │          │Service│        │Tracker│
└───┬───┘        └───┬───┘          └───┬───┘          └───┬───┘        └───┬───┘
    │                │                  │                  │                │
    └────────────────┴──────────────────┼──────────────────┴────────────────┘
                                        │
                        ┌───────────────▼───────────────┐
                        │ Data Layer & Message Queues   │
                        │ (PostgreSQL / SQLite / Redis) │
                        └───────────────────────────────┘
```

---

## 🌟 Comprehensive 5-Pillar Architecture & Features

### 🎨 Pillar 1 — Product & User Experience
- **Interactive Resume Builder**: Drag-and-drop sections, professional templates (`Modern`, `Executive`, `Creative`, `Minimalist`), and single-click PDF export.
- **Portfolio Website Generator (`/api/v2/resume/portfolio-html`)**: Compiles candidate resume data into a standalone, responsive HTML/CSS portfolio website with light and dark themes.
- **Personalized Cover Letter Generator (`/api/v2/ai/cover-letter`)**: Tailors cover letters to candidate resume skills, job descriptions, and target company names.
- **LinkedIn Profile Optimizer (`/api/v2/ai/linkedin-optimize`)**: Calculates headline SEO scores, detected keyword tags, and recruiter searchability ratings.

### 🧠 Pillar 2 — Advanced AI, Vector Embeddings & Memory
- **40% / 60% Hybrid Job Matching Engine**: Combines sparse TF-IDF keyword vector space similarity (40%) with SentenceTransformer dense embeddings (60% using `all-MiniLM-L6-v2`) for semantic job matching.
- **spaCy NER Candidate Name Extraction**: Named Entity Recognition (`PERSON` entity tagger) with top-line heuristic fallbacks for accurate candidate name identification.
- **500+ Skill Alias Normalization Map**: Normalizes skill variations to canonical forms (`Py Torch`/`torch` $\rightarrow$ `PyTorch`, `JS` $\rightarrow$ `JavaScript`, `NodeJS` $\rightarrow$ `Node.js`, `Postgres` $\rightarrow$ `PostgreSQL`).
- **AI Explainability ATS Score Breakdown (`/api/v2/ai/explain-ats`)**: Explains raw ATS scores down to 4 sub-score categories (`Formatting Hygiene`, `Projects & Impact`, `Experience & Action Verbs`, `Skills Match`) and predicts callback probability %.

### ⚙️ Pillar 3 — Backend Engineering & Security
- **Dual JWT Token Architecture**: 15-minute `access_token` and 7-day `refresh_token` split with dedicated `/api/v1/auth/refresh` endpoint.
- **SHA-256 Single-Use Password Reset Tokens**: 32-byte URL-safe raw tokens (`secrets.token_urlsafe(32)`), stored as SHA-256 hashes in DB with 15-minute expiration and automatic invalidation.
- **Soft Delete Schema (`deleted_at TIMESTAMP NULL`)**: Standardized soft deletion across all 13 database models (`deleted_at IS NULL` indicates active records).
- **Clean Resume Versioning Entity Model**: `User` $\rightarrow$ `Resume` $\rightarrow$ `ResumeRevision` $\rightarrow$ `ResumeAnalysis` tracking file versions, version numbers, SHA-256 content hashes, and parsed sections.
- **SHA-256 Resume Content Hash Caching**: Hashes uploaded file content to return cached analysis results instantly for duplicate uploads without re-running heavy NLP parsers.

### 🛡️ Pillar 4 — DevOps, Security & Observability
- **Centralized Pydantic Settings Config ([config.py](file:///c:/HireMind-AI/backend/app/core/config.py))**: Manages JWT expiries, file size limits (10MB), allowed MIME types, upload paths, and secret keys.
- **Request IDs & Correlation Header (`X-Request-ID`)**: Middleware assigning unique `req-...` UUIDs to every HTTP request.
- **Structured JSON Logging**: Standardized JSON log output capturing `timestamp`, `request_id`, `method`, `path`, `status_code`, and `process_time_sec`.
- **Granular Health Check Endpoints**: `/health` (system), `/health/db` (`SELECT 1`), `/health/ai` (spaCy status), `/health/storage` (write access).
- **Standardized Error Envelopes**: Global exception handlers returning clean `{ "success": false, "error": { "code": "...", "message": "...", "request_id": "..." } }` JSON responses.

### 🔒 Pillar 5 — Upload Security & Compliance
- **Upload Security**: MIME type validation, 10MB file size limits, UUID4 randomized filenames (eliminating path traversal risks), and malformed PDF guards.
- **Multi-language ReportLab UTF-8 PDF Reports**: String XML escaping & UTF-8 character sanitization for multi-language resume PDF reports.

---

## 🗄️ Relational Database Schema (13 SQLAlchemy ORM Models)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│    Users     │────<│   Resumes    │────<│   ResumeRevisions    │────<│   ResumeAnalyses     │
└──────────────┘     └──────────────┘     └──────────────────────┘     └──────────────────────┘
       │                    │                        │
       │                    │                        │
       ▼                    ▼                        ▼
┌──────────────────┐ ┌──────────────┐     ┌──────────────────────┐
│PasswordResetToken│ │BuilderDrafts │     │   InterviewSessions  │
└──────────────────┘ └──────────────┘     └──────────────────────┘
```

1. **`users`**: Email/Mobile authentication, direct bcrypt hashes, RBAC roles, `created_at`, `updated_at`, `deleted_at`.
2. **`password_reset_tokens`**: SHA-256 hashed reset tokens (`token_hash`), `expires_at`, `is_used` single-use flag.
3. **`resumes`**: Resume container records bound to users.
4. **`resume_revisions`**: Individual file uploads, version numbers, content hashes, raw text, and parsed sections.
5. **`resume_analyses`**: ATS scores, rating badges, 4-part subscore dashboards, and detected skills.
6. **`resume_builder_drafts`**: Saved JSON drafts and template selections.
7. **`job_descriptions`**: Target role titles, raw text, and extracted skill arrays.
8. **`job_matches`**: Match scores, 40/60 hybrid vector similarity values, and missing skill lists.
9. **`job_applications`**: Application tracker board stages.
10. **`coach_messages`**: Conversational Q&A chat history with the AI Career Mentor.
11. **`career_roadmaps`**: Step-by-step learning roadmaps, completed steps, streaks, and estimated salary ranges.
12. **`interview_sessions`**: Practice interview questions, candidate answers, and evaluation scores.
13. **`notifications`**: System alerts and status updates.
14. **`feedbacks`**: User feedback ratings and comments.

---

## 📄 REST API Endpoint Manual

### API v1 Namespace (`/api/v1`)
| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register user with email or mobile number. |
| `POST` | `/api/v1/auth/login` | Authenticate user and return Access (15m) + Refresh (7d) token pair. |
| `POST` | `/api/v1/auth/refresh` | Exchange valid refresh token for a new access token pair. |
| `POST` | `/api/v1/auth/forgot-password` | Generate single-use SHA-256 hashed password reset token. |
| `POST` | `/api/v1/auth/reset-password` | Update password using valid reset token and invalidate single-use token. |
| `POST` | `/api/v1/auth/demo-login` | Instant 1-click login for Demo Student, Recruiter, or Admin. |
| `POST` | `/api/v1/resumes/upload` | Secure resume upload (PDF/DOCX) with SHA-256 caching & ATS scoring. |
| `GET` | `/api/v1/resumes/history` | Retrieve historical resume evaluation records. |
| `POST` | `/api/v1/jobs/match` | 40/60 Hybrid TF-IDF + Sentence Transformer semantic job matching. |
| `GET` | `/api/v1/applications` | List active job application tracker records. |
| `POST` | `/api/v1/coach/ask` | Send question to AI Career Mentor. |
| `POST` | `/api/v1/career/roadmap` | Generate 4-phase step-by-step career growth roadmap. |
| `POST` | `/api/v1/interview/questions` | Fetch domain-specific interview practice questions. |
| `POST` | `/api/v1/interview/evaluate` | Evaluate candidate interview response against key rubrics. |
| `POST` | `/api/v1/rewriter/rewrite` | Transform bullet points into Google XYZ formula items. |
| `GET` | `/api/v1/recruiter/candidates` | Search, filter, and rank candidate resumes for recruiters. |

### System & Health Endpoints
| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | System health overview. |
| `GET` | `/health/db` | Database connection health check (`SELECT 1`). |
| `GET` | `/health/ai` | AI engine & spaCy model loading status. |
| `GET` | `/health/storage` | File storage write permission check. |
| `GET` | `/metrics` | Prometheus format metrics telemetry endpoint. |

---

## 👨‍💻 Lead Developer Profile

<div align="center">
  <img src="https://github.com/shambhushekharsinha-engg.png" width="120" style="border-radius: 50%;" alt="Shambhu Shekhar Sinha"/>
  <h3>Shambhu Shekhar Sinha</h3>
  <p><b>Lead Full-Stack AI Engineer & Distributed Systems Architect</b></p>
  <p>
    <a href="https://github.com/shambhushekharsinha-engg">GitHub</a> • 
    <a href="https://linkedin.com">LinkedIn</a> • 
    <a href="mailto:shambhushekharsinha@example.com">Email</a>
  </p>
</div>

### Engineering Bio
**Shambhu Shekhar Sinha** is a Full-Stack AI Engineer and Distributed Systems Architect specializing in production-grade AI platforms, real-time telemetry systems, high-throughput REST microservices, and modern web application architecture. 

With deep domain expertise in **FastAPI**, **React 19**, **Natural Language Processing (NLP)**, **Sentence Transformers**, **SQLAlchemy ORM**, **Docker**, and **DevOps Infrastructure**, Shambhu architected **HireMind AI v3.0** and **Aegis Traffic AI** to demonstrate production-level reliability, sub-100ms response times, and state-of-the-art 3D glassmorphic user experiences.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
