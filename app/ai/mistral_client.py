import httpx
from fastapi import HTTPException

from app.core.config import settings

MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

SYSTEM_PROMPT = (
    "You are the AI assistant for KhanayWala, an online food delivery platform. "
    "Help customers find food, suggest dishes or cuisines based on their mood or cravings, "
    "answer questions about ordering, and be friendly and concise. "
    "You do not have live access to the restaurant database in this conversation, "
    "so speak in general terms about cuisines and dishes rather than inventing specific "
    "restaurant names, prices, or availability."
)


async def get_ai_reply(user_message: str, conversation_history: list[dict] | None = None) -> str:
    """Calls Mistral's chat completion endpoint and returns the assistant's reply text.

    conversation_history: optional list of {"role": "user"/"assistant", "content": str}
    for prior turns, oldest first.
    """
    if not settings.MISTRAL_API_KEY:
        raise HTTPException(status_code=500, detail="AI assistant is not configured (missing MISTRAL_API_KEY)")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {settings.MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.MISTRAL_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(MISTRAL_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"AI service error: {exc.response.status_code} {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f"Could not reach AI service: {exc}")

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=502, detail="Unexpected response from AI service")
