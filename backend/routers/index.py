from fastapi import APIRouter

from backend.services.project_service import ProjectService
from backend.services.indexing.index_service import IndexService
from backend.services.indexing.serializer import IndexSerializer
from config import DATA_DIR

router = APIRouter(prefix="/index", tags=["Indexing"])

project_service = ProjectService(f"{DATA_DIR}/projects.json")
serializer = IndexSerializer(f"{DATA_DIR}/index")


@router.post("/build/{project_id}")
def build_index(project_id: str):
    # 1. Load project config
    project = project_service.get_project(project_id)

    # 2. Create index service
    index_service = IndexService(project)

    # 3. Build index
    result = index_service.build_index()

    # 4. Save index
    manifest = serializer.save(project_id, result)

    return {
        "status": "success",
        "project_id": project_id,
        "manifest": manifest
    }

@router.get("/status/{project_id}")
def index_status(project_id: str):
    import os

    path = f"{DATA_DIR}/index/{project_id}/manifest.json"

    if not os.path.exists(path):
        return {
            "project_id": project_id,
            "indexed": False
        }

    return {
        "project_id": project_id,
        "indexed": True
    }