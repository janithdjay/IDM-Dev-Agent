import json
from pathlib import Path


class SymbolSearchService:
    def __init__(self, index_path: str):
        self.index_path = Path(index_path)
        self.symbols = self._load_symbols()

    def _load_symbols(self):
        symbols_file = self.index_path / "symbols.json"

        if not symbols_file.exists():
            return []

        return json.loads(symbols_file.read_text(encoding="utf-8"))

    def search(self, query: str):
        query = query.lower().strip()

        results = []

        for sym in self.symbols:
            name = sym.get("name", "").lower()
            sym_type = sym.get("type", "").lower()

            # MATCH RULES
            if query in name:
                results.append(sym)
                continue

            if query == sym_type:
                results.append(sym)
                continue

        return {
            "query": query,
            "count": len(results),
            "results": results
        }

    def search_by_type(self, symbol_type: str):
        symbol_type = symbol_type.lower()

        return [
            s for s in self.symbols
            if s.get("type", "").lower() == symbol_type
        ]