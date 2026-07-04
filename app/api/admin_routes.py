from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import require_role
from app.crud.admin import (
    list_all_users,
    set_user_active_status,
    list_all_restaurants,
    platform_analytics,
)
from app.crud.user import get_user_by_id
from app.db.database import get_db
from app.models.user import UserRole
from app.schemas.admin import AdminUserOut, PlatformAnalyticsOut
from app.schemas.restaurant import RestaurantOut

# Every route in this router requires an admin — set once at router level.
router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(require_role(UserRole.admin))],
)


@router.get("/users", response_model=list[AdminUserOut])
def get_all_users(db: Session = Depends(get_db)):
    return list_all_users(db)


@router.patch("/users/{user_id}/deactivate", response_model=AdminUserOut)
def deactivate_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return set_user_active_status(db, user, False)


@router.patch("/users/{user_id}/activate", response_model=AdminUserOut)
def activate_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return set_user_active_status(db, user, True)


@router.get("/restaurants", response_model=list[RestaurantOut])
def get_all_restaurants(db: Session = Depends(get_db)):
    """All restaurants — pending, approved, active, inactive — for admin oversight."""
    return list_all_restaurants(db)


@router.get("/analytics", response_model=PlatformAnalyticsOut)
def get_platform_analytics(db: Session = Depends(get_db)):
    return platform_analytics(db)
