from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.models.review import Review
from app.schemas.review import ReviewCreate


def create_review(db: Session, customer_id: str, review_in: ReviewCreate) -> Review:
    order = db.query(Order).filter(Order.id == review_in.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if str(order.customer_id) != str(customer_id):
        raise HTTPException(status_code=403, detail="You can only review your own orders")
    if order.status != OrderStatus.delivered:
        raise HTTPException(status_code=400, detail="You can only review delivered orders")

    existing = db.query(Review).filter(Review.order_id == order.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="You've already reviewed this order")

    review = Review(
        customer_id=customer_id,
        restaurant_id=order.restaurant_id,
        order_id=order.id,
        rating=review_in.rating,
        comment=review_in.comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_restaurant_reviews(db: Session, restaurant_id: str):
    return (
        db.query(Review)
        .filter(Review.restaurant_id == restaurant_id)
        .order_by(Review.created_at.desc())
        .all()
    )


def get_review_by_id(db: Session, review_id: str) -> Review | None:
    return db.query(Review).filter(Review.id == review_id).first()


def delete_review(db: Session, review: Review) -> None:
    db.delete(review)
    db.commit()
