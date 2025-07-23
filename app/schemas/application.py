from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: str
    resume_file_path: Optional[str] = None  # path to uploaded file


class ApplicationUpdateStatus(BaseModel):
    status: Literal["pending", "reviewed", "rejected"]


class ApplicationResponse(BaseModel):
    id: int
    job_id: int
    applicant_id: int
    cover_letter: Optional[str]
    resume_file_path: Optional[str]
    parsed_resume: Optional[dict]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
