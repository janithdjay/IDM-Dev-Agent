import json
from pathlib import Path


class SymbolLookupService:

    def __init__(self, index_path: Path):
        self.index_path = Path(index_path)
        self.symbols = self._load_symbols()

    def _load_symbols(self):
        file = self.index_path / "symbols.json"

        if not file.exists():
            return []

        return json.loads(file.read_text(encoding="utf-8"))

    def get_symbol(self, symbol_name: str):

        for symbol in self.symbols:

            if symbol["name"] == symbol_name:
                return symbol

        return None