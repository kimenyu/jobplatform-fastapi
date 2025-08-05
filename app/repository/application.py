import os
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdateStatus
from openai import OpenAI
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
import mimetypes


def extract_resume_text(file_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type == "application/pdf":
        return extract_pdf_text(file_path)
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type for resume")


def parse_resume_with_openai(text: str) -> dict:
    from openai import OpenAI
    import os
    import json

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""
    Extract the following structured JSON from the resume text:

    {{
        "name": "",
        "email": "",
        "phone": "",
        "education": [{{"degree": "", "institution": "", "year": ""}}],
        "experience": [{{"title": "", "company": "", "dates": "", "description": ""}}],
        "skills": []
    }}

    Resume text:
    \"\"\"{text}\"\"\"
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")



def create_application(db: Session, applicant_id: int, application: ApplicationCreate):
    if not os.path.isfile(application.resume_file_path):
        raise HTTPException(status_code=400, detail="Resume file not found")

    try:
        text = extract_resume_text(application.resume_file_path)
        parsed_resume = parse_resume_with_openai(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

    new_application = Application(
        job_id=application.job_id,
        applicant_id=applicant_id,
        resume_file_path=application.resume_file_path,
        cover_letter=application.cover_letter,
        parsed_resume=parsed_resume
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application


def get_application_detail(db: Session, app_id: int):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


def get_applications_by_job(db: Session, job_id: int):
    return db.query(Application).filter(Application.job_id == job_id).all()


def get_applications_by_user(db: Session, applicant_id: int):
    return db.query(Application).filter(Application.applicant_id == applicant_id).all()


def update_application_status(db: Session, app_id: int, status_data: ApplicationUpdateStatus):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    application.status = status_data.status
    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, app_id: int, current_user_id: int, is_admin=False):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application.applicant_id != current_user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this application")

    db.delete(application)
    db.commit()
    return {"detail": "Application deleted successfully"}