from fastapi import APIRouter

from backend.services.analysis.impact_analysis_service import ImpactAnalysisService
from config import INDEX_DIR

router = APIRouter(prefix="/analysis", tags=["Analysis"])

service = ImpactAnalysisService(INDEX_DIR / "idm")


@router.get("/impact/{symbol_name}")
def impact(symbol_name: str, depth: int = 5):
    return service.analyze(symbol_name, depth)