import re

from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def _slugify(name: str) -> str:
    slug = name.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug


def get_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: str) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(db: Session, category_in: CategoryCreate) -> Category:
    category = Category(name=category_in.name, slug=_slugify(category_in.name))
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()
