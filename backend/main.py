# .\backend\main.py
import uvicorn
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# Import your existing pipeline modules
from backend.services.agent.symbol_resolver import SymbolResolver
from backend.services.context.context_builder import ContextBuilder
from backend.services.agent.prompt_builder import PromptBuilder
from backend.services.llm.ollama_client import OllamaClient

app = FastAPI(title="IDM Dev Companion Agent")

# Enable CORS so your web interface can talk to the backend hassle-free
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your specific frontend port later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global shared services (Point this to your indexed data folder)
INDEX_DIR = Path("./index_data") 
resolver = SymbolResolver(INDEX_DIR)
context_builder = ContextBuilder(INDEX_DIR)
prompt_builder = PromptBuilder()
llm_client = OllamaClient()

@app.get("/api/chat/stream")
async def chat_stream(
    question: str = Query(..., description="The user's debugging or code question"),
    detected_symbol: str = Query(None, description="Optional symbol parsed out by the agent UI")
):
    """
    Endpoint that streams codebase-aware intelligence tokens directly to the UI.
    """
    def token_generator():
        # 1. Map user query/symbol to the precise target in your indexing layer
        target_symbol = resolver.resolve(detected_symbol or question)
        
        # 2. Build out technical context if a relevant symbol is uncovered
        symbol_data = {}
        intent = "unknown"
        
        if target_symbol:
            # Fall back to general explanation/intent map for the prompt context
            intent = "explain_symbol" 
            symbol_data = context_builder.build(target_symbol, intent=intent)
        
        # 3. Compile the rigid, engineering-focused systemic prompt layout
        full_prompt = prompt_builder.build(
            intent=intent,
            symbol_data=symbol_data,
            question=question
        )
        
        # 4. Stream tokens down the pipe to the web UI
        for token in llm_client.generate_stream(full_prompt):
            yield token

    # text/event-stream or text/plain tells the browser to process text iteratively
    return StreamingResponse(token_generator(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)