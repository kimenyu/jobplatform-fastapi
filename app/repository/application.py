from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.schemas.application import ApplicationResponse
from app.repository.application import create_application
import shutil
import os
import uuid

router = APIRouter(prefix="/applications", tags=["Applications"])

UPLOAD_DIR = "app/uploads/resumes"

@router.post("/upload", response_model=ApplicationResponse)
async def upload_resume(
    job_id: int = Form(...),
    cover_letter: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file to disk
    file_extension = os.path.splitext(resume.filename)[1]
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Create application
    application_data = {
        "job_id": job_id,
        "cover_letter": cover_letter,
        "resume_file_path": file_path
    }

    return create_application(db, current_user.id, application=type("AppCreate", (), application_data)())


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
