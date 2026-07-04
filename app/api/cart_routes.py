from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.crud.cart import (
    get_or_create_cart,
    add_item_to_cart,
    update_cart_item,
    remove_cart_item,
    clear_cart,
    serialize_cart,
)
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartOut

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.get("", response_model=CartOut)
def view_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    cart = get_or_create_cart(db, str(current_user.id))
    return serialize_cart(db, cart)


@router.post("/items", response_model=CartOut, status_code=201)
def add_to_cart(
    item_in: CartItemAdd,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    cart = get_or_create_cart(db, str(current_user.id))
    cart = add_item_to_cart(db, cart, item_in)
    return serialize_cart(db, cart)


@router.put("/items/{item_id}", response_model=CartOut)
def change_quantity(
    item_id: str,
    item_in: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    cart = get_or_create_cart(db, str(current_user.id))
    cart = update_cart_item(db, cart, item_id, item_in.quantity)
    return serialize_cart(db, cart)


@router.delete("/items/{item_id}", response_model=CartOut)
def remove_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    cart = get_or_create_cart(db, str(current_user.id))
    cart = remove_cart_item(db, cart, item_id)
    return serialize_cart(db, cart)


@router.delete("", status_code=204)
def empty_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    cart = get_or_create_cart(db, str(current_user.id))
    clear_cart(db, cart)
