from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from fastapi import HTTPException, status
from typing import List, Optional
from app.models.application import Application
from app.models.resume import Resume
from app.schemas.application import ApplicationCreate, ApplicationUpdateStatus
import os


def create_application(
        db: Session,
        applicant_id: int,
        application: ApplicationCreate,
        resume_id: Optional[int] = None
):
    """Create a new job application"""
    try:
        # If resume_id is provided, get the resume file path
        resume_file_path = None
        parsed_resume = None

        if resume_id:
            resume = db.query(Resume).filter(
                and_(
                    Resume.id == resume_id,
                    Resume.applicant_id == applicant_id
                )
            ).first()

            if not resume:
                raise HTTPException(
                    status_code=404,
                    detail="Resume not found or not authorized"
                )

            resume_file_path = resume.file_path
            parsed_resume = resume.parsed_data

            # Verify file still exists
            if not os.path.isfile(resume_file_path):
                raise HTTPException(
                    status_code=400,
                    detail="Resume file no longer exists"
                )

        elif application.resume_file_path:
            # Legacy support for direct file path
            if not os.path.isfile(application.resume_file_path):
                raise HTTPException(
                    status_code=400,
                    detail="Resume file not found"
                )
            resume_file_path = application.resume_file_path

        else:
            raise HTTPException(
                status_code=400,
                detail="Either resume_id or resume_file_path must be provided"
            )

        new_application = Application(
            job_id=application.job_id,
            applicant_id=applicant_id,
            resume_file_path=resume_file_path,
            cover_letter=application.cover_letter,
            parsed_resume=parsed_resume,
        )

        db.add(new_application)
        db.commit()
        db.refresh(new_application)
        return new_application

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete application: {str(e)}"
        )


def get_applications_by_status(
        db: Session,
        status: str,
        skip: int = 0,
        limit: int = 20
) -> List[Application]:
    """Get applications by status (recruiter/admin only)"""
    return db.query(Application).filter(
        Application.status == status
    ).order_by(desc(Application.created_at)).offset(skip).limit(limit).all()


def search_applications(
        db: Session,
        job_id: Optional[int] = None,
        applicant_id: Optional[int] = None,
        status: Optional[str] = None,
        field: Optional[str] = None,
        skills: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 20
) -> dict:
    """Advanced search for applications"""
    try:
        query = db.query(Application)

        # Apply basic filters
        if job_id:
            query = query.filter(Application.job_id == job_id)
        if applicant_id:
            query = query.filter(Application.applicant_id == applicant_id)
        if status:
            query = query.filter(Application.status == status)

        # Apply resume-based filters
        if field:
            query = query.filter(
                Application.parsed_resume['field'].astext.ilike(f"%{field}%")
            )

        if skills:
            skill_conditions = []
            for skill in skills:
                skill_conditions.append(
                    Application.parsed_resume['skills'].astext.ilike(f"%{skill}%")
                )
            if skill_conditions:
                from sqlalchemy import or_
                query = query.filter(or_(*skill_conditions))

        # Get total count
        total = query.count()

        # Apply pagination
        applications = query.order_by(desc(Application.created_at)).offset(skip).limit(limit).all()

        return {
            "applications": applications,
            "total": total,
            "page": (skip // limit) + 1 if limit > 0 else 1,
            "pages": (total + limit - 1) // limit if limit > 0 else 1
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search applications: {str(e)}"
        )



def get_application_by_id(db: Session, application_id: int) -> Optional[Application]:
    """Get application by ID"""
    return db.query(Application).filter(Application.id == application_id).first()


def get_user_applications(
        db: Session,
        applicant_id: int,
        skip: int = 0,
        limit: int = 10
) -> List[Application]:
    """Get all applications for a specific user"""
    return db.query(Application).filter(
        Application.applicant_id == applicant_id
    ).order_by(desc(Application.created_at)).offset(skip).limit(limit).all()


def get_job_applications(
        db: Session,
        job_id: int,
        skip: int = 0,
        limit: int = 20
) -> List[Application]:
    """Get all applications for a specific job"""
    return db.query(Application).filter(
        Application.job_id == job_id
    ).order_by(desc(Application.created_at)).offset(skip).limit(limit).all()


def update_application_status(
        db: Session,
        application_id: int,
        status_update: ApplicationUpdateStatus
) -> Optional[Application]:
    """Update application status (recruiter/admin only)"""
    try:
        application = db.query(Application).filter(
            Application.id == application_id
        ).first()

        if not application:
            return None

        application.status = status_update.status

        db.commit()
        db.refresh(application)
        return application

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update application status: {str(e)}"
        )


def delete_application(db: Session, application_id: int, applicant_id: int) -> bool:
    """Delete an application (applicant only, and only if pending)"""
    try:
        application = db.query(Application).filter(
            and_(
                Application.id == application_id,
                Application.applicant_id == applicant_id
            )
        ).first()

        if not application:
            return False

        # Only allow deletion if application is still pending
        if application.status != "pending":
            raise HTTPException(
                status_code=400,
                detail="Cannot delete application that has been reviewed"
            )

        db.delete(application)
        db.commit()
        return True

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()