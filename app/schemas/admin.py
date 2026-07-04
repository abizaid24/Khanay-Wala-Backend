import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.user import UserRole


class AdminUserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: str
    role: UserRole
    is_active: bool
    created_at: datetime


class PlatformAnalyticsOut(BaseModel):
    total_users: int
    total_restaurants: int
    total_orders: int
    total_revenue: Decimal
    orders_by_status: dict[str, int]
