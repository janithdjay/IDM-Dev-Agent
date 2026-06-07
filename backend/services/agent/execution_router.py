from backend.services.graph.call_graph_service import CallGraphService


class ExecutionRouter:

    DETERMINISTIC_INTENTS = {
        "find_callers",
        "find_dependencies",
        "find_related",
    }

    def should_use_llm(self, intent: str) -> bool:
        return intent not in self.DETERMINISTIC_INTENTS