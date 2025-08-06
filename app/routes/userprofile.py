from fastapi import APIRouter, status, Depends, HTTPException
from app.models.userprofile import UserProfile
from app.models.user import User
from sqlalchemy.orm import Session
from app.repository.userprofile import create_profile, get_profile_details,update_profile, delete_profile
from app.schemas.userprofile import ShowUserProfile, UserProfileCreate,UpdateProfile
from app.core.dependencies import get_db, get_current_user


router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/create", response_model=ShowUserProfile, status_code=status.HTTP_201_CREATED)
def create_new_profile(userprofile: UserProfileCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    if current_user.role != "applicant":
        raise HTTPException(status_code=403, detail="Only employers can post jobs")
    return create_profile(db, userprofile, current_user.id)

@router.get("/details/{id}", response_model=ShowUserProfile, status_code=status.HTTP_200_OK)
def show_profile_details(id: int, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_profile_details(id, db, current_user)

@router.put("/update/{id}", response_model=ShowUserProfile, status_code=status.HTTP_202_ACCEPTED)
def update_user_profile(id: int, db: Session=Depends(get_db), profile=UpdateProfile, current_user: User=Depends(get_current_user)):
    return update_profile(id, db, profile, current_user)

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy_job(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return delete_profile(id, db, current_user)