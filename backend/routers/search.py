from fastapi import APIRouter

from backend.services.search.search_service import SymbolSearchService
from config import INDEX_DIR

router = APIRouter(prefix="/search", tags=["Search"])

search_service = SymbolSearchService(INDEX_DIR / "idm")


@router.get("/symbols")
def search_symbols(q: str):
    return search_service.search(q)


@router.get("/symbols/type/{symbol_type}")
def search_by_type(symbol_type: str):
    return search_service.search_by_type(symbol_type)