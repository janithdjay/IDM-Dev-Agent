from pathlib import Path

from backend.services.graph.call_graph_service import CallGraphService
from backend.services.reasoning.context_builder import ContextBuilder
from config import INDEX_DIR


class ExecutionEngine:

    def __init__(self):

        index_path = INDEX_DIR / "idm"

        self.graph = CallGraphService(index_path)
        self.context = ContextBuilder(index_path)

    def execute(self, intent, symbol):

        if intent == "find_callers":

            return {
                "intent": intent,
                "symbol": symbol,
                "result": self.graph.get_dependents(symbol)
            }

        if intent == "find_callees":

            return {
                "intent": intent,
                "symbol": symbol,
                "result": self.graph.get_dependencies(symbol)
            }

        if intent == "explain_symbol":

            return {
                "intent": intent,
                "symbol": symbol,
                "result": self.context.build(symbol)
            }

        return {
            "error": "Unsupported intent"
        }