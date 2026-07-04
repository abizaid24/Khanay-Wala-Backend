from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.order import Order, OrderStatus
from app.models.restaurant import Restaurant
from app.models.user import User


def list_all_users(db: Session):
    return db.query(User).order_by(User.created_at.desc()).all()


def set_user_active_status(db: Session, user: User, is_active: bool) -> User:
    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user


def list_all_restaurants(db: Session):
    """Admin view — includes pending/inactive restaurants, unlike the public browse endpoint."""
    return db.query(Restaurant).order_by(Restaurant.created_at.desc()).all()


def platform_analytics(db: Session) -> dict:
    total_users = db.query(func.count(User.id)).scalar()
    total_restaurants = db.query(func.count(Restaurant.id)).scalar()
    total_orders = db.query(func.count(Order.id)).scalar()

    total_revenue = (
        db.query(func.coalesce(func.sum(Order.total_amount), 0))
        .filter(Order.status == OrderStatus.delivered)
        .scalar()
    )

    status_counts = db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    orders_by_status = {status.value: count for status, count in status_counts}

    return {
        "total_users": total_users,
        "total_restaurants": total_restaurants,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "orders_by_status": orders_by_status,
    }
