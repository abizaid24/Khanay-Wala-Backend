from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_role
from app.crud.restaurant import (
    create_restaurant,
    get_restaurant_by_id,
    get_restaurants_by_owner,
    list_public_restaurants,
    list_pending_restaurants,
    update_restaurant,
    approve_restaurant,
)
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.restaurant import (
    RestaurantCreate,
    RestaurantUpdate,
    RestaurantOut,
    RestaurantListOut,
)

router = APIRouter(prefix="/api/restaurants", tags=["Restaurants"])


def _ensure_owner_or_admin(restaurant, current_user: User):
    if current_user.role != UserRole.admin and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't own this restaurant")


@router.post("", response_model=RestaurantOut, status_code=201)
def create_my_restaurant(
    restaurant_in: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.restaurant_owner)),
):
    return create_restaurant(db, str(current_user.id), restaurant_in)


@router.get("", response_model=list[RestaurantListOut])
def browse_restaurants(
    search: str | None = Query(default=None, description="Search restaurants by name"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Public — customers browse approved & active restaurants."""
    return list_public_restaurants(db, search=search, skip=skip, limit=limit)


@router.get("/mine", response_model=list[RestaurantOut])
def my_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.restaurant_owner)),
):
    return get_restaurants_by_owner(db, str(current_user.id))


@router.get("/pending", response_model=list[RestaurantOut], dependencies=[Depends(require_role(UserRole.admin))])
def pending_restaurants(db: Session = Depends(get_db)):
    """Admin — restaurants awaiting approval."""
    return list_pending_restaurants(db)


@router.get("/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: str, db: Session = Depends(get_db)):
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant


@router.put("/{restaurant_id}", response_model=RestaurantOut)
def edit_restaurant(
    restaurant_id: str,
    restaurant_in: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    _ensure_owner_or_admin(restaurant, current_user)
    return update_restaurant(db, restaurant, restaurant_in)


@router.patch("/{restaurant_id}/approve", response_model=RestaurantOut, dependencies=[Depends(require_role(UserRole.admin))])
def approve(restaurant_id: str, db: Session = Depends(get_db)):
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return approve_restaurant(db, restaurant)
