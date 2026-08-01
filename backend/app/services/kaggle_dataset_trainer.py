import csv
import io
import os
from typing import Any, Dict, List

from app.services.nlp_engine import nlp
from app.services.resume_parser import ResumeParser
from app.services.resume_quality_pipeline import resume_quality_pipeline
from app.services.vector_store import faiss_vector_store


class KaggleDatasetTrainer:
    """
    Bulk Kaggle Resume Dataset Ingestion & Model Training Pipeline.
    Supports CSV datasets (e.g. Resume.csv) & Directory of PDF/DOCX resumes.
    Bulk parses, extracts NLP skills, computes ATS quality metrics, and indexes into FAISS Vector Store.
    """

    @classmethod
    def train_from_csv_bytes(cls, csv_content: bytes, max_rows: int = 500) -> Dict[str, Any]:
        text_stream = io.StringIO(csv_content.decode("utf-8", errors="ignore"))
        reader = csv.DictReader(text_stream)

        trained_count = 0
        categories_map: Dict[str, int] = {}
        all_skills: Dict[str, int] = {}
        total_ats_score = 0.0
        docs_to_index: List[Dict[str, Any]] = []

        for i, row in enumerate(reader):
            if i >= max_rows:
                break

            # Find resume text column (Resume_str, resume_text, Text, Resume)
            resume_text = row.get("Resume_str") or row.get("resume_text") or row.get("Text") or row.get("Resume") or ""
            category = row.get("Category") or row.get("category") or "General Software"

            if not resume_text.strip():
                continue

            cleaned_text = ResumeParser.clean_text(resume_text)
            extracted_skills = nlp.extract_skills(cleaned_text)
            quality_res = resume_quality_pipeline.analyze(cleaned_text)
            ats_score = quality_res["overall_quality_score"]

            total_ats_score += ats_score
            categories_map[category] = categories_map.get(category, 0) + 1

            for skill in extracted_skills:
                all_skills[skill] = all_skills.get(skill, 0) + 1

            trained_count += 1
            docs_to_index.append(
                {
                    "id": f"kaggle-{trained_count}",
                    "category": category,
                    "content": cleaned_text[:500],
                    "skills": extracted_skills,
                    "ats_score": ats_score,
                }
            )

        # Bulk index into FAISS Vector Database
        faiss_vector_store.add_documents(docs_to_index)

        sorted_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:15]
        avg_score = round(total_ats_score / trained_count, 1) if trained_count > 0 else 0.0

        return {
            "status": "success",
            "total_resumes_trained": trained_count,
            "average_ats_score": avg_score,
            "categories_discovered_count": len(categories_map),
            "category_distribution": categories_map,
            "top_skills_extracted": [s[0] for s in sorted_skills],
            "faiss_total_vectors_indexed": len(faiss_vector_store.documents),
            "message": f"Successfully ingested and trained {trained_count} Kaggle resumes into FAISS Vector Store.",
        }

    @classmethod
    def train_from_pdf_directory(cls, dir_path: str, max_files: int = 200) -> Dict[str, Any]:
        if not os.path.exists(dir_path):
            return {"status": "error", "message": f"Directory '{dir_path}' does not exist."}

        files = [f for f in os.listdir(dir_path) if f.lower().endswith((".pdf", ".docx"))][:max_files]
        trained_count = 0
        total_ats_score = 0.0
        docs_to_index: List[Dict[str, Any]] = []

        for filename in files:
            full_path = os.path.join(dir_path, filename)
            parsed = ResumeParser.parse_file(full_path, filename)
            raw_text = parsed["raw_text"]
            if not raw_text.strip():
                continue

            extracted_skills = nlp.extract_skills(raw_text)
            quality_res = resume_quality_pipeline.analyze(raw_text)
            ats_score = quality_res["overall_quality_score"]

            total_ats_score += ats_score
            trained_count += 1

            docs_to_index.append(
                {
                    "id": f"kaggle-pdf-{trained_count}",
                    "filename": filename,
                    "content": raw_text[:500],
                    "skills": extracted_skills,
                    "ats_score": ats_score,
                }
            )

        faiss_vector_store.add_documents(docs_to_index)
        avg_score = round(total_ats_score / trained_count, 1) if trained_count > 0 else 0.0

        return {
            "status": "success",
            "total_resumes_trained": trained_count,
            "average_ats_score": avg_score,
            "faiss_total_vectors_indexed": len(faiss_vector_store.documents),
            "message": f"Successfully processed and indexed {trained_count} PDF/DOCX resumes from directory.",
        }


kaggle_trainer = KaggleDatasetTrainer()
