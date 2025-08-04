# app/routers/applications.py - Updated
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.resume import (
    ApplicationCreate, ApplicationResponse, ApplicationUpdateStatus,
    ApplicationSearchFilters, ApplicationSearchResponse
)
from app.core.dependencies import get_db, get_current_user, require_role
from app.repository import application as application_repo
from app.repository import applicationwithresumeparser as resume_repo
from app.utils.resume_parser import ResumeParser
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
        resume_id: Optional[int] = Form(None),
        resume: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db),
        current_user=Depends(require_role("applicant"))
):
    """Apply for a job using existing resume or uploading new one"""

    # Must provide either resume_id or resume file
    if not resume_id and not resume:
        raise HTTPException(
            status_code=400,
            detail="Either resume_id or resume file must be provided"
        )

    if resume_id and resume:
        raise HTTPException(
            status_code=400,
            detail="Provide either resume_id or resume file, not both"
        )

    # If uploading new resume
    if resume:
        # Validate file type
        allowed_extensions = {'.pdf', '.docx', '.doc'}
        file_extension = os.path.splitext(resume.filename)[1].lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and DOCX files are supported"
            )

        # Validate file size (5MB limit)
        if resume.size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size must be less than 5MB"
            )

        # Generate unique filename and save
        filename = f"{uuid.uuid4()}_{resume.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(resume.file, buffer)

            # Parse resume
            parser = ResumeParser(file_path)
            parsed_data = parser.get_extracted_data()

            # Create resume record first
            from app.schemas.resume import ResumeCreate
            resume_data = ResumeCreate(
                file_path=file_path,
                parsed_data=parsed_data
            )

            created_resume = resume_repo.create_resume(
                db=db,
                resume_data=resume_data,
                applicant_id=current_user.id
            )

            resume_id = created_resume.id

        except Exception as e:
            # Clean up file if error occurred
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process resume: {str(e)}"
            )

    # Create application
    application_data = ApplicationCreate(
        job_id=job_id,
        cover_letter=cover_letter
    )

    return application_repo.create_application(
        db=db,
        applicant_id=current_user.id,
        application=application_data,
        resume_id=resume_id
    )


@router.get("/my-applications/", response_model=List[ApplicationResponse])
def get_my_applications(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=50),
        db: Session = Depends(get_db),
        current_user=Depends(require_role("applicant"))
):
    """Get current user's applications"""
    applications = application_repo.get_user_applications(
        db=db,
        applicant_id=current_user.id,
        skip=skip,
        limit=limit
    )
    return applications


@router.get("/{application_id}/", response_model=ApplicationResponse)
def get_application(
        application_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """Get a specific application by ID"""
    application = application_repo.get_application_by_id(
        db=db,
        application_id=application_id
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    # Check permissions
    if (current_user.role == "applicant" and
            application.applicant_id != current_user.id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to view this application"
        )

    return application


@router.delete("/{application_id}/")
def delete_application(
        application_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_role("applicant"))
):
    """Delete an application (only if pending)"""
    success = application_repo.delete_application(
        db=db,
        application_id=application_id,
        applicant_id=current_user.id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Application not found or not authorized"
        )

    return {"message": "Application deleted successfully"}


# Recruiter/Admin endpoints
@router.get("/job/{job_id}/applications/", response_model=List[ApplicationResponse])
def get_job_applications(
        job_id: int,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user=Depends(require_role(["admin", "recruiter"]))
):
    """Get all applications for a specific job"""
    applications = application_repo.get_job_applications(
        db=db,
        job_id=job_id,
        skip=skip,
        limit=limit
    )
    return applications


@router.put("/{application_id}/status/", response_model=ApplicationResponse)
def update_application_status(
        application_id: int,
        status_update: ApplicationUpdateStatus,
        db: Session = Depends(get_db),
        current_user=Depends(require_role(["admin", "recruiter"]))
):
    """Update application status"""
    updated_application = application_repo.update_application_status(
        db=db,
        application_id=application_id,
        status_update=status_update
    )

    if not updated_application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return updated_application


@router.get("/status/{status}/", response_model=List[ApplicationResponse])
def get_applications_by_status(
        status: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user=Depends(require_role(["admin", "recruiter"]))
):
    """Get applications by status"""
    applications = application_repo.get_applications_by_status(
        db=db,
        status=status,
        skip=skip,
        limit=limit
    )
    return applications


@router.post("/search/", response_model=ApplicationSearchResponse)
def search_applications(
        filters: ApplicationSearchFilters,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        db: Session = Depends(get_db),
        current_user=Depends(require_role(["admin", "recruiter"]))
):
    """Search applications with advanced filters"""
    result = application_repo.search_applications(
        db=db,
        job_id=filters.job_id,
        applicant_id=filters.applicant_id,
        status=filters.status,
        field=filters.field,
        skills=filters.skills,
        skip=skip,
        limit=limit
    )

    return ApplicationSearchResponse(
        applications=result["applications"],
        total=result["total"],
        page=result["page"],
        pages=result["pages"]
    )


@router.get("/download-resume/{application_id}/")
def download_application_resume(
        application_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(require_role(["admin", "recruiter"]))
):
    """Download resume file from application"""
    from fastapi.responses import FileResponse

    application = application_repo.get_application_by_id(
        db=db,
        application_id=application_id
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    if not application.resume_file_path or not os.path.exists(application.resume_file_path):
        raise HTTPException(
            status_code=404,
            detail="Resume file not found"
        )

    filename = os.path.basename(application.resume_file_path)
    return FileResponse(
        path=application.resume_file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


