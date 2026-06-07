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

        return json.loads(
            file.read_text(
                encoding="utf-8"
            )
        )

    # -----------------------------------
    # PUBLIC ENTRY
    # -----------------------------------

    def build(
        self,
        symbol_name: str,
        intent: str = None
    ):

        symbol = self.name_index.get(symbol_name)

        if not symbol:
            return None

        if intent == "find_callers":
            return self._build_find_callers(
                symbol_name
            )

        if intent == "impact_analysis":
            return self._build_impact(
                symbol
            )

        if intent == "dependency_analysis":
            return self._build_dependency(
                symbol
            )

        if intent == "explain_symbol":
            return self._build_explain(
                symbol
            )

        return self._build_default(
            symbol
        )

    # -----------------------------------
    # EXPLAIN
    # -----------------------------------

    def _build_explain(
        self,
        symbol
    ):

        return {

            "symbol": symbol["name"],

            "type": symbol.get("type"),

            "parent": symbol.get("parent"),

            "file": symbol.get("file"),

            "calls": symbol.get(
                "calls",
                []
            ),

            "related_symbols":
                self._find_related(symbol)

        }

    # -----------------------------------
    # FIND CALLERS
    # -----------------------------------

    def _build_find_callers(
        self,
        symbol_name
    ):

        return {

            "symbol": symbol_name,

            "called_by":
                self._find_callers(
                    symbol_name
                )

        }

    # -----------------------------------
    # IMPACT
    # -----------------------------------

    def _build_impact(
        self,
        symbol
    ):

        return {

            "symbol": symbol["name"],

            "type": symbol.get(
                "type"
            ),

            "parent": symbol.get(
                "parent"
            ),

            "file": symbol.get(
                "file"
            ),

            "calls": symbol.get(
                "calls",
                []
            ),

            "called_by":
                self._find_callers(
                    symbol["name"]
                ),

            "related_symbols":
                self._find_related(
                    symbol
                )

        }

    # -----------------------------------
    # DEPENDENCY
    # -----------------------------------

    def _build_dependency(
        self,
        symbol
    ):

        return {

            "symbol": symbol["name"],

            "file": symbol.get(
                "file"
            ),

            "parent": symbol.get(
                "parent"
            ),

            "calls": symbol.get(
                "calls",
                []
            )

        }

    # -----------------------------------
    # DEFAULT
    # -----------------------------------

    def _build_default(
        self,
        symbol
    ):

        return {

            "symbol": symbol["name"],

            "type": symbol.get(
                "type"
            ),

            "parent": symbol.get(
                "parent"
            ),

            "file": symbol.get(
                "file"
            ),

            "calls": symbol.get(
                "calls",
                []
            ),

            "called_by":
                self._find_callers(
                    symbol["name"]
                ),

            "related_symbols":
                self._find_related(
                    symbol
                )

        }

    # -----------------------------------
    # REVERSE LOOKUP
    # -----------------------------------

    def _find_callers(
        self,
        symbol_name
    ):

        callers = []

        for s in self.symbols:

            if symbol_name in s.get(
                "calls",
                []
            ):

                callers.append({

                    "name": s["name"],

                    "type": s.get(
                        "type"
                    ),

                    "parent": s.get(
                        "parent"
                    )

                })

        return callers

    # -----------------------------------
    # RELATED
    # -----------------------------------

    def _find_related(
        self,
        symbol
    ):

        related = []

        parent = symbol.get(
            "parent"
        )

        if parent:

            for s in self.symbols:

                if (
                    s.get("parent") == parent
                    and s["name"] != symbol["name"]
                ):

                    related.append(
                        f"{parent}.{s['name']}"
                    )

        return related