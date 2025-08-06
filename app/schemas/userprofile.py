from typing import Optional

from pydantic import BaseModel


class UserProfileBase(BaseModel):
    full_name: str
    bio: str
    linkedin: str
    github: str
    website: str

class UserProfileCreate(UserProfileBase):
    pass


class ShowUserProfile(UserProfileBase):
    id: int

    class Config:
        orm_mode=True


class UpdateProfile(BaseModel):
    full_name: Optional[str]
    bio: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    website: Optional[str]
