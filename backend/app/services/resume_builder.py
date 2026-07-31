import os
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.core.config import settings

class ResumeBuilderService:

    @classmethod
    def generate_resume_pdf(cls, data: Dict[str, Any], template_name: str = "Modern") -> str:
        full_name = data.get("full_name", "Candidate Name")
        pdf_filename = f"Resume_Builder_{full_name.replace(' ', '_')}.pdf"
        output_path = os.path.join(settings.REPORTS_DIR, pdf_filename)

        doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()

        PRIMARY_COLOR = colors.HexColor("#4F46E5") if template_name == "Modern" else colors.HexColor("#1F2937")

        name_style = ParagraphStyle("RName", parent=styles["Title"], fontSize=20, leading=24, textColor=PRIMARY_COLOR, alignment=0)
        contact_style = ParagraphStyle("RContact", parent=styles["Normal"], fontSize=9, textColor=colors.HexColor("#4B5563"))
        heading_style = ParagraphStyle("RHeading", parent=styles["Heading2"], fontSize=13, leading=16, textColor=PRIMARY_COLOR, spaceBefore=10, spaceAfter=4)
        body_style = ParagraphStyle("RBody", parent=styles["Normal"], fontSize=9.5, leading=13, textColor=colors.HexColor("#111827"))

        story = []

        # Name & Contact Header
        story.append(Paragraph(f"<b>{full_name}</b>", name_style))
        contact_info = f"{data.get('email', '')} | {data.get('phone', '')} | {data.get('linkedin', '')} | {data.get('github', '')}"
        story.append(Paragraph(contact_info, contact_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY_COLOR, spaceAfter=10, spaceBefore=5))

        # Summary
        if data.get("summary"):
            story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
            story.append(Paragraph(data["summary"], body_style))
            story.append(Spacer(1, 8))

        # Skills
        if data.get("skills"):
            story.append(Paragraph("TECHNICAL & CORE SKILLS", heading_style))
            skills_str = ", ".join(data["skills"]) if isinstance(data["skills"], list) else str(data["skills"])
            story.append(Paragraph(f"<b>Skills:</b> {skills_str}", body_style))
            story.append(Spacer(1, 8))

        # Experience
        if data.get("experience"):
            story.append(Paragraph("WORK EXPERIENCE", heading_style))
            for exp in data["experience"]:
                title_line = f"<b>{exp.get('role', 'Role')}</b> — <i>{exp.get('company', 'Company')}</i> ({exp.get('duration', '')})"
                story.append(Paragraph(title_line, body_style))
                if exp.get("bullets"):
                    for b in exp["bullets"]:
                        story.append(Paragraph(f"• {b}", body_style))
                story.append(Spacer(1, 4))
            story.append(Spacer(1, 4))

        # Education
        if data.get("education"):
            story.append(Paragraph("EDUCATION", heading_style))
            for edu in data["education"]:
                edu_line = f"<b>{edu.get('degree', 'Degree')}</b> — {edu.get('institution', 'University')} ({edu.get('year', '')})"
                story.append(Paragraph(edu_line, body_style))
            story.append(Spacer(1, 8))

        doc.build(story)
        return output_path
