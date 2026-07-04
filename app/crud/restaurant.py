from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


def create_restaurant(db: Session, owner_id: str, restaurant_in: RestaurantCreate) -> Restaurant:
    restaurant = Restaurant(owner_id=owner_id, **restaurant_in.model_dump())
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def get_restaurant_by_id(db: Session, restaurant_id: str) -> Restaurant | None:
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def get_restaurants_by_owner(db: Session, owner_id: str):
    return db.query(Restaurant).filter(Restaurant.owner_id == owner_id).all()


def list_public_restaurants(db: Session, search: str | None = None, skip: int = 0, limit: int = 20):
    """Only approved + active restaurants are visible to customers."""
    query = db.query(Restaurant).filter(
        Restaurant.is_approved == True,  # noqa: E712
        Restaurant.is_active == True,  # noqa: E712
    )
    if search:
        query = query.filter(Restaurant.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()


def list_pending_restaurants(db: Session):
    """For admin: restaurants awaiting approval."""
    return db.query(Restaurant).filter(Restaurant.is_approved == False).all()  # noqa: E712


def update_restaurant(db: Session, restaurant: Restaurant, restaurant_in: RestaurantUpdate) -> Restaurant:
    update_data = restaurant_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(restaurant, field, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def approve_restaurant(db: Session, restaurant: Restaurant) -> Restaurant:
    restaurant.is_approved = True
    db.commit()
    db.refresh(restaurant)
    return restaurant
