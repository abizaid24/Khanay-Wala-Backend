import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


class ChatHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    message: str
    response: str
    created_at: datetime
