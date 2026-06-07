import json
from pathlib import Path
from collections import defaultdict


class CallGraphService:
    def __init__(self, index_path: str):
        self.index_path = Path(index_path)
        self.symbols = self._load_symbols()

    def _load_symbols(self):
        file = self.index_path / "symbols.json"

        if not file.exists():
            return []

        return json.loads(file.read_text(encoding="utf-8"))

    def build_graph(self):
        graph = defaultdict(list)
        reverse_graph = defaultdict(list)

        for sym in self.symbols:
            caller = sym["name"]
            calls = sym.get("calls", [])

            for callee in calls:
                graph[caller].append(callee)
                reverse_graph[callee].append(caller)
                
        print("SYMBOLS:", len(self.symbols))
        print("SAMPLE CALLS:", self.symbols[0].get("calls"))

        return {
            "calls": dict(graph),
            "called_by": dict(reverse_graph)
        }
    

    def get_dependencies(self, function_name: str):
        graph = self.build_graph()["calls"]
        return graph.get(function_name, [])

    def get_dependents(self, function_name: str):
        reverse = self.build_graph()["called_by"]
        return reverse.get(function_name, [])