import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    is_approved = Column(Boolean, default=False)   # admin must approve before it's public
    is_active = Column(Boolean, default=True)       # owner can temporarily deactivate

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User")
    food_items = relationship("FoodItem", back_populates="restaurant", cascade="all, delete-orphan")
