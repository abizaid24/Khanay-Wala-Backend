from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem, OrderStatus


def restaurant_sales_summary(db: Session, restaurant_id: str) -> dict:
    total_orders = db.query(func.count(Order.id)).filter(Order.restaurant_id == restaurant_id).scalar()

    total_revenue = (
        db.query(func.coalesce(func.sum(Order.total_amount), 0))
        .filter(Order.restaurant_id == restaurant_id, Order.status == OrderStatus.delivered)
        .scalar()
    )

    status_counts = (
        db.query(Order.status, func.count(Order.id))
        .filter(Order.restaurant_id == restaurant_id)
        .group_by(Order.status)
        .all()
    )
    orders_by_status = {status.value: count for status, count in status_counts}

    top_items = (
        db.query(OrderItem.food_name, func.sum(OrderItem.quantity).label("total_qty"))
        .join(Order, Order.id == OrderItem.order_id)
        .filter(Order.restaurant_id == restaurant_id)
        .group_by(OrderItem.food_name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )
    top_selling_items = [{"food_name": name, "total_quantity": int(qty)} for name, qty in top_items]

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "orders_by_status": orders_by_status,
        "top_selling_items": top_selling_items,
    }
