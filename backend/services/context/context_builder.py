import json
from pathlib import Path


class ContextBuilder:

    def __init__(self, index_path: Path):

        self.index_path = Path(index_path)

        self.symbols = self._load_symbols()

        self.name_index = {
            s["name"]: s for s in self.symbols
        }

    def _load_symbols(self):

        file = self.index_path / "symbols.json"

        if not file.exists():
            return []

        return json.loads(file.read_text(encoding="utf-8"))

    # -----------------------------
    # MAIN ENTRY POINT
    # -----------------------------

    def build(self, symbol_name: str):

        symbol = self.name_index.get(symbol_name)

        if not symbol:
            return None

        return {
            "symbol": symbol["name"],
            "type": symbol.get("type"),
            "parent": symbol.get("parent"),
            "file": symbol.get("file"),
            "calls": symbol.get("calls", []),

            "called_by": self._find_callers(symbol_name),
            "related_symbols": self._find_related(symbol)
        }

    # -----------------------------
    # CALLERS (reverse lookup)
    # -----------------------------

    def _find_callers(self, symbol_name: str):

        callers = []

        for s in self.symbols:

            if symbol_name in s.get("calls", []):
                callers.append({
                    "name": s["name"],
                    "type": s.get("type"),
                    "parent": s.get("parent")
                })

        return callers

    # -----------------------------
    # RELATED SYMBOLS
    # -----------------------------

    def _find_related(self, symbol):

        related = []

        parent = symbol.get("parent")

        if parent:

            for s in self.symbols:

                if s.get("parent") == parent and s["name"] != symbol["name"]:
                    related.append(f"{parent}.{s['name']}")

        return related