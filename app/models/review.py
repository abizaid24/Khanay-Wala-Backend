import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_between_1_and_5"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), unique=True, nullable=False)

    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User")
    restaurant = relationship("Restaurant")
    order = relationship("Order")
