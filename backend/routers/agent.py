from fastapi import APIRouter

from backend.services.reasoning.context_builder import ContextBuilder
from config import INDEX_DIR


router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)

builder = ContextBuilder(INDEX_DIR / "idm")


@router.get("/context/{symbol_name}")
def get_context(symbol_name: str):

    return builder.build(symbol_name)