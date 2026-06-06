from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="IDM Dev Agent",
    version="0.1.0"
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>IDM Dev Agent</h1>
    <h3>Status: Running</h3>
    <p>Version: 0.1.0</p>
    """