from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

def create_review(db: Session, reviewer_id: int, data: ReviewCreate):
    new_review = Review(
        reviewer_id=reviewer_id,
        reviewee_id=data.reviewee_id,
        rating=data.rating,
        comment=data.comment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def get_reviews_for_user(db: Session, user_id: int):
    return db.query(Review).filter(Review.reviewee_id == user_id).all()

def get_review_detail(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

def update_review(db: Session, review_id: int, data: ReviewUpdate, user_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.reviewer_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this review")

    review.rating = data.rating
    review.comment = data.comment
    db.commit()
    db.refresh(review)
    return review

def delete_review(db: Session, review_id: int, user_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.reviewer_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this review")

    db.delete(review)
    db.commit()
    return {"detail": "Review deleted successfully"}
