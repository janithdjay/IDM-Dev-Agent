class ContextCompressor:

    def compress(self, context: dict, intent: str):

        compressed = dict(context)

        if intent == "explain_symbol":
            compressed["calls"] = context.get("calls", [])[:20]
            compressed["related_symbols"] = context.get("related_symbols", [])[:10]

            reasoning = context.get("reasoning", {})

            compressed["reasoning"] = {
                "callers_chain": reasoning.get("callers_chain", [])[:5],
                "callees_chain": reasoning.get("callees_chain", [])[:5],
            }

        elif intent == "find_callers":

            compressed = {
                "symbol": context.get("symbol"),
                "called_by": context.get("called_by", []),
                "reasoning": context.get("reasoning", {}),
            }

        return compressed