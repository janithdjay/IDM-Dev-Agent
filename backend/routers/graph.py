from fastapi import APIRouter

from backend.services.graph.call_graph_service import CallGraphService
from config import INDEX_DIR

router = APIRouter(prefix="/graph", tags=["Graph"])

service = CallGraphService(INDEX_DIR / "idm")


@router.get("/data")
def graph_data():
    return service.build_graph()


@router.get("/deps/{function_name}")
def dependencies(function_name: str):
    return service.get_dependencies(function_name)


@router.get("/dependents/{function_name}")
def dependents(function_name: str):
    return service.get_dependents(function_name)