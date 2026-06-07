from pathlib import Path
import json


class ProjectService:
    def __init__(self, projects_file: str):
        self.projects_file = Path(projects_file)
        self._projects_cache = None

    def _load_projects(self):
        if self._projects_cache:
            return self._projects_cache

        if not self.projects_file.exists():
            raise FileNotFoundError("projects.json not found")

        data = json.loads(self.projects_file.read_text(encoding="utf-8"))
        self._projects_cache = data["projects"]
        return self._projects_cache

    def get_project(self, project_id: str):
        print("LOADED PROJECTS:", self._load_projects())
        projects = self._load_projects()

        for p in projects:
            if p["project_id"] == project_id:
                return p

        raise ValueError(f"Project not found: {project_id}")

    def list_projects(self):
        return self._load_projects()