from backend.services.context.context_builder import ContextBuilder
from config import INDEX_DIR


class ExecutionEngine:

    def __init__(self):

        self.context = ContextBuilder(INDEX_DIR / "idm")

    def execute(self, intent: str, symbol: str):

        if intent == "find_callers":

            return self.context._find_callers(symbol)

        if intent == "explain_symbol":

            return self.context.build(symbol)

        return {
            "error": "unsupported intent"
        }