import json
import re
from pathlib import Path


class SymbolResolver:

    def __init__(self, index_path: Path):

        self.index_path = Path(index_path)

        self.symbols = self._load_symbols()

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

        # Ignore spaces

        normalized = candidate.replace(" ", "_")

        for symbol in self.symbols:

            if symbol["name"].lower() == normalized:
                return symbol["name"]

        # Ignore underscores

        normalized = normalized.replace("_", "")

        for symbol in self.symbols:

            if symbol["name"].lower().replace("_", "") == normalized:
                return symbol["name"]

        return None

    def resolve_from_text(self, text: str):

        """
        Fallback scan.

        Looks through every word in the sentence
        and attempts to resolve it as a project symbol.
        """

        tokens = re.findall(
            r"[A-Za-z_][A-Za-z0-9_]*",
            text
        )

        for token in tokens:

            resolved = self.resolve(token)

            if resolved:

                return resolved

        return None