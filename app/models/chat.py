import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class AIChatHistory(Base):
    __tablename__ = "ai_chat_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    message = Column(Text, nullable=False)     # what the customer sent
    response = Column(Text, nullable=False)    # what the AI replied

    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User")
