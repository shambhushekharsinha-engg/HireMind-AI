import json
from typing import Dict, Any, List

# Curated Industry Knowledge Base (O*NET & ESCO Taxonomy Mapped)
CAREER_KNOWLEDGE_BASE = {
    "machine_learning_engineer": {
        "title": "Machine Learning Engineer",
        "required_skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "SQL", "Docker", "Kubernetes", "AWS", "MLOps", "CI/CD"],
        "top_keywords": ["PyTorch", "Deep Learning", "LLMs", "RAG", "MLOps", "Kubernetes", "Transformer Models", "Model Optimization"],
        "salary_range": {"inr": "₹12 - ₹35 LPA", "usd": "$135,000 - $210,000 / year"},
        "interview_difficulty": "Hard (4.3 / 5.0)",
        "interview_topics": ["Machine Learning Algorithms", "System Design for ML", "Python Data Structures", "Deep Learning Architectures", "SQL & Data Pipeline"],
        "weekly_roadmap": [
            {"week": "Week 1", "topic": "Python Advanced & Data Structures", "resource": "Python Docs & LeetCode Medium"},
            {"week": "Week 2", "topic": "SQL & Data Manipulation (Pandas/NumPy)", "resource": "Kaggle Pandas Course & SQLZOO"},
            {"week": "Week 3", "topic": "Classical Machine Learning (Scikit-Learn)", "resource": "Andrew Ng Machine Learning Specialization"},
            {"week": "Week 4", "topic": "Deep Learning & Transformers (PyTorch)", "resource": "Fast.ai Deep Learning & PyTorch Official Tutorials"},
            {"week": "Week 5", "topic": "MLOps, Docker & Model Deployment", "resource": "Full Stack Deep Learning & Docker Docs"}
        ],
        "recommended_projects": [
            {"name": "AI Resume & Career Intelligence Engine", "desc": "NLP-powered parsing, TF-IDF semantic matching, and vector score recommendations."},
            {"name": "Real-Time Financial Fraud Detection", "desc": "Imbalanced classification using XGBoost, Kafka streaming, and Docker."},
            {"name": "Medical Imaging Diagnosis Classifier", "desc": "Convolutional Neural Networks (ResNet/EfficientNet) trained on chest X-ray scans."},
            {"name": "Multi-Modal RAG Knowledge Assistant", "desc": "LangChain, LlamaIndex, FAISS vector database, and Llama3 LLM integration."}
        ]
    },
    "full_stack_engineer": {
        "title": "Full-Stack Software Engineer",
        "required_skills": ["JavaScript", "TypeScript", "React", "Node.js", "Python", "FastAPI", "PostgreSQL", "Docker", "REST API", "GraphQL", "Tailwind CSS", "Git"],
        "top_keywords": ["React 19", "Next.js", "TypeScript", "Microservices", "PostgreSQL", "Docker", "Redis", "CI/CD"],
        "salary_range": {"inr": "₹8 - ₹28 LPA", "usd": "$110,000 - $175,000 / year"},
        "interview_difficulty": "Moderate-Hard (3.9 / 5.0)",
        "interview_topics": ["Frontend Architecture & State", "REST vs GraphQL", "Database Indexing & Queries", "System Design & Caching"],
        "weekly_roadmap": [
            {"week": "Week 1", "topic": "Modern JavaScript (ES6+) & TypeScript", "resource": "TypeScript Handbook & ExecuteProgram"},
            {"week": "Week 2", "topic": "React 19 Hooks, Context & Tailwind", "resource": "React Official Docs & Scrimba"},
            {"week": "Week 3", "topic": "Backend APIs with FastAPI / Node.js", "resource": "FastAPI Official Tutorial"},
            {"week": "Week 4", "topic": "PostgreSQL Schema Design & Redis Caching", "resource": "Use The Index, Luke & Postgres Docs"},
            {"week": "Week 5", "topic": "Dockerization, Nginx & Deployment", "resource": "Docker Curriculum & DigitalOcean Docs"}
        ],
        "recommended_projects": [
            {"name": "SaaS Product Dashboard with Analytics", "desc": "Full-stack React dashboard with authentication, subscription tiering, and PostgreSQL."},
            {"name": "Collaborative Real-Time Workspace App", "desc": "WebSockets, Node.js/FastAPI backend, and optimistic state updates."},
            {"name": "E-Commerce Microservices Engine", "desc": "Decoupled catalog, payment gateway integration, and Docker Compose setup."}
        ]
    },
    "data_scientist": {
        "title": "Data Scientist",
        "required_skills": ["Python", "R", "SQL", "Pandas", "NumPy", "Scikit-Learn", "Matplotlib", "Seaborn", "Statistics", "A/B Testing", "Tableau", "Power BI"],
        "top_keywords": ["A/B Testing", "Statistical Modeling", "SQL Analysis", "Predictive Analytics", "Tableau", "Hypothesis Testing"],
        "salary_range": {"inr": "₹9 - ₹30 LPA", "usd": "$120,000 - $185,000 / year"},
        "interview_difficulty": "Hard (4.1 / 5.0)",
        "interview_topics": ["Probability & Statistics", "SQL Queries & Aggregations", "Machine Learning Evaluation Metrics", "Business Case Studies"],
        "weekly_roadmap": [
            {"week": "Week 1", "topic": "Applied Statistics & Probability", "resource": "Khan Academy Statistics & OpenIntro"},
            {"week": "Week 2", "topic": "Advanced SQL & Window Functions", "resource": "Mode Analytics SQL Tutorial"},
            {"week": "Week 3", "topic": "Exploratory Data Analysis (Pandas/Seaborn)", "resource": "Kaggle Data Analysis Micro-Courses"},
            {"week": "Week 4", "topic": "Predictive Modeling & Feature Engineering", "resource": "Applied Predictive Modeling by Kuhn"}
        ],
        "recommended_projects": [
            {"name": "Customer Churn Prediction & Retention Analytics", "desc": "Random Forest and Logistic Regression modeling with actionable business recommendations."},
            {"name": "E-Commerce User Segmentation Dashboard", "desc": "K-Means Clustering, RFM analysis, and Interactive Streamlit/Tableau visualization."}
        ]
    }
}

class KnowledgeBaseEngine:

    @classmethod
    def get_role_info(cls, target_role: str) -> Dict[str, Any]:
        key = target_role.lower().replace(" ", "_").replace("/", "_")
        for role_key, info in CAREER_KNOWLEDGE_BASE.items():
            if role_key in key or key in role_key:
                return info
        
        # Fallback default info
        return CAREER_KNOWLEDGE_BASE["full_stack_engineer"]
