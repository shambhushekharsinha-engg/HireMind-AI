import os
import re
from typing import Dict, Any
from pypdf import PdfReader

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

class ResumeParser:

    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        text = ""
        if HAS_PDFPLUMBER:
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                if text.strip():
                    return text.strip()
            except Exception:
                pass
        
        # Fallback to PyPDF
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
            
        return text.strip()

    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        if not HAS_DOCX:
            return ""
        try:
            doc = docx.Document(file_path)
            full_text = [para.text for para in doc.paragraphs if para.text]
            return "\n".join(full_text)
        except Exception as e:
            print(f"Error reading DOCX: {e}")
            return ""

    @classmethod
    def parse_file(cls, file_path: str, filename: str) -> Dict[str, Any]:
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".pdf":
            raw_text = cls.extract_text_from_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            raw_text = cls.extract_text_from_docx(file_path)
        else:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    raw_text = f.read()
            except Exception:
                raw_text = ""

        cleaned_text = cls.clean_text(raw_text)
        sections = cls.identify_sections(cleaned_text)

        return {
            "raw_text": cleaned_text,
            "sections": sections
        }

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        # Remove extra whitespace and null bytes
        text = text.replace("\x00", "")
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return "\n".join(lines)

    @staticmethod
    def identify_sections(text: str) -> Dict[str, str]:
        sections = {
            "summary": "",
            "skills": "",
            "experience": "",
            "education": "",
            "projects": "",
            "certifications": ""
        }
        
        section_patterns = {
            "summary": r"(summary|objective|profile|about me|professional summary)",
            "skills": r"(skills|technical skills|key competencies|core competencies|technologies|expertise)",
            "experience": r"(experience|work experience|employment|history|professional experience|internships)",
            "education": r"(education|academic background|qualifications|degrees)",
            "projects": r"(projects|key projects|academic projects|personal projects)",
            "certifications": r"(certifications|licenses|courses|certificates|achievements)"
        }

        lines = text.split("\n")
        current_section = "summary"
        
        for line in lines:
            line_lower = line.lower().strip()
            # Check if header line
            if len(line_lower) < 40:
                found_match = False
                for sec_name, pattern in section_patterns.items():
                    if re.search(r"^" + pattern + r"[:\s]*$", line_lower, re.IGNORECASE) or line_lower == sec_name:
                        current_section = sec_name
                        found_match = True
                        break
                if found_match:
                    continue

            sections[current_section] += line + "\n"

        return {k: v.strip() for k, v in sections.items()}
