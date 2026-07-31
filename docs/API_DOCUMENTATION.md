# HireMind AI v3.0 — API Reference Manual

Base API Endpoint: `/api/v1`

---

## 🔑 Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/register`: Register new user (Student / Recruiter / Admin).
- `POST /api/v1/auth/login`: Authenticate and return JWT access token.

---

## 📄 Resumes & ATS Intelligence (`/api/v1/resumes`)
- `POST /api/v1/resumes/upload`: Upload PDF/DOCX resume for text parsing & multi-factor ATS evaluation.
- `GET /api/v1/resumes/history`: Retrieve list of past resume evaluations.

---

## 🎨 Interactive Resume Builder (`/api/v1/builder`)
- `POST /api/v1/builder/draft`: Save interactive resume draft.
- `POST /api/v1/builder/download-pdf`: Render and download styled PDF resume.

---

## 🎯 Job Intelligence & Matching (`/api/v1/jobs`)
- `POST /api/v1/jobs/match`: Calculate TF-IDF Cosine Similarity and skill gap comparison.

---

## 📌 Job Application Tracker (`/api/v1/applications`)
- `GET /api/v1/applications`: List all tracked job applications.
- `POST /api/v1/applications`: Create new application card.
- `PATCH /api/v1/applications/{app_id}`: Update application stage (Saved, Applied, Interviewing, Offer, Rejected).
- `DELETE /api/v1/applications/{app_id}`: Delete application card.

---

## 🤖 AI Career Coach (`/api/v1/coach`)
- `POST /api/v1/coach/ask`: Conversational Q&A assistant for career questions.

---

## 🧭 Career Roadmaps (`/api/v1/career`)
- `POST /api/v1/career/roadmap`: Generate 4-phase step-by-step learning roadmap and salary estimates.

---

## 🎤 Interview Hub (`/api/v1/interview`)
- `POST /api/v1/interview/questions`: Generate domain technical/behavioral interview questions.
- `POST /api/v1/interview/evaluate`: Evaluate user answer text with scoring rubric.

---

## ✍️ Resume Bullet Rewriter (`/api/v1/rewriter`)
- `POST /api/v1/rewriter/rewrite`: Rewrite basic bullets into Google XYZ formula items.

---

## 👥 Recruiter Portal (`/api/v1/recruiter`)
- `GET /api/v1/recruiter/candidates`: Filter candidates by skills and min ATS score.

---

## 📊 Analytics Dashboard (`/api/v1/analytics`)
- `GET /api/v1/analytics/user`: Candidate ATS score history and funnel conversion metrics.
- `GET /api/v1/analytics/admin`: System metrics, active users, and API latency.
