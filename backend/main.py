from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import spacy
from pypdf import PdfReader

app = FastAPI()

nlp = spacy.load("en_core_web_sm")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.get("/")
def home():
    return {"message": "HireMind AI Resume Analyzer Running"}

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):

    print("UPLOAD API HIT")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    reader = PdfReader(file_path)

    resume_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text

    # JOB DESCRIPTION 

    job_description = """
    Python
    SQL
    Machine Learning
    TensorFlow 
    FastAPI
    React
    """

    # SKILL EXTRACTION

    doc = nlp(resume_text)

    skills = []

    skill_keywords = [
        "python",
        "java",
        "c++",
        "sql",
        "tensorflow",
        "machine learning",
        "deep learning",
        "nlp",
        "pandas",
        "numpy",
        "react",
        "fastapi",
        "opencv",
        "keras",
        "pytorch",
        "flask",
        "javascript",
        "html",
        "css"
    ]

    resume_lower = resume_text.lower()
    resume_lower =  " ".join(resume_lower.split())  # Remove extra whitespace

    for skill in skill_keywords:

        if skill in resume_lower:
            skills.append(skill)

    # ATS SCORE

    score = 0

    score += len(skills) * 3

    if len(resume_text) > 1500:
        score += 10

    if "project" in resume_lower:
        score += 10

    if "b.tech" in resume_lower or "education" in resume_lower:
        score += 5

    if "experience" in resume_lower or "internship" in resume_lower:
        score += 7

    if "certification" in resume_lower or "coursera" in resume_lower:
        score += 5

    if score > 100:
        score = 100

    # MISSING SKILLS SECTION

    job_skill = [
        "python",
        "sql",
        "machine learning",
        "tensorflow",
        "pandas",
        "numpy",
        "fastapi",
        "react"
    ]

    missing_skills = []

    for skill in job_skill:
        if skill not in skills:
            missing_skills.append(skill)

    matched_skills = []
    for skill in job_skill:
        if skill in skills:
            matched_skills.append(skill)

    match_score = int(
        (len(matched_skills) / len(job_skill)) * 100
    )

    # SUGGESTIONS

    suggestions = []

    if score < 80:
      suggestions.append("Add more relevant technical skills.")

    if "experience" not in resume_lower:
      suggestions.append("Add internship or project experience section.")

    if "react" not in skills:
      suggestions.append("Consider learning React for full-stack opportunities.")

    if "fastapi" not in skills:
      suggestions.append("Adding FastAPI projects can strengthen backend profile.")

    # STRENGTHS

    strengths = []

    if "education" in resume_lower or "b.tech" in resume_lower:
      strengths.append("Education Section Found")

    if "project" in resume_lower:
      strengths.append("Projects Section Found")

    if "experience" in resume_lower or "internship" in resume_lower:
      strengths.append("Experience Section Found")

    if "certification" in resume_lower or "coursera" in resume_lower:
      strengths.append("Certifications Found")

    # RESUME RATING BADGE

    if score >= 85:
        rating = ("Excellent")

    elif score >= 70:
        rating = ("Good")

    elif score >= 50:
        rating = ("Average")

    else:
        rating = ("Needs Improvement")

    # CAREER PATH SUGGESTION

    career_suggestions = []

    if "python" in skills and "sql" in skills:
        career_suggestions.append("Consider pursuing a career in Data Science or Software Engineering.")

    if "react" in skills:
        career_suggestions.append("Explore opportunities in Frontend Development or Full-Stack Development.")

    if "python" in skills and "machine learning" in skills:
        career_suggestions.append("Consider pursuing a career in Machine Learning Engineering.")

    if "fastapi" in skills:
        career_suggestions.append("Explore opportunities in Backend Development or API Development.")

    if "tensorflow" in skills :
        career_suggestions.append("Consider pursuing a career as AI Engineer.")

    if "pandas" in skills and "numpy" in skills:
        career_suggestions.append("Consider roles in Data Analysis or Data Engineering.")

    if "opencv" in skills:
        career_suggestions.append("Explore opportunities in Computer Vision.")

    if "keras" in skills or "pytorch" in skills:
        career_suggestions.append("Consider roles in Deep Learning or AI Research.")

    if "javascript" in skills and "html" in skills and "css" in skills:
        career_suggestions.append("Consider roles in Web Development.")

    if "flask" in skills:
        career_suggestions.append("Explore opportunities in Backend Development or API Development.")

    if "nlp" in skills:
        career_suggestions.append("Consider pursuing a career in Natural Language Processing.")

    if "c++" in skills or "java" in skills:
        career_suggestions.append("Consider roles in Software Development or Systems Programming.")

    if "sql" in skills and "python" in skills and "pandas" in skills and "numpy" in skills:
        career_suggestions.append("Consider roles as Data Analyst or Data Engineer.")

    if "machine learning" in skills and "tensorflow" in skills and "keras" in skills:
        career_suggestions.append("Consider roles as Machine Learning Engineer or AI Researcher.")

    career_suggestions = list(set(career_suggestions))

    # RETURN RESPONSE

    return {
        "filename": file.filename,
        "message": "Resume uploaded successfully",
        "resume_text": resume_text,
        "skills_found": skills,
        "ats_score": score,
        "job_match_score": match_score,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "strengths": strengths,
        "rating": rating,
        "career_suggestions": career_suggestions
    }

# NEW API STARTS HERE
@app.post("/job-match/")
async def job_match(job_description: str):

    job_description = job_description.lower()

    job_skills = [
        "python",
        "sql",
        "machine learning",
        "tensorflow",
        "pandas",
        "numpy",
        "fastapi",
        "react"
    ]

    matched_skills = []
    missing_skills = []

    for skill in job_skills:

        if skill in job_description:
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    match_score = int((len(matched_skills) / len(job_skills)) * 100)

    return {
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }