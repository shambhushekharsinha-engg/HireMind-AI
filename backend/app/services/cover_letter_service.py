from typing import Any, Dict

from app.services.nlp_engine import NLPEngine


class CoverLetterService:
    @classmethod
    def generate_cover_letter(
        cls,
        candidate_name: str,
        company_name: str,
        job_title: str,
        resume_text: str,
        job_description: str,
    ) -> Dict[str, Any]:
        skills = NLPEngine.extract_skills(resume_text or "")
        top_skills = ", ".join(skills[:4]) if skills else "software engineering, Python, and scalable system design"

        salutation = f"Dear Hiring Team at {company_name or 'the Organization'},"

        opening = (
            f"I am writing to express my strong enthusiasm for the {job_title or 'Software Engineer'} position at {company_name or 'your company'}. "
            f"With a proven background in building production-ready applications and technical expertise spanning {top_skills}, "
            f"I am eager to contribute to {company_name}'s engineering initiatives and product innovation."
        )

        body_paragraph = (
            "Throughout my technical journey, I have focused on building scalable, reliable, and user-centric software solutions. "
            "My technical toolset aligns closely with the qualifications outlined in your job posting. "
            "I thrive in fast-paced collaborative environments, leveraging data-driven decision making, clean code practices, and continuous integration to deliver tangible impact."
        )

        closing = (
            f"Thank you for your time and consideration. I welcome the opportunity to discuss how my technical skills and passion "
            f"for high-quality engineering make me a strong fit for the {job_title or 'position'} at {company_name}."
        )

        sign_off = f"Sincerely,\n{candidate_name or 'Applicant'}"

        full_letter = f"{salutation}\n\n{opening}\n\n{body_paragraph}\n\n{closing}\n\n{sign_off}"

        return {
            "candidate_name": candidate_name,
            "company_name": company_name,
            "job_title": job_title,
            "cover_letter_text": full_letter,
            "highlighted_skills": skills[:4],
        }
