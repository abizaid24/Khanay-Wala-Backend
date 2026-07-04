from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.cart import clear_cart
from app.models.cart import Cart
from app.models.order import Order, OrderItem, OrderStatus, ORDER_STATUS_TRANSITIONS
from app.schemas.order import CheckoutRequest


def checkout(db: Session, customer_id: str, cart: Cart, checkout_in: CheckoutRequest) -> Order:
    if not cart.items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    restaurant_id = cart.items[0].food_item.restaurant_id
    total_amount = sum(item.food_item.price * item.quantity for item in cart.items)

    order = Order(
        customer_id=customer_id,
        restaurant_id=restaurant_id,
        total_amount=total_amount,
        delivery_address=checkout_in.delivery_address,
        notes=checkout_in.notes,
        status=OrderStatus.pending,
    )
    db.add(order)
    db.flush()  # get order.id before adding items

    for item in cart.items:
        db.add(
            OrderItem(
                order_id=order.id,
                food_item_id=item.food_item_id,
                food_name=item.food_item.name,
                price_at_order=item.food_item.price,
                quantity=item.quantity,
            )
        )

    db.commit()
    db.refresh(order)

    clear_cart(db, cart)

    return order


def get_order_by_id(db: Session, order_id: str) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def get_customer_orders(db: Session, customer_id: str):
    return db.query(Order).filter(Order.customer_id == customer_id).order_by(Order.created_at.desc()).all()


def get_restaurant_orders(db: Session, restaurant_id: str):
    return db.query(Order).filter(Order.restaurant_id == restaurant_id).order_by(Order.created_at.desc()).all()


def update_order_status(db: Session, order: Order, new_status: OrderStatus) -> Order:
    allowed_next = ORDER_STATUS_TRANSITIONS.get(order.status, set())
    if new_status not in allowed_next:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot move order from '{order.status.value}' to '{new_status.value}'",
        )
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order
