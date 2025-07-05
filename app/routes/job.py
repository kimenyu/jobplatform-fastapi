from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.repository.job import create_job, list_jobs, get_job_details, delete_job, update_job
from app.core.dependencies import get_db, get_current_user
from app.schemas.job import JobCreate, ShowJobs, UpdateJobs
from app.models.user import User

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/create/", response_model=ShowJobs, status_code=status.HTTP_201_CREATED)
def create_new_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ["employer", "admin"]:
        raise HTTPException(status_code=403, detail="Only employers can post jobs")
    return create_job(db, job, current_user.id)

@router.get("/all/", response_model=List[ShowJobs], status_code=status.HTTP_200_OK)
def get_all_jobs(db: Session = Depends(get_db)):
    return list_jobs(db)

@router.get("/{id}", response_model=ShowJobs, status_code=status.HTTP_200_OK)
def get_a_job_detail(id: int, db: Session = Depends(get_db)):
    return get_job_details(id, db)

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_job(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_job(id, db, current_user)

@router.put("/update/{id}", response_model=ShowJobs, status_code=status.HTTP_202_ACCEPTED)
def update(
    id: int,
    job: UpdateJobs,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_job(id, job, db, current_user)
