from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.routers import (
    home,
    projects,
    index,
    search,
    graph,
    analysis,
    ui,
    agent,
    agent_query,
    agent_execute,
    agent_chat,
    chat_ui
)

app = FastAPI(
    title="IDM Dev Agent",
    version="0.1.0"
)

app.mount(
    "/static",
    StaticFiles(
        directory="frontend/static"
    ),
    name="static"
)

templates = Jinja2Templates(
    directory="frontend/templates"
)

app.include_router(home.router)
app.include_router(projects.router)
app.include_router(index.router)
app.include_router(search.router)
app.include_router(graph.router)
app.include_router(analysis.router)
app.include_router(ui.router)

app.include_router(agent.router)
app.include_router(agent_query.router)
app.include_router(agent_execute.router)
app.include_router(agent_chat.router)

app.include_router(chat_ui.router)