import json
from pathlib import Path
from collections import defaultdict, deque


class ImpactAnalysisService:
    def __init__(self, index_path: str):
        self.index_path = Path(index_path)
        self.symbols = self._load_symbols()
        self.graph = self._build_reverse_graph()

    def _load_symbols(self):
        file = self.index_path / "symbols.json"

        if not file.exists():
            return []

        return json.loads(file.read_text(encoding="utf-8"))

    def _build_reverse_graph(self):
        reverse_graph = defaultdict(list)

        for sym in self.symbols:
            caller = sym["name"]
            calls = sym.get("calls", [])

            for callee in calls:
                reverse_graph[callee].append(caller)

        return reverse_graph

    def analyze(self, symbol_name: str, max_depth: int = 5):
        """
        Returns all impacted functions (who depends on this symbol)
        """

        visited = set()
        queue = deque([(symbol_name, 0)])
        impacted = set()

        while queue:
            current, depth = queue.popleft()

            if depth >= max_depth:
                continue

            for caller in self.graph.get(current, []):
                if caller not in visited:
                    visited.add(caller)
                    impacted.add(caller)
                    queue.append((caller, depth + 1))

        return {
            "symbol": symbol_name,
            "max_depth": max_depth,
            "impacted_count": len(impacted),
            "impacted_symbols": list(impacted)
        }