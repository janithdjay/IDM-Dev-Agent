class QueryRouter:

    def route(self, intent, symbol):

        if intent.value == "find_callers":
            return {
                "action": "call_graph.get_dependents",
                "symbol": symbol
            }

        if intent.value == "find_callees":
            return {
                "action": "call_graph.get_dependencies",
                "symbol": symbol
            }

        if intent.value == "explain_symbol":
            return {
                "action": "context_builder.build",
                "symbol": symbol
            }

        return None