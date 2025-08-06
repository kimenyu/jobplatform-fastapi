from pydantic import BaseModel, conint
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: conint(ge=1, le=5)  # restrict between 1–5
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    reviewee_id: int

class ReviewUpdate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    reviewer_id: int
    reviewee_id: int
    created_at: datetime

    class Config:
        orm_mode = True
