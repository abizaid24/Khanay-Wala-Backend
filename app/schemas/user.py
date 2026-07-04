import enum
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict

from app.models.user import UserRole


class RegisterableRole(str, enum.Enum):
    """Roles a person can pick for themselves at sign-up.

    Deliberately excludes UserRole.admin — admin accounts must be
    granted by an existing admin, never self-selected at registration.
    """
    customer = "customer"
    restaurant_owner = "restaurant_owner"


class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: RegisterableRole = RegisterableRole.customer


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: UserRole
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None
    exp: Optional[int] = None
