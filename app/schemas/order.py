import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.order import OrderStatus


class CheckoutRequest(BaseModel):
    delivery_address: str
    notes: str | None = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    food_item_id: uuid.UUID
    food_name: str
    price_at_order: Decimal
    quantity: int


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    customer_id: uuid.UUID
    restaurant_id: uuid.UUID
    status: OrderStatus
    total_amount: Decimal
    delivery_address: str
    notes: str | None = None
    created_at: datetime
    items: list[OrderItemOut]
