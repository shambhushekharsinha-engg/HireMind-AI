# HireMind AI Enterprise API v2 Documentation

Base API v2 Prefix: `/api/v2`

---

## 📄 Resume API v2 (`/api/v2/resume`)
- `POST /api/v2/resume/live-ats-score`: Real-time ATS score recalculation while editing.
- `POST /api/v2/resume/compare-versions`: Git-style side-by-side version comparison (added/removed skills, word count, ATS delta).
- `POST /api/v2/resume/portfolio-html`: Render responsive standalone HTML/CSS portfolio website.

---

## 🤖 AI Engine API v2 (`/api/v2/ai`)
- `POST /api/v2/ai/cover-letter`: Generate personalized cover letters based on candidate resume and company.
- `POST /api/v2/ai/linkedin-optimize`: Analyze LinkedIn headline/summary and output SEO recommendations.
- `POST /api/v2/ai/company-blueprint`: Fetch target company hiring insights ("Microsoft SDE", "Google SWE", "Amazon SDE").
- `POST /api/v2/ai/explain-ats`: Explain exact ATS score point breakdown and interview call probability %.

---

## 🔗 Integrations API v2 (`/api/v2/integrations`)
- `POST /api/v2/integrations/github-analyze`: Analyze GitHub repository URLs for project structure, language breakdown, and README quality.

---

## 📊 Observability & System Endpoints
- `GET /health`: System uptime, database connection status, and health status.
- `GET /metrics`: Prometheus formatted monitoring metrics (`hiremind_api_requests_total`, `hiremind_ats_evaluations_total`).
