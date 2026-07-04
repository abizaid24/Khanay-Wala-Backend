import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RestaurantBase(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    phone: Optional[str] = None


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class RestaurantOut(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    owner_id: uuid.UUID
    image_url: Optional[str] = None
    is_approved: bool
    is_active: bool
    created_at: datetime


class RestaurantListOut(BaseModel):
    """Lighter version for browse/search results."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    address: str
    image_url: Optional[str] = None
    is_active: bool
