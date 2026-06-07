from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.agent.chat_engine import ChatEngine

router = APIRouter(
    prefix="/agent",
    tags=["Agent Chat"]
)

engine = ChatEngine()


class ChatRequest(BaseModel):

    message: str


@router.post("/chat")
def chat(
    request: ChatRequest
):

    return engine.chat(
        request.message
    )