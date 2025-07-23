from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdateStatus
from app.core.dependencies import get_db, get_current_user, require_role
from app.repository import application as application_repo
import shutil
import os
import uuid

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/create/", response_model=ApplicationResponse)
def apply_for_job(
    job_id: int = Form(...),
    cover_letter: str = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_role("applicant"))
):
    filename = f"{uuid.uuid4()}_{resume.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save resume: {str(e)}")

    application_data = ApplicationCreate(
        job_id=job_id,
        cover_letter=cover_letter,
        resume_file_path=file_path
    )

    return application_repo.create_application(db, current_user.id, application_data)


@router.get("/{app_id}/", response_model=ApplicationResponse)
def get_application(app_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return application_repo.get_application_detail(db, app_id)


@router.get("/job/{job_id}/", response_model=List[ApplicationResponse])
def get_applications_for_job(job_id: int, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    return application_repo.get_applications_by_job(db, job_id)


@router.get("/user/me/", response_model=List[ApplicationResponse])
def get_my_applications(db: Session = Depends(get_db), current_user=Depends(require_role("applicant"))):
    return application_repo.get_applications_by_user(db, current_user.id)


@router.patch("/{app_id}/status", response_model=ApplicationResponse)
def update_status(app_id: int, status_data: ApplicationUpdateStatus, db: Session = Depends(get_db), current_user=Depends(require_role("employer"))):
    return application_repo.update_application_status(db, app_id, status_data)


@router.delete("/{app_id}/")
def delete_application(app_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    is_admin = current_user.role == "admin"
    return application_repo.delete_application(db, app_id, current_user.id, is_admin)
