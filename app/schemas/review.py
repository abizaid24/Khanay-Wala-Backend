import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewCreate(BaseModel):
    order_id: uuid.UUID
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    customer_id: uuid.UUID
    restaurant_id: uuid.UUID
    order_id: uuid.UUID
    rating: int
    comment: Optional[str] = None
    created_at: datetime
