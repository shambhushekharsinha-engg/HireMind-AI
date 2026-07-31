# HireMind AI v3.0 – Enterprise Career Operating System

[![CI/CD Pipeline](https://github.com/shambhushekharsinha-engg/HireMind-AI/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/shambhushekharsinha-engg/HireMind-AI/actions)
[![FastAPI](https://img.shields.io/badge/FastAPI-v3.0-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-v19.0-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-v4.0-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Positioning Statement**: HireMind AI is not just a standard resume analyzer. It is an **AI-Powered Career Operating System** that helps students, software engineers, and professionals optimize resumes, match jobs with vector space similarity, prepare for interviews, plan learning roadmaps, generate portfolio websites, and manage their entire career journey through intelligent automation.

---

## 🌐 Live Production Deployments & Access

- **⚡ Production Web Application (Vercel)**: [https://hiremind-ai-resume.vercel.app](https://hiremind-ai-resume.vercel.app)
- **⚙️ Backend REST API Documentation (Render)**: [https://hiremind-ai-au7b.onrender.com/docs](https://hiremind-ai-au7b.onrender.com/docs)
- **📊 System Health Check**: [https://hiremind-ai-au7b.onrender.com/health](https://hiremind-ai-au7b.onrender.com/health)
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

## 🏛️ Scalable Architecture Specification

```
                          ┌───────────────────────────┐
                          │    API Gateway & Router   │
                          └─────────────┬─────────────┘
                                        │
    ┌────────────────┬──────────────────┼──────────────────┬────────────────┐
    │                │                  │                  │                │
┌───▼───┐        ┌───▼───┐          ┌───▼───┐          ┌───▼───┐        ┌───▼───┐
│ Auth  │        │Resume │          │  AI   │          │Report │        │  Job  │
│Service│        │Service│          │Service│          │Service│        │Tracker│
└───┬───┘        └───┬───┘          └───┬───┘          └───┬───┘        └───┬───┘
    │                │                  │                  │                │
    └────────────────┴──────────────────┼──────────────────┴────────────────┘
                                        │
                        ┌───────────────▼───────────────┐
                        │ Data Layer & Message Queues   │
                        │ (PostgreSQL / Redis / FAISS)  │
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
- **Vector Embeddings & FAISS**: TF-IDF Vector Space Model & Sentence Transformer cosine similarity for semantic job description matching.
- **Multi-Model Provider Support**: Pluggable backend architecture supporting OpenAI, Gemini, Hugging Face, and Ollama (offline local LLM).
- **AI Career Mentor ("I Want Microsoft SDE")**: Creates tailored roadmaps, timelines, projects, certifications, and interview preparation plans.
- **AI Explainability Score Breakdown (`/api/v2/ai/explain-ats`)**: Explains raw ATS scores down to weighted factor contributions (`Formatting 18/20`, `Skills 15/20`, `Experience 19/20`, `Projects 12/15`, `Education 9/10`, `Keywords 9/15`) and predicts interview callback probability %.

### ⚙️ Pillar 3 — Backend Engineering
- **API Versioning Namespace (`/api/v1` & `/api/v2`)**: Decoupled routers for enterprise features running alongside v1 routes.
- **Modular Microservices Boundary**: Split into Auth, Resumes, Jobs, AI, Reports, Notifications, and Analytics modules.
- **Redis & Caching**: Cache layers for OTP validation, user sessions, and API rate limiting.

### 🛡️ Pillar 4 — DevOps & Observability
- **Docker & Orchestration**: Containerization with production `Dockerfile.backend`, `Dockerfile.frontend`, and `docker-compose.yml`.
- **GitHub Actions CI/CD**: Automated integration testing workflow in `.github/workflows/ci-cd.yml`.
- **Observability**: Uptime health checks (`/health`), Prometheus metrics (`/metrics`), and performance execution timing headers (`X-Process-Time-Sec`).

### 🔒 Pillar 5 — Security & Compliance
- **Authentication**: Direct `bcrypt` password hashing, JWT bearer tokens, and OAuth2 form handlers.
- **Access Control**: Role-Based Access Control (RBAC) supporting `Student`, `Recruiter`, and `Admin` roles.
- **Input Validation**: Strict Pydantic v2 validation and file upload extension filtering (`PDF`, `DOCX`, `TXT`).

---

## 🚀 Unique Features Integrated

1. **Git-Style Resume Version Control Diff (`/api/v2/resume/compare-versions`)**: Side-by-side version comparator calculating added/removed skills and ATS score deltas.
2. **Application Tracker Board**: Kanban lifecycle management (`Applied`, `Interviewing`, `Offer`, `Rejected`).
3. **Target Company Blueprint (`/api/v2/ai/company-blueprint`)**: Pre-application hiring insights detailing interview difficulty, expected tech stack skills, salary estimates, and hiring trends.
4. **GitHub Repository Analyzer (`/api/v2/integrations/github-analyze`)**: Evaluates repository URLs for code quality, README documentation score, and commit consistency.
5. **Recruiter AI Portal (`/api/v1/recruiter/candidates`)**: Candidate ranking, minimum ATS threshold filter, and candidate summary badges.

---

## 🗄️ Relational Database Schema (12 SQLAlchemy ORM Models)

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│    Users     │────<│   Resumes    │────<│   ResumeAnalyses     │
└──────────────┘     └──────────────┘     └──────────────────────┘
       │                    │                        │
       │                    │                        │
       ▼                    ▼                        ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────────────┐
│ Applications │     │BuilderDrafts │     │   InterviewSessions  │
└──────────────┘     └──────────────┘     └──────────────────────┘
```

1. **`users`**: Email/Mobile authentication, direct bcrypt hashes, and RBAC roles.
2. **`resumes`**: File storage paths, extracted raw text, and version numbers.
3. **`resume_analyses`**: ATS scores, rating badges, section breakdowns, and detected skills.
4. **`resume_builder_drafts`**: Saved JSON drafts and template selections.
5. **`job_descriptions`**: Target role titles, raw text, and extracted skill arrays.
6. **`job_matches`**: Match scores, TF-IDF cosine similarity values, and missing skill lists.
7. **`job_applications`**: Application tracker board stages.
8. **`coach_messages`**: Conversational Q&A chat history with the AI Career Mentor.
9. **`career_roadmaps`**: Step-by-step learning roadmaps and estimated salary ranges.
10. **`interview_sessions`**: Practice interview questions, candidate answers, and evaluation scores.
11. **`notifications`**: System alerts and status updates.
12. **`feedbacks`**: User feedback ratings and comments.

---

## 📄 REST API Endpoint Manual

### API v1 Namespace (`/api/v1`)
| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | Register user with email or mobile number. |
| `POST` | `/api/v1/auth/login` | Authenticate user and return JWT bearer token. |
| `POST` | `/api/v1/auth/demo-login` | Instant 1-click login for Demo Student, Recruiter, or Admin. |
| `POST` | `/api/v1/resumes/upload` | Upload resume file (PDF/DOCX) and run multi-factor ATS evaluation. |
| `GET` | `/api/v1/resumes/history` | Retrieve historical resume evaluation records. |
| `POST` | `/api/v1/builder/download-pdf` | Render and download formatted PDF resume. |
| `POST` | `/api/v1/jobs/match` | Compute TF-IDF vector similarity between resume and job description. |
| `GET` | `/api/v1/applications` | List active job application tracker records. |
| `POST` | `/api/v1/applications` | Create a new job application tracker entry. |
| `POST` | `/api/v1/coach/ask` | Send question to AI Career Mentor. |
| `POST` | `/api/v1/career/roadmap` | Generate 4-phase step-by-step career growth roadmap. |
| `POST` | `/api/v1/interview/questions` | Fetch domain-specific interview practice questions. |
| `POST` | `/api/v1/interview/evaluate` | Evaluate candidate interview response against key rubrics. |
| `POST` | `/api/v1/rewriter/rewrite` | Transform bullet points into Google XYZ formula items. |
| `GET` | `/api/v1/recruiter/candidates` | Search, filter, and rank candidate resumes for recruiters. |
| `GET` | `/api/v1/analytics/user` | Fetch user activity metrics and platform status. |

### API v2 Namespace (`/api/v2`)
| Method | Path | Description |
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

With deep domain expertise in **FastAPI**, **React 19**, **Natural Language Processing (NLP)**, **TF-IDF Vector Space Models**, **SQLAlchemy ORM**, **Docker**, and **DevOps Infrastructure**, Shambhu architected **HireMind AI v3.0** and **Aegis Traffic AI** to demonstrate production-level reliability, sub-100ms response times, and state-of-the-art 3D glassmorphic user experiences.

### Core Technical Competencies
- **Artificial Intelligence & NLP**: Natural Language Processing, TF-IDF Cosine Similarity, PyTorch, Scikit-Learn, spaCy, Vector Embeddings, RAG Architectures.
- **Backend Engineering**: FastAPI, Python 3.13+, SQLAlchemy 2.0, Pydantic v2, Direct Bcrypt Security, JWT Authentication, PostgreSQL, SQLite.
- **Frontend Development**: React 19, Vite, Tailwind CSS v4.0, Glassmorphic 3D UI, Lucide Icons, Responsive Mobile-First Design.
- **DevOps & Cloud Infrastructure**: Docker, Docker Compose, Nginx Reverse Proxy, GitHub Actions CI/CD, Render, Vercel, Prometheus Telemetry.

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
