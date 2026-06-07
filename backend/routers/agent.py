from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from pathlib import Path

# Explicit imports pointing to your provided components
from backend.services.reasoning.context_builder import ContextBuilder as ReasoningContextBuilder
from backend.services.llm.prompt_builder import PromptBuilder
from backend.services.llm.ollama_client import OllamaClient

router = APIRouter(prefix="/api/agent", tags=["Agent"])

# Path pointing to where your serialized index files live
INDEX_PATH = Path("./index_data")

# Instantiate layout-aware operational services
context_builder = ReasoningContextBuilder(INDEX_PATH)
prompt_builder = PromptBuilder()
llm_client = OllamaClient()


@router.get("/stream")
async def stream_agent_response(
    question: str = Query(..., description="The user query or code question"),
    symbol_name: str = Query(None, description="Target symbol if explicitly extracted")
):
    """
    Asynchronously streams repository context analysis back to the development chat frame.
    """
    def token_generator():
        context_data = None
        intent = "explain_symbol"

        # Attempt structural reasoning lookups if a specific symbol is provided
        if symbol_name:
            context_data = context_builder.build(symbol_name)

        # Fallback context dictionary if symbol parsing yielded nothing
        if not context_data:
            intent = "general_query"
            context_data = {
                "message": "No direct codebase symbol matches resolved for this request context."
            }

        # Build prompt using your precise layout format
        full_prompt = prompt_builder.build(
            question=question,
            intent=intent,
            context=context_data
        )

        # Stream generated tokens out of Ollama to the client connection
        for token in llm_client.generate_stream(full_prompt):
            yield token

    return StreamingResponse(token_generator(), media_type="text/plain")