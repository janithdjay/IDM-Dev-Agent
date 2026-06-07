from collections import deque


class ReasoningEngine:
    """
    Expands symbol context using call graph relationships.
    Enables multi-hop reasoning for debugging questions.
    """

    def __init__(self, graph_service):
        self.graph = graph_service

    def build_reasoning_context(self, symbol: str, max_depth: int = 2):
        """
        Expands:
        - callers
        - callees
        - indirect chains
        """

        visited = set()
        queue = deque([(symbol, 0)])

        callers_map = self.graph.build_graph().get("called_by", {})
        calls_map = self.graph.build_graph().get("calls", {})

        result = {
            "root": symbol,
            "callers_chain": [],
            "callees_chain": []
        }

        while queue:
            node, depth = queue.popleft()

            if node in visited or depth > max_depth:
                continue

            visited.add(node)

            # callers
            for caller in callers_map.get(node, []):
                result["callers_chain"].append({
                    "from": caller,
                    "to": node,
                    "depth": depth + 1
                })
                queue.append((caller, depth + 1))

            # callees
            for callee in calls_map.get(node, []):
                result["callees_chain"].append({
                    "from": node,
                    "to": callee,
                    "depth": depth + 1
                })
                queue.append((callee, depth + 1))

        return result