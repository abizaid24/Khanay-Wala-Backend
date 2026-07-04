from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.crud.review import create_review, get_restaurant_reviews, get_review_by_id, delete_review
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.review import ReviewCreate, ReviewOut

router = APIRouter(tags=["Reviews"])


@router.post("/api/reviews", response_model=ReviewOut, status_code=201)
def add_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    return create_review(db, str(current_user.id), review_in)


@router.get("/api/restaurants/{restaurant_id}/reviews", response_model=list[ReviewOut])
def list_restaurant_reviews(restaurant_id: str, db: Session = Depends(get_db)):
    """Public — anyone can read a restaurant's reviews."""
    return get_restaurant_reviews(db, restaurant_id)


@router.delete("/api/reviews/{review_id}", status_code=204)
def remove_review(
    review_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    review = get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if current_user.role != UserRole.admin and review.customer_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own review")
    delete_review(db, review)
