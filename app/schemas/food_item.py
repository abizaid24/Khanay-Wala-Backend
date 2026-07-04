import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FoodItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    category_id: Optional[uuid.UUID] = None


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    category_id: Optional[uuid.UUID] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None


class FoodItemOut(FoodItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    restaurant_id: uuid.UUID
    image_url: Optional[str] = None
    is_available: bool
    created_at: datetime
