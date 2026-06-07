from fastapi import APIRouter
from backend.services.project_service import ProjectService
from config import DATA_DIR

router = APIRouter(prefix="/projects", tags=["Projects"])

project_service = ProjectService(f"{DATA_DIR}/projects.json")


@router.get("/")
def list_projects():
    return project_service.list_projects()


@router.get("/{project_id}")
def get_project(project_id: str):
    print("DEBUG:", project_id)
    return project_service.get_project(project_id)