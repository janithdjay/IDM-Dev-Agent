from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()


@router.get(
    "/chat",
    response_class=HTMLResponse
)
def chat_ui():

    html_path = Path(
        "frontend/templates/chat.html"
    )

    return html_path.read_text(
        encoding="utf-8"
    )