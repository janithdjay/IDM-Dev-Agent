from pathlib import Path

from backend.services.reasoning.symbol_lookup_service import SymbolLookupService
from backend.services.reasoning.source_loader import SourceLoader


class ContextBuilder:

    def __init__(self, index_path: Path):

        self.lookup = SymbolLookupService(index_path)
        self.loader = SourceLoader()

    def build(self, symbol_name: str):

        symbol = self.lookup.get_symbol(symbol_name)

        if symbol is None:
            return None

        source = self.loader.get_source(
            symbol["file"],
            symbol["start_line"],
            symbol["end_line"]
        )

        return {
            "symbol": symbol,
            "source": source
        }