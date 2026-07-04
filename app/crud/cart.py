from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.cart import Cart, CartItem
from app.models.food_item import FoodItem
from app.schemas.cart import CartItemAdd, CartOut, CartItemOut


def get_or_create_cart(db: Session, customer_id: str) -> Cart:
    cart = db.query(Cart).filter(Cart.customer_id == customer_id).first()
    if not cart:
        cart = Cart(customer_id=customer_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def _cart_restaurant_id(cart: Cart):
    """Returns the restaurant_id items in this cart belong to, or None if empty."""
    if not cart.items:
        return None
    return cart.items[0].food_item.restaurant_id


def add_item_to_cart(db: Session, cart: Cart, item_in: CartItemAdd) -> Cart:
    food_item = db.query(FoodItem).filter(FoodItem.id == item_in.food_item_id).first()
    if not food_item or not food_item.is_available:
        raise HTTPException(status_code=404, detail="Food item not found or unavailable")

    existing_restaurant_id = _cart_restaurant_id(cart)
    if existing_restaurant_id is not None and existing_restaurant_id != food_item.restaurant_id:
        raise HTTPException(
            status_code=400,
            detail="Your cart has items from another restaurant. Clear your cart first (DELETE /api/cart) to order from a new restaurant.",
        )

    existing_item = (
        db.query(CartItem)
        .filter(CartItem.cart_id == cart.id, CartItem.food_item_id == item_in.food_item_id)
        .first()
    )
    if existing_item:
        existing_item.quantity += item_in.quantity
    else:
        db.add(CartItem(cart_id=cart.id, food_item_id=item_in.food_item_id, quantity=item_in.quantity))

    db.commit()
    db.refresh(cart)
    return cart


def update_cart_item(db: Session, cart: Cart, item_id: str, quantity: int) -> Cart:
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    item.quantity = quantity
    db.commit()
    db.refresh(cart)
    return cart


def remove_cart_item(db: Session, cart: Cart, item_id: str) -> Cart:
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    db.delete(item)
    db.commit()
    db.refresh(cart)
    return cart


def clear_cart(db: Session, cart: Cart) -> None:
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()


def serialize_cart(db: Session, cart: Cart) -> CartOut:
    """Builds the response with live food names/prices and computed subtotals."""
    db.refresh(cart)
    items_out = []
    total = 0
    for item in cart.items:
        food = item.food_item
        subtotal = food.price * item.quantity
        total += subtotal
        items_out.append(
            CartItemOut(
                id=item.id,
                food_item_id=item.food_item_id,
                food_name=food.name,
                unit_price=food.price,
                quantity=item.quantity,
                subtotal=subtotal,
            )
        )
    return CartOut(id=cart.id, items=items_out, total=total)
