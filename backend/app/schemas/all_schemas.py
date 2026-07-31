from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Auth & User ---
class UserCreate(BaseModel):
    email: str
    password: str
    mobile_number: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = "student"

class UserLogin(BaseModel):
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: int
    email: str
    mobile_number: Optional[str] = None
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Resume Builder ---
class ResumeBuilderData(BaseModel):
    title: Optional[str] = "My Professional Resume"
    template_name: Optional[str] = "Modern"
    full_name: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    linkedin: Optional[str] = ""
    github: Optional[str] = ""
    summary: Optional[str] = ""
    experience: Optional[List[Dict[str, Any]]] = []
    education: Optional[List[Dict[str, Any]]] = []
    skills: Optional[List[str]] = []
    projects: Optional[List[Dict[str, Any]]] = []

# --- Job Application Tracker ---
class ApplicationCreate(BaseModel):
    company: str
    position: str
    status: Optional[str] = "Saved"
    location: Optional[str] = ""
    salary_range: Optional[str] = ""
    notes: Optional[str] = ""

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    company: str
    position: str
    status: str
    location: Optional[str]
    salary_range: Optional[str]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- AI Career Coach ---
class CoachAskRequest(BaseModel):
    question: str
    user_context: Optional[Dict[str, Any]] = {}

class CoachAskResponse(BaseModel):
    answer: str
    suggested_followups: List[str]
    recommended_resources: List[str]

# --- Resume Analysis ---
class ResumeAnalysisResult(BaseModel):
    filename: str
    resume_id: int
    ats_score: float
    rating: str
    skills_found: List[str]
    missing_skills: List[str]
    strengths: List[str]
    suggestions: List[str]
    career_suggestions: List[str]
    section_scores: Dict[str, float]
    parsed_sections: Dict[str, str]

# --- Job Match ---
class JobMatchRequest(BaseModel):
    job_title: Optional[str] = "Target Role"
    job_description: str
    resume_text: Optional[str] = None
    resume_id: Optional[int] = None

class JobMatchResult(BaseModel):
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    recommendations: List[str]
    role_fit: str

# --- Career Roadmap ---
class CareerRoadmapRequest(BaseModel):
    target_role: Optional[str] = None
    resume_id: Optional[int] = None
    resume_text: Optional[str] = None

class RoadmapStep(BaseModel):
    step: int
    title: str
    duration: str
    focus: str
    key_skills: List[str]
    recommended_projects: List[str]
    recommended_certifications: List[str]

class CareerRoadmapResult(BaseModel):
    target_role: str
    recommended_roles: List[str]
    skill_gaps: List[str]
    estimated_salary: Dict[str, str]
    roadmap: List[RoadmapStep]

# --- Interview Prep ---
class InterviewGenerateRequest(BaseModel):
    target_role: str
    resume_text: Optional[str] = None
    experience_level: Optional[str] = "Intermediate"

class InterviewQuestion(BaseModel):
    id: int
    category: str
    question: str
    hints: List[str]
    key_points_expected: List[str]

class InterviewSessionResult(BaseModel):
    target_role: str
    questions: List[InterviewQuestion]

class AnswerEvalRequest(BaseModel):
    question: str
    user_answer: str
    expected_points: Optional[List[str]] = []

class AnswerEvalResult(BaseModel):
    score: float
    feedback: str
    strengths: List[str]
    improvements: List[str]

# --- Bullet Rewriter ---
class BulletRewriteRequest(BaseModel):
    bullet_point: str
    target_role: Optional[str] = "Software Engineer"

class BulletRewriteResponse(BaseModel):
    original: str
    rewritten_options: List[str]
    action_verbs_used: List[str]
    impact_score_boost: str

# --- Feedback ---
class FeedbackCreate(BaseModel):
    rating: int
    comment: Optional[str] = None
