from http.client import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app.models.userprofile import  UserProfile
from app.schemas.userprofile import UserProfileCreate, UpdateProfile


def create_profile(db: Session, userprofile: UserProfileCreate, userID: int):
    new_profile = UserProfile(
        user_id=userID,
        full_name=userprofile.full_name,
        bio=userprofile.bio,
        linkedin=userprofile.linkedin,
        github=userprofile.github,
        website=userprofile.website
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

def get_profile_details(id: int, db:Session, current_user):
    profile = db.query(UserProfile).filter(UserProfile.id == id).fist()
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile with id {id} not found")
    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, details="Not authorized to view this")
    return profile

def update_profile(id: int, profile_data: UpdateProfile, db:Session, current_user):
    profile = db.query(UserProfile).filter(UserProfile.id == id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, details="Not authorized to update this profile")

    for key, value in profile_data.dict(exclude_unser=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile

def delete_profile(id: int, db: Session, current_user):
    profile = db.query(UserProfile).filter(UserProfile.id == id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this profile")

    db.delete(profile)
    db.commit()
    return {"message": 'Profile deleted'}