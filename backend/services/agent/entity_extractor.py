import re

from config import INDEX_DIR
from backend.services.agent.symbol_resolver import SymbolResolver


class EntityExtractor:

    def __init__(self):

        self.resolver = SymbolResolver(
            INDEX_DIR / "idm"
        )

    def extract_symbol(self, question: str):

        patterns = [

            r"where\s+is\s+([A-Za-z_][A-Za-z0-9_]*)\(?\)?\s+called",
            r"who\s+calls\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"explain\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"what\s+does\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"can\s+i\s+delete\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"safe\s+to\s+remove\s+([A-Za-z_][A-Za-z0-9_]*)"

        ]

        candidate = None

        for pattern in patterns:

            match = re.search(
                pattern,
                question,
                re.IGNORECASE
            )

            if match:
                candidate = match.group(1)
                break

        if candidate is None:
            return None

        print(f"Candidate extracted: {candidate}")
        return self.resolver.resolve(candidate)