from pathlib import Path
import json
from datetime import datetime

from .models import FileEntry, SymbolEntry, ImportEntry


class IndexSerializer:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def _ensure_dir(self, project_id: str):
        project_dir = self.base_path / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir

    def _to_dict_file(self, file: FileEntry):
        return {
            "file_id": file.file_id,
            "path": file.path,
            "language": file.language,
            "lines": file.lines,
            "symbols": file.symbols,
            "imports": file.imports
        }

    def _to_dict_symbol(self, symbol: SymbolEntry):
        return {
            "symbol_id": symbol.symbol_id,
            "name": symbol.name,
            "type": symbol.type,
            "file": symbol.file,
            "start_line": symbol.start_line,
            "end_line": symbol.end_line,
            "parent": symbol.parent,
            "calls": symbol.calls,
            "referenced_vars": symbol.referenced_vars
        }

    def _to_dict_import(self, imp: ImportEntry):
        return {
            "file": imp.file,
            "module": imp.module,
            "alias": imp.alias,
            "type": imp.type
        }

    def save(self, project_id: str, index_data: dict):
        project_dir = self._ensure_dir(project_id)

        files = index_data["files"]
        symbols = index_data["symbols"]
        imports = index_data["imports"]

        # Convert objects → dicts
        files_json = [self._to_dict_file(f) for f in files]
        symbols_json = [self._to_dict_symbol(s) for s in symbols]
        imports_json = [self._to_dict_import(i) for i in imports]

        # Write files
        (project_dir / "files.json").write_text(
            json.dumps(files_json, indent=2),
            encoding="utf-8"
        )

        (project_dir / "symbols.json").write_text(
            json.dumps(symbols_json, indent=2),
            encoding="utf-8"
        )

        (project_dir / "imports.json").write_text(
            json.dumps(imports_json, indent=2),
            encoding="utf-8"
        )

        # Manifest
        manifest = {
            "project_id": project_id,
            "indexed_at": datetime.utcnow().isoformat(),
            "files_count": len(files_json),
            "symbols_count": len(symbols_json),
            "imports_count": len(imports_json),
            "files_index": "files.json",
            "symbols_index": "symbols.json",
            "imports_index": "imports.json"
        }

        (project_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2),
            encoding="utf-8"
        )

        return manifest