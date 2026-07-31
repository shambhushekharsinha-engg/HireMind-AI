import re
from typing import List, Dict, Any, Set
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None

SKILL_TAXONOMY = {
    # Programming Languages
    "python", "java", "c++", "c#", "c", "javascript", "typescript", "golang", "go", "rust", "php", "ruby", "swift", "kotlin", "sql", "html", "css", "r", "scala", "bash", "shell",
    
    # Web Frameworks & Libraries
    "react", "react.js", "reactjs", "next.js", "nextjs", "vue", "vue.js", "angular", "node.js", "nodejs", "express", "express.js", "fastapi", "flask", "django", "spring boot", "bootstrap", "tailwind", "tailwindcss", "redux", "graphql", "rest api", "html5", "css3",
    
    # ML / AI / Data Science
    "machine learning", "deep learning", "nlp", "natural language processing", "computer vision", "opencv", "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly", "huggingface", "transformers", "spacy", "nltk", "langchain", "llm", "generative ai", "rag", "faiss", "chromadb", "data science", "data analysis", "data engineering",
    
    # Databases & Cloud
    "postgresql", "postgres", "mysql", "sqlite", "mongodb", "redis", "elasticsearch", "oracle", "dynamodb", "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s", "terraform", "ci/cd", "git", "github", "gitlab", "linux", "nginx", "apache",
    
    # Soft Skills & Concepts
    "agile", "scrum", "problem solving", "leadership", "communication", "teamwork", "critical thinking", "project management", "time management", "analytical skills"
}

class NLPEngine:

    @staticmethod
    def extract_skills(text: str) -> List[str]:
        if not text:
            return []
        
        text_lower = " " + text.lower() + " "
        found_skills: Set[str] = set()

        for skill in SKILL_TAXONOMY:
            # Word boundary check
            escaped_skill = re.escape(skill)
            pattern = r"(?<=[\s,./()\-:;])" + escaped_skill + r"(?=[\s,./()\-:;]|$)"
            if re.search(pattern, text_lower):
                # Standardize names
                if skill in ["react.js", "reactjs"]:
                    found_skills.add("react")
                elif skill in ["next.js", "nextjs"]:
                    found_skills.add("next.js")
                elif skill in ["node.js", "nodejs"]:
                    found_skills.add("node.js")
                elif skill in ["express.js"]:
                    found_skills.add("express")
                elif skill in ["tailwindcss"]:
                    found_skills.add("tailwind css")
                elif skill in ["postgres"]:
                    found_skills.add("postgresql")
                elif skill in ["sklearn"]:
                    found_skills.add("scikit-learn")
                else:
                    found_skills.add(skill)

        return sorted(list(found_skills))

    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, str]:
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        github_match = re.search(r"(github\.com/[\w\-]+)", text, re.IGNORECASE)
        linkedin_match = re.search(r"(linkedin\.com/in/[\w\-]+)", text, re.IGNORECASE)

        return {
            "email": email_match.group(0) if email_match else "",
            "phone": phone_match.group(0) if phone_match else "",
            "github": github_match.group(0) if github_match else "",
            "linkedin": linkedin_match.group(0) if linkedin_match else ""
        }

    @staticmethod
    def detect_experience_years(text: str) -> float:
        matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years?|yrs?)", text, re.IGNORECASE)
        if matches:
            try:
                numbers = [float(m) for m in matches]
                return max(numbers)
            except ValueError:
                pass
        return 0.0

    @staticmethod
    def detect_education_level(text: str) -> str:
        text_lower = text.lower()
        if re.search(r"\b(ph\.?d|doctorate)\b", text_lower):
            return "PhD / Doctorate"
        elif re.search(r"\b(m\.?tech|master|ms|m\.?s|mca|msc)\b", text_lower):
            return "Master's Degree"
        elif re.search(r"\b(b\.?tech|bachelor|bs|b\.?s|bca|bsc|b\.?e)\b", text_lower):
            return "Bachelor's Degree"
        elif re.search(r"\b(diploma|associate)\b", text_lower):
            return "Diploma / Associate"
        return "Not Specified"
