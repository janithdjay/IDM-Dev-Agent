import json
from pathlib import Path


class SymbolResolver:

    def __init__(self, index_path: Path):

        self.index_path = Path(index_path)

        self.symbols = self._load_symbols()
        
        print("Loading symbols from:")
        print(self.index_path)

        print(self.index_path / "symbols.json")

    def _load_symbols(self):

        file = self.index_path / "symbols.json"

        if not file.exists():
            return []

        return json.loads(
            file.read_text(encoding="utf-8")
        )

    def resolve(self, candidate: str):

        if not candidate:
            return None

        candidate = candidate.lower().strip()

        # Exact match
        for symbol in self.symbols:

            if symbol["name"].lower() == candidate:
                return symbol["name"]

        # Ignore spaces vs underscores
        normalized = candidate.replace(" ", "_")

        for symbol in self.symbols:

            if symbol["name"].lower() == normalized:
                return symbol["name"]

        # Ignore underscores completely
        normalized = normalized.replace("_", "")

        for symbol in self.symbols:

            if symbol["name"].lower().replace("_", "") == normalized:
                return symbol["name"]

        return None