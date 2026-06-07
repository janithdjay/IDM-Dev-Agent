from fastapi import APIRouter
from backend.services.agent.execution_engine import ExecutionEngine

engine = ExecutionEngine()

router = APIRouter(
    prefix="/agent",
    tags=["Agent Execute"]
)

@router.post("/execute")
def execute(payload: dict):

    return engine.execute(
        intent=payload["intent"],
        symbol=payload.get("symbol"),
        question=payload.get("question")
    )