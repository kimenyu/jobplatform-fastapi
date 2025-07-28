from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from app.repository import review as review_repo
from app.core.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(data: ReviewCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return review_repo.create_review(db, current_user.id, data)

@router.get("/user/{user_id}", response_model=List[ReviewResponse])
def get_reviews_for_user(user_id: int, db: Session = Depends(get_db)):
    return review_repo.get_reviews_for_user(db, user_id)

@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    return review_repo.get_review_detail(db, review_id)

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, data: ReviewUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return review_repo.update_review(db, review_id, data, current_user.id)

@router.delete("/{review_id}", status_code=status.HTTP_200_OK)
def delete_review(review_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return review_repo.delete_review(db, review_id, current_user.id)
