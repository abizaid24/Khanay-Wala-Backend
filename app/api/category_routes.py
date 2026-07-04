from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.crud.category import get_categories, get_category_by_id, create_category, delete_category
from app.db.database import get_db
from app.models.user import UserRole
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """Public — anyone can browse categories."""
    return get_categories(db)


@router.post("", response_model=CategoryOut, status_code=201, dependencies=[Depends(require_role(UserRole.admin))])
def add_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category_in)


@router.delete("/{category_id}", status_code=204, dependencies=[Depends(require_role(UserRole.admin))])
def remove_category(category_id: str, db: Session = Depends(get_db)):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    delete_category(db, category)
