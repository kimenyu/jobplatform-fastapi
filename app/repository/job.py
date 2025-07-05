from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate, ShowJobs, UpdateJobs
from fastapi import HTTPException, status

def create_job(db: Session, job: JobCreate, employer_id: int):
    new_job = Job(
        title=job.title,
        description=job.description,
        location=job.location,
        company_name=job.company_name,
        skills_required=job.skills_required,
        posted_by=employer_id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

def list_jobs(db: Session):
    return db.query(Job).all()

def get_job_details(id: int, db: Session):
    job = db.query(Job).filter(Job.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job with id {id} not found")
    return job

def delete_job(id: int, db: Session, current_user):
    job = db.query(Job).filter(Job.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.posted_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}

def update_job(id: int, job_data: UpdateJobs, db: Session, current_user):
    job = db.query(Job).filter(Job.id == id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.posted_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this job")

    for key, value in job_data.dict(exclude_unset=True).items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)
    return job
