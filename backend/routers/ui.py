from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter()

@router.get("/graph", response_class=HTMLResponse)
def graph_ui():
    html_path = Path("frontend/templates/graph.html")
    return html_path.read_text(encoding="utf-8")