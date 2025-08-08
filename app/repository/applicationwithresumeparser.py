import os
import shutil
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from app.models.application import Application
from app.models.resume import Resume
from app.models.job import Job
from app.models.user import User
from app.utils.resume_parser import ResumeParser


class ApplicationWithResumeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_application_with_resume(
            self,
            job_id: int,
            applicant_id: int,
            resume_file: UploadFile,
            cover_letter: Optional[str] = None,
            upload_dir: str = "uploads/resumes"
    ) -> Dict:
        """Create application and parse resume in one operation"""

        # Verify job exists
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        # Verify user exists
        user = self.db.query(User).filter(User.id == applicant_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if user already applied for this job
        existing_application = self.db.query(Application).filter(
            Application.job_id == job_id,
            Application.applicant_id == applicant_id
        ).first()

        if existing_application:
            raise HTTPException(status_code=400, detail="You have already applied for this job")

        try:
            # Create upload directory if it doesn't exist
            os.makedirs(upload_dir, exist_ok=True)

            # Generate unique filename
            file_extension = resume_file.filename.split('.')[-1]
            unique_filename = f"resume_{applicant_id}_{job_id}.{file_extension}"
            file_path = os.path.join(upload_dir, unique_filename)

            # Save the uploaded file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(resume_file.file, buffer)

            # Parse the resume
            parser = ResumeParser(file_path)
            parsed_data = parser.get_extracted_data()

            # Check if parsing was successful
            if "error" in parsed_data:
                # Clean up the uploaded file on parsing error
                if os.path.exists(file_path):
                    os.remove(file_path)
                raise HTTPException(status_code=422, detail=f"Resume parsing failed: {parsed_data['error']}")

            # Create resume record
            resume = Resume(
                applicant_id=applicant_id,
                file_path=file_path,
                parsed_data=parsed_data
            )
            self.db.add(resume)
            self.db.flush()  # Get the resume ID

            # Create application record
            application = Application(
                job_id=job_id,
                applicant_id=applicant_id,
                resume_file_path=file_path,
                cover_letter=cover_letter,
                parsed_resume=parsed_data,
                status="pending"
            )
            self.db.add(application)

            # Commit both records
            self.db.commit()
            self.db.refresh(application)
            self.db.refresh(resume)

            return {
                "application_id": application.id,
                "resume_id": resume.id,
                "parsed_data": parsed_data,
                "status": "success",
                "message": "Application submitted and resume parsed successfully"
            }

        except Exception as e:
            self.db.rollback()
            # Clean up uploaded file on error
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=f"Failed to process application: {str(e)}")

    def get_application_with_parsed_resume(self, application_id: int, user_id: Optional[int] = None) -> Optional[Dict]:
        """Get application with parsed resume data"""
        query = self.db.query(Application).filter(Application.id == application_id)

        if user_id:
            query = query.filter(Application.applicant_id == user_id)

        application = query.first()
        if not application:
            return None

        return {
            "id": application.id,
            "job_id": application.job_id,
            "applicant_id": application.applicant_id,
            "status": application.status,
            "cover_letter": application.cover_letter,
            "parsed_resume": application.parsed_resume,
            "created_at": application.created_at,
            "job_title": application.job.title if application.job else None,
            "applicant_name": application.applicant.email if application.applicant else None
        }

    def get_user_applications_with_resumes(self, user_id: int) -> List[Dict]:
        """Get all applications for a user with parsed resume data"""
        applications = self.db.query(Application).filter(
            Application.applicant_id == user_id
        ).all()

        return [
            {
                "id": app.id,
                "job_id": app.job_id,
                "job_title": app.job.title if app.job else None,
                "company_name": app.job.company_name if app.job else None,
                "status": app.status,
                "parsed_resume": app.parsed_resume,
                "created_at": app.created_at
            }
            for app in applications
        ]

    def get_job_applications_with_resumes(self, job_id: int, employer_id: Optional[int] = None) -> List[Dict]:
        """Get all applications for a job with parsed resume data"""
        query = self.db.query(Application).filter(Application.job_id == job_id)

        # If employer_id is provided, verify they own the job
        if employer_id:
            job = self.db.query(Job).filter(
                Job.id == job_id,
                Job.posted_by == employer_id
            ).first()
            if not job:
                raise HTTPException(status_code=403, detail="Not authorized to view these applications")

        applications = query.all()

        return [
            {
                "id": app.id,
                "applicant_id": app.applicant_id,
                "applicant_name": app.applicant.email if app.applicant else None,
                "applicant_email": app.applicant.email if app.applicant else None,
                "status": app.status,
                "cover_letter": app.cover_letter,
                "parsed_resume": app.parsed_resume,
                "created_at": app.created_at
            }
            for app in applications
        ]

    def update_application_status(self, application_id: int, new_status: str,
                                  employer_id: Optional[int] = None) -> bool:
        """Update application status"""
        valid_statuses = ["pending", "reviewed", "accepted", "rejected"]
        if new_status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

        query = self.db.query(Application).filter(Application.id == application_id)

        # If employer_id provided, verify they own the job
        if employer_id:
            query = query.join(Job).filter(Job.employer_id == employer_id)

        application = query.first()
        if not application:
            return False

        application.status = new_status
        self.db.commit()
        return True

    def reparse_resume(self, application_id: int) -> Dict:
        """Reparse an existing resume file"""
        application = self.db.query(Application).filter(Application.id == application_id).first()
        if not application or not application.resume_file_path:
            raise HTTPException(status_code=404, detail="Application or resume file not found")

        if not os.path.exists(application.resume_file_path):
            raise HTTPException(status_code=404, detail="Resume file no longer exists")

        try:
            # Reparse the resume
            parser = ResumeParser(application.resume_file_path)
            parsed_data = parser.get_extracted_data()

            if "error" in parsed_data:
                raise HTTPException(status_code=422, detail=f"Resume parsing failed: {parsed_data['error']}")

            # Update application with new parsed data
            application.parsed_resume = parsed_data

            # Update resume record if it exists
            resume = self.db.query(Resume).filter(
                Resume.applicant_id == application.applicant_id,
                Resume.file_path == application.resume_file_path
            ).first()

            if resume:
                resume.parsed_data = parsed_data

            self.db.commit()

            return {
                "status": "success",
                "message": "Resume reparsed successfully",
                "parsed_data": parsed_data
            }

        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to reparse resume: {str(e)}")

    def delete_application(self, application_id: int, user_id: int) -> bool:
        """Delete application and associated resume file"""
        application = self.db.query(Application).filter(
            Application.id == application_id,
            Application.applicant_id == user_id
        ).first()

        if not application:
            return False

        # Remove file if it exists
        if application.resume_file_path and os.path.exists(application.resume_file_path):
            try:
                os.remove(application.resume_file_path)
            except OSError:
                pass  # File might be in use or already deleted

        # Delete from database
        self.db.delete(application)
        self.db.commit()
        return True