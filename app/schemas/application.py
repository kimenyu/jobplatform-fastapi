# app/schemas/application.py

from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class ApplicationCreate(BaseModel):
    job_id: int
    resume_file_path: Optional[str] = None
    cover_letter: Optional[str] = None
    parsed_resume: Optional[dict] = None  # Assuming it's a parsed JSON resume

class ApplicationUpdateStatus(BaseModel):
    status: Literal["pending", "reviewed", "rejected"]

class ShowApplication(BaseModel):
    id: int
    job_id: int
    applicant_id: int
    resume_file_path: Optional[str]
    cover_letter: Optional[str]
    parsed_resume: Optional[dict]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
