from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.crud.dashboard import restaurant_sales_summary
from app.crud.restaurant import get_restaurant_by_id
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.dashboard import RestaurantDashboardOut

router = APIRouter(prefix="/api/restaurants", tags=["Owner Dashboard"])


@router.get("/{restaurant_id}/dashboard", response_model=RestaurantDashboardOut)
def get_dashboard(
    restaurant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = get_restaurant_by_id(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if current_user.role != UserRole.admin and restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't own this restaurant")
    return restaurant_sales_summary(db, restaurant_id)
