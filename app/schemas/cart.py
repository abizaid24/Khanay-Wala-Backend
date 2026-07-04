import uuid
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CartItemAdd(BaseModel):
    food_item_id: uuid.UUID
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    food_item_id: uuid.UUID
    food_name: Optional[str] = None
    unit_price: Optional[Decimal] = None
    quantity: int
    subtotal: Optional[Decimal] = None


class CartOut(BaseModel):
    id: uuid.UUID
    items: list[CartItemOut]
    total: Decimal
