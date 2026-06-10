from pathlib import Path

from .scanner import ProjectScanner
from .python_parser import PythonParser
from .builder import IndexBuilder


class IndexService:
    def __init__(self, project_config: dict):
        self.project_id = project_config["project_id"]
        self.root_path = project_config["root_path"]
        self.scanner = ProjectScanner(self.root_path)
        self.parser = PythonParser()
        self.builder = IndexBuilder()

        self.serializer = None

        self.files = []
        self.symbols = []
        self.imports = []

    def build_index(self):
        file_paths = self.scanner.scan()

        for file_path in file_paths:
            source = Path(file_path).read_text(encoding="utf-8")

            symbols, imports = self.parser.parse(
                str(file_path),
                source
            )

            self.symbols.extend(symbols)
            self.imports.extend(imports)

            file_entry = self.builder.build_file_entry(
                file_path,
                symbols,
                imports
            )

            self.files.append(file_entry)

        return {
            "files": self.files,
            "symbols": self.symbols,
            "imports": self.imports
        }
        
    def get_index(self):
        """
        Compatibility layer for analysis services.

        Returns the internal index structure.
        """

        # Case 1: if index already stored
        if hasattr(self, "index") and self.index:
            return self.index

        # Case 2: if build method exists
        if hasattr(self, "build_index"):
            return self.build_index()

        # Case 3: fallback empty safe structure
        return {}