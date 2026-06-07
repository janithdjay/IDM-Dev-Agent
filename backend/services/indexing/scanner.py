from pathlib import Path
from typing import List


class ProjectScanner:
    def __init__(self, root_path: str, ignore_dirs=None):
        self.root_path = Path(root_path)
        self.ignore_dirs = ignore_dirs or {".git", "__pycache__", "venv", ".venv"}

    def scan(self) -> List[Path]:
        files = []

        for path in self.root_path.rglob("*"):
            if path.is_dir():
                continue

            if any(part in self.ignore_dirs for part in path.parts):
                continue

            if path.suffix == ".py":
                files.append(path)

        return files