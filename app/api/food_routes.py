from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.crud.food_item import (
    create_food_item,
    get_food_item_by_id,
    list_food_items_by_restaurant,
    search_food_items,
    update_food_item,
    delete_food_item,
)
from app.crud.restaurant import get_restaurant_by_id
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.food_item import FoodItemCreate, FoodItemUpdate, FoodItemOut

router = APIRouter(tags=["Menu / Food Items"])


def _ensure_restaurant_owner(restaurant, current_user: User):
    if current_user.role != UserRole.admin and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't own this restaurant")


@router.post("/api/restaurants/{restaurant_id}/foods", response_model=FoodItemOut, status_code=201)
def add_food_item(
    restaurant_id: str,
    item_in: FoodItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    _ensure_restaurant_owner(restaurant, current_user)
    return create_food_item(db, restaurant_id, item_in)


@router.get("/api/restaurants/{restaurant_id}/foods", response_model=list[FoodItemOut])
def get_menu(restaurant_id: str, db: Session = Depends(get_db)):
    """Public — view a restaurant's menu."""
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return list_food_items_by_restaurant(db, restaurant_id)


@router.get("/api/foods/search", response_model=list[FoodItemOut])
def search_foods(
    q: str = Query(..., min_length=1, description="Search food items by name"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Public — search food items across all restaurants."""
    return search_food_items(db, q, skip=skip, limit=limit)


@router.put("/api/foods/{food_id}", response_model=FoodItemOut)
def edit_food_item(
    food_id: str,
    item_in: FoodItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = get_food_item_by_id(db, food_id)
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found")
    restaurant = get_restaurant_by_id(db, str(item.restaurant_id))
    _ensure_restaurant_owner(restaurant, current_user)
    return update_food_item(db, item, item_in)


@router.delete("/api/foods/{food_id}", status_code=204)
def remove_food_item(
    food_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = get_food_item_by_id(db, food_id)
    if not item:
        raise HTTPException(status_code=404, detail="Food item not found")
    restaurant = get_restaurant_by_id(db, str(item.restaurant_id))
    _ensure_restaurant_owner(restaurant, current_user)
    delete_food_item(db, item)
