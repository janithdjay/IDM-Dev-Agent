class CrawlerReviewService:
    """
    Converts indexed codebase into architecture insights.
    """

    def __init__(self, index_service, graph_service):
        self.index_service = index_service
        self.graph_service = graph_service

    def build_review_context(self):
        """
        Main entry point for full crawler analysis.
        """

        index = self.index_service.get_index()

        graph = self.graph_service.build_graph()

        return {
            "modules": self._extract_modules(index),
            "symbols": self._extract_symbols(index),
            "dependencies": self._extract_dependencies(graph),
            "hotspots": self._find_hotspots(graph),
            "architecture_summary": self._build_arch_summary(graph)
        }

    # -------------------------------------------------

    def _extract_modules(self, index):

        modules = set()

        if not index:
            return []

        for value in index.values():

            # CASE 1: value is list of symbol entries
            if isinstance(value, list):

                for item in value:

                    if isinstance(item, dict):
                        modules.add(item.get("module", "unknown"))

                    elif isinstance(item, str):
                        modules.add("unknown")

            # CASE 2: value is dict (old expected format)
            elif isinstance(value, dict):
                modules.add(value.get("module", "unknown"))

        return list(modules)

    # -------------------------------------------------

    def _extract_symbols(self, index):
        return {
            k: {
                "type": v.get("type"),
                "file": v.get("file"),
                "calls": v.get("calls", []),
                "called_by": v.get("called_by", [])
            }
            for k, v in index.items()
        }

    # -------------------------------------------------

    def _extract_dependencies(self, graph):
        return graph.get("calls", {})

    # -------------------------------------------------

    def _find_hotspots(self, graph):
        """
        Identify heavily connected nodes.
        """
        calls = graph.get("calls", {})

        hotspots = []

        for node, edges in calls.items():
            if len(edges) > 5:
                hotspots.append({
                    "symbol": node,
                    "fan_out": len(edges)
                })

        return sorted(
            hotspots,
            key=lambda x: x["fan_out"],
            reverse=True
        )

    # -------------------------------------------------

    def _build_arch_summary(self, graph):
        calls = graph.get("calls", {})

        total_edges = sum(len(v) for v in calls.values())

        return {
            "total_nodes": len(calls),
            "total_edges": total_edges,
            "avg_fan_out": total_edges / max(len(calls), 1)
        }