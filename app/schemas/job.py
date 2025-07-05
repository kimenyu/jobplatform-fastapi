# schemas/job.py
from typing import List, Optional
from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    description: str
    location: str
    company_name: str
    skills_required: List[str]

class JobCreate(JobBase):
    pass

class UpdateJobs(BaseModel):
    title: Optional[str]
    description: Optional[str]
    location: Optional[str]
    company_name: Optional[str]
    skills_required: Optional[List[str]]

class ShowJobs(JobBase):
    id: int
    posted_by: int

    class Config:
        orm_mode = True
