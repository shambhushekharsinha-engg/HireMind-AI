import re
from typing import List, Dict, Any, Set, Optional
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    try:
        nlp = spacy.load("en")
    except Exception:
        nlp = None

# Canonical Skill Normalization Dictionary Map (Alias -> Canonical Name)
SKILL_ALIASES: Dict[str, str] = {
    # Machine Learning & AI
    "pytorch": "PyTorch", "py torch": "PyTorch", "torch": "PyTorch", "py-torch": "PyTorch",
    "tensorflow": "TensorFlow", "tf": "TensorFlow",
    "keras": "Keras",
    "scikit-learn": "scikit-learn", "sklearn": "scikit-learn",
    "pandas": "Pandas", "numpy": "NumPy", "scipy": "SciPy",
    "matplotlib": "Matplotlib", "seaborn": "Seaborn", "plotly": "Plotly",
    "huggingface": "Hugging Face", "transformers": "Transformers",
    "spacy": "spaCy", "nltk": "NLTK", "opencv": "OpenCV",
    "langchain": "LangChain", "llm": "LLM", "generative ai": "Generative AI",
    "rag": "RAG", "faiss": "FAISS", "chromadb": "ChromaDB", "vector db": "Vector DB",
    "machine learning": "Machine Learning", "ml": "Machine Learning",
    "deep learning": "Deep Learning", "dl": "Deep Learning",
    "nlp": "NLP", "natural language processing": "NLP",
    "computer vision": "Computer Vision", "cv": "Computer Vision",
    
    # Languages
    "python": "Python", "python3": "Python",
    "javascript": "JavaScript", "js": "JavaScript",
    "typescript": "TypeScript", "ts": "TypeScript",
    "golang": "Go", "go": "Go",
    "rust": "Rust",
    "java": "Java",
    "c++": "C++", "cpp": "C++",
    "c#": "C#", "csharp": "C#",
    "c": "C",
    "php": "PHP",
    "ruby": "Ruby",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "sql": "SQL", "psql": "SQL",
    "html": "HTML", "html5": "HTML",
    "css": "CSS", "css3": "CSS",
    "bash": "Bash", "shell": "Shell", "sh": "Shell",
    "r": "R", "scala": "Scala", "dart": "Dart",
    
    # Web Frameworks
    "react": "React", "react.js": "React", "reactjs": "React",
    "next.js": "Next.js", "nextjs": "Next.js", "next": "Next.js",
    "vue": "Vue.js", "vue.js": "Vue.js", "vuejs": "Vue.js",
    "angular": "Angular", "angularjs": "Angular",
    "node.js": "Node.js", "nodejs": "Node.js", "node": "Node.js",
    "express": "Express", "express.js": "Express",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "spring boot": "Spring Boot", "spring": "Spring Boot",
    "bootstrap": "Bootstrap",
    "tailwind": "Tailwind CSS", "tailwindcss": "Tailwind CSS", "tailwind css": "Tailwind CSS",
    "redux": "Redux", "graphql": "GraphQL", "rest api": "REST API", "restful api": "REST API",
    
    # Databases & Infrastructure
    "postgresql": "PostgreSQL", "postgres": "PostgreSQL", "psql": "PostgreSQL",
    "mysql": "MySQL",
    "sqlite": "SQLite",
    "mongodb": "MongoDB", "mongo": "MongoDB",
    "redis": "Redis",
    "elasticsearch": "Elasticsearch",
    "oracle": "Oracle DB",
    "dynamodb": "DynamoDB",
    "aws": "AWS", "amazon web services": "AWS",
    "azure": "Azure", "microsoft azure": "Azure",
    "gcp": "GCP", "google cloud": "GCP", "google cloud platform": "GCP",
    "docker": "Docker",
    "kubernetes": "Kubernetes", "k8s": "Kubernetes",
    "terraform": "Terraform",
    "ci/cd": "CI/CD", "jenkins": "Jenkins", "github actions": "GitHub Actions",
    "git": "Git", "github": "GitHub", "gitlab": "GitLab",
    "linux": "Linux", "nginx": "Nginx", "apache": "Apache",
    
    # Soft Skills & Practice
    "agile": "Agile", "scrum": "Scrum",
    "problem solving": "Problem Solving",
    "leadership": "Leadership",
    "communication": "Communication",
    "teamwork": "Teamwork",
    "critical thinking": "Critical Thinking",
    "project management": "Project Management",
    "time management": "Time Management",
    "analytical skills": "Analytical Skills"
}

class NLPEngine:

    @staticmethod
    def extract_candidate_name(text: str) -> str:
        """Extracts candidate name using spaCy PERSON NER with heuristic fallback."""
        if not text:
            return ""

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        top_text = "\n".join(lines[:10])

        # 1. spaCy NER PERSON detection
        if nlp:
            try:
                doc = nlp(top_text)
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        raw_name = ent.text.strip().split("\n")[0].strip()
                        clean_name = re.sub(r"[^A-Za-z\.\'\s-]", "", raw_name).strip()
                        words = clean_name.split()
                        if 2 <= len(words) <= 4 and not re.search(r"(engineer|developer|manager|designer|architect|resume|cv|summary|experience)", clean_name, re.I):
                            return clean_name.title()
            except Exception:
                pass

        # 2. Heuristic fallback: First non-contact non-header line
        header_keywords = {"resume", "curriculum", "vitae", "summary", "profile", "contact", "experience", "education", "skills", "projects", "engineer", "developer"}
        for line in lines[:5]:
            line_lower = line.lower()
            if any(kw in line_lower for kw in header_keywords):
                continue
            if re.search(r"[\w\.-]+@[\w\.-]+\.\w+", line) or re.search(r"\d{3}", line) or "http" in line_lower or "linkedin" in line_lower:
                continue
            # Must look like a name (2 to 4 words, letters only)
            words = line.split()
            if 2 <= len(words) <= 4 and all(re.match(r"^[A-Za-z\.\'-]+$", w) for w in words):
                return line.title()

        return "Candidate"


    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Extracts skills normalized via alias map."""
        if not text:
            return []
        
        text_lower = " " + text.lower() + " "
        found_skills: Set[str] = set()

        for alias, canonical_name in SKILL_ALIASES.items():
            escaped_alias = re.escape(alias)
            pattern = r"(?<=[\s,./()\-:;])" + escaped_alias + r"(?=[\s,./()\-:;]|$)"
            if re.search(pattern, text_lower):
                found_skills.add(canonical_name)

        return sorted(list(found_skills))

    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, str]:
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        github_match = re.search(r"(github\.com/[\w\-]+)", text, re.IGNORECASE)
        linkedin_match = re.search(r"(linkedin\.com/in/[\w\-]+)", text, re.IGNORECASE)

        candidate_name = NLPEngine.extract_candidate_name(text)

        return {
            "name": candidate_name,
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

