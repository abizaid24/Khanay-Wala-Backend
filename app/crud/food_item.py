from sqlalchemy.orm import Session

from app.models.food_item import FoodItem
from app.schemas.food_item import FoodItemCreate, FoodItemUpdate


def create_food_item(db: Session, restaurant_id: str, item_in: FoodItemCreate) -> FoodItem:
    item = FoodItem(restaurant_id=restaurant_id, **item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_food_item_by_id(db: Session, item_id: str) -> FoodItem | None:
    return db.query(FoodItem).filter(FoodItem.id == item_id).first()


def list_food_items_by_restaurant(db: Session, restaurant_id: str):
    return db.query(FoodItem).filter(FoodItem.restaurant_id == restaurant_id).all()


def search_food_items(db: Session, search: str, skip: int = 0, limit: int = 20):
    return (
        db.query(FoodItem)
        .filter(FoodItem.name.ilike(f"%{search}%"), FoodItem.is_available == True)  # noqa: E712
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_food_item(db: Session, item: FoodItem, item_in: FoodItemUpdate) -> FoodItem:
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_food_item(db: Session, item: FoodItem) -> None:
    db.delete(item)
    db.commit()
