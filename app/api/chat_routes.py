from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.mistral_client import get_ai_reply
from app.auth.dependencies import require_role
from app.crud.chat import save_chat_turn, get_chat_history, build_conversation_context
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.chat import ChatRequest, ChatResponse, ChatHistoryOut

router = APIRouter(prefix="/api/chat", tags=["AI Chat Assistant"])


@router.post("", response_model=ChatResponse)
async def chat_with_assistant(
    chat_in: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    context = build_conversation_context(db, str(current_user.id))
    reply = await get_ai_reply(chat_in.message, conversation_history=context)
    save_chat_turn(db, str(current_user.id), chat_in.message, reply)
    return ChatResponse(reply=reply)


@router.get("/history", response_model=list[ChatHistoryOut])
def chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.customer)),
):
    return get_chat_history(db, str(current_user.id))
