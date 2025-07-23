import os
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdateStatus
from pyresparser import ResumeParser


def create_application(db: Session, applicant_id: int, application: ApplicationCreate):
    parsed_resume = None

    if application.resume_file_path:
        file_path = application.resume_file_path

        if not os.path.isfile(file_path):
            raise HTTPException(status_code=400, detail="Resume file not found")

        try:
            parsed_resume = ResumeParser(file_path).get_extracted_data()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")

    new_application = Application(
        job_id=application.job_id,
        applicant_id=applicant_id,
        resume_file_path=application.resume_file_path,
        cover_letter=application.cover_letter,
        parsed_resume=parsed_resume,
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


def delete_application(db: Session, app_id: int, current_user_id: int, is_admin: bool = False):
    application = db.query(Application).filter(Application.id == app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application.applicant_id != current_user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to delete this application")

    db.delete(application)
    db.commit()
    return {"detail": "Application deleted successfully"}
