from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.crud.cart import get_or_create_cart
from app.crud.order import (
    checkout,
    get_order_by_id,
    get_customer_orders,
    get_restaurant_orders,
    update_order_status,
)
from app.crud.restaurant import get_restaurant_by_id
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.order import CheckoutRequest, OrderOut, OrderStatusUpdate

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/checkout", response_model=OrderOut, status_code=201)
def place_order(
    checkout_in: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    cart = get_or_create_cart(db, str(current_user.id))
    return checkout(db, str(current_user.id), cart, checkout_in)


@router.get("", response_model=list[OrderOut])
def my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    """Customer's own order history."""
    return get_customer_orders(db, str(current_user.id))


@router.get("/restaurant/{restaurant_id}", response_model=list[OrderOut])
def restaurant_incoming_orders(
    restaurant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Restaurant owner (or admin) views incoming orders for their restaurant."""
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if current_user.role != UserRole.admin and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't own this restaurant")
    return get_restaurant_orders(db, restaurant_id)


@router.get("/{order_id}", response_model=OrderOut)
def order_detail(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    is_customer_owner = order.customer_id == current_user.id
    is_restaurant_owner = order.restaurant.owner_id == current_user.id
    if current_user.role != UserRole.admin and not (is_customer_owner or is_restaurant_owner):
        raise HTTPException(status_code=403, detail="You don't have access to this order")

    return order


@router.patch("/{order_id}/status", response_model=OrderOut)
def change_order_status(
    order_id: str,
    status_in: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Only the restaurant owner (or admin) can update order status."""
    order = get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if current_user.role != UserRole.admin and order.restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to update this order")

    return update_order_status(db, order, status_in.status)
