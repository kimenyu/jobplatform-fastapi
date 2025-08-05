from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.repository.applicationwithresumeparser import ApplicationWithResumeRepository
from app.core.dependencies import get_current_user, get_current_employer, get_db
from app.models.user import User

router = APIRouter(prefix="/applications", tags=["Applications with Resume Parser"])


# Pydantic models for request/response
class StatusUpdateRequest(BaseModel):
    status: str


# Test endpoint to verify the route is working
@router.get("/test")
async def test_endpoint():
    return {"message": "Application routes are working"}


@router.post("/submit")
async def submit_application_with_resume(
    job_id: int = Form(...),
    cover_letter: Optional[str] = Form(None),
    resume_file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit job application with resume upload and automatic parsing
    """
    print(f"Received file: {resume_file.filename}")
    print(f"File content type: {resume_file.content_type}")
    print(f"Job ID: {job_id}")
    print(f"User ID: {current_user.id}")

    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.doc']
    if not resume_file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_extension = '.' + resume_file.filename.split('.')[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )

    # Validate file size (e.g., max 10MB)
    if hasattr(resume_file, 'size') and resume_file.size and resume_file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size too large. Maximum 10MB allowed.")

    repo = ApplicationWithResumeRepository(db)

    try:
        result = repo.create_application_with_resume(
            job_id=job_id,
            applicant_id=current_user.id,
            resume_file=resume_file,
            cover_letter=cover_letter
        )
        return result
    except Exception as e:
        print(f"Error in submit_application_with_resume: {str(e)}")
        raise


@router.get("/my-applications")
async def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all applications submitted by the current user with parsed resume data
    """
    repo = ApplicationWithResumeRepository(db)
    applications = repo.get_user_applications_with_resumes(current_user.id)

    return applications


@router.get("/{application_id}")
async def get_application_details(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed application information including parsed resume
    """
    repo = ApplicationWithResumeRepository(db)
    application = repo.get_application_with_parsed_resume(application_id, current_user.id)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@router.get("/job/{job_id}/applications")
async def get_job_applications(
    job_id: int,
    current_user: User = Depends(get_current_employer),
    db: Session = Depends(get_db)
):
    """
    Get all applications for a specific job (for employers)
    """
    repo = ApplicationWithResumeRepository(db)
    applications = repo.get_job_applications_with_resumes(job_id, current_user.id)

    return applications


@router.patch("/{application_id}/status")
async def update_application_status(
    application_id: int,
    status_update: StatusUpdateRequest,
    current_user: User = Depends(get_current_employer),
    db: Session = Depends(get_db)
):
    """
    Update application status (for employers)
    """
    repo = ApplicationWithResumeRepository(db)
    success = repo.update_application_status(
        application_id=application_id,
        new_status=status_update.status,
        employer_id=current_user.id
    )

    if not success:
        raise HTTPException(status_code=404, detail="Application not found or not authorized")

    return {"message": f"Application status updated to {status_update.status}"}


@router.post("/{application_id}/reparse")
async def reparse_resume(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reparse an existing resume file (useful if parser logic is updated)
    """
    repo = ApplicationWithResumeRepository(db)

    # Check if user owns this application
    application = repo.get_application_with_parsed_resume(application_id, current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    result = repo.reparse_resume(application_id)
    return result


@router.delete("/{application_id}")
async def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an application (only if it's in pending status)
    """
    repo = ApplicationWithResumeRepository(db)

    # First check the application status
    application = repo.get_application_with_parsed_resume(application_id, current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    if application["status"] != "pending":
        raise HTTPException(
            status_code=400,
            detail="Cannot delete application that has been reviewed"
        )

    success = repo.delete_application(application_id, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Application not found")

    return {"message": "Application deleted successfully"}


@router.get("/skills/analysis/{job_id}")
async def analyze_skills_for_job(
    job_id: int,
    current_user: User = Depends(get_current_employer),
    db: Session = Depends(get_db)
):
    """
    Analyze skills from all applicants for a specific job
    """
    repo = ApplicationWithResumeRepository(db)
    applications = repo.get_job_applications_with_resumes(job_id, current_user.id)

    # Analyze skills across all applications
    all_skills = []
    skill_frequency = {}

    for app in applications:
        if app.get("parsed_resume") and app["parsed_resume"].get("skills"):
            skills = app["parsed_resume"]["skills"]
            all_skills.extend(skills)

            for skill in skills:
                skill_lower = skill.lower().strip()
                skill_frequency[skill_lower] = skill_frequency.get(skill_lower, 0) + 1

    # Sort skills by frequency
    sorted_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)

    return {
        "job_id": job_id,
        "total_applications": len(applications),
        "unique_skills_count": len(skill_frequency),
        "most_common_skills": sorted_skills[:20],  # Top 20 skills
        "skills_distribution": skill_frequency
    }


@router.get("/resume/preview/{application_id}")
async def get_resume_preview(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a preview of the extracted resume text (first 1000 characters)
    """
    repo = ApplicationWithResumeRepository(db)
    application = repo.get_application_with_parsed_resume(application_id, current_user.id)

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    parsed_resume = application.get("parsed_resume", {})
    extracted_text = parsed_resume.get("extracted_text", "No text available")

    return {
        "application_id": application_id,
        "preview_text": extracted_text,
        "parsing_summary": {
            "name": parsed_resume.get("name"),
            "email": parsed_resume.get("email"),
            "phone": parsed_resume.get("mobile_number"),
            "skills_count": len(parsed_resume.get("skills", [])),
            "education_count": len(parsed_resume.get("education", [])),
            "pages": parsed_resume.get("no_of_pages")
        }
    }