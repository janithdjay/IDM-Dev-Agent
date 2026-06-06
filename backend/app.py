from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.routers.home import router as home_router

app = FastAPI(
    title="IDM Dev Agent",
    version="0.1.0"
)

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="frontend/templates"
)

app.include_router(home_router)