from sqlalchemy.orm import Session

from app.models.chat import AIChatHistory


def save_chat_turn(db: Session, customer_id: str, message: str, response: str) -> AIChatHistory:
    entry = AIChatHistory(customer_id=customer_id, message=message, response=response)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_chat_history(db: Session, customer_id: str, limit: int = 20):
    return (
        db.query(AIChatHistory)
        .filter(AIChatHistory.customer_id == customer_id)
        .order_by(AIChatHistory.created_at.desc())
        .limit(limit)
        .all()
    )


def build_conversation_context(db: Session, customer_id: str, turns: int = 5) -> list[dict]:
    """Recent history as alternating user/assistant messages, oldest first,
    to give the AI short-term memory of the conversation."""
    recent = get_chat_history(db, customer_id, limit=turns)
    recent = list(reversed(recent))  # oldest first
    context = []
    for entry in recent:
        context.append({"role": "user", "content": entry.message})
        context.append({"role": "assistant", "content": entry.response})
    return context
