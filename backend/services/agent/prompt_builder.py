from typing import Dict, Any, List


class PromptBuilder:
    """
    Central prompt construction layer for the agent.
    This ensures deterministic, structured, debug-focused outputs.
    """

    def __init__(self):
        pass

    def build(self, intent: str, symbol_data: Dict[str, Any], question: str) -> str:
        """
        Build a structured prompt for the LLM.
        """

        base_instructions = self._system_instructions()

        intent_prompt = self._intent_prompt(intent)

        context_block = self._build_context(symbol_data)

        return f"""
{base_instructions}

{intent_prompt}

# USER QUESTION
{question}

# CODE CONTEXT
{context_block}

# INSTRUCTIONS
- Be precise and technical
- Focus only on the provided code context
- Do not hallucinate functions or files not present
- If something is unclear, say "unknown from context"
- Keep response structured and concise
# OUTPUT FORMAT
Return your response in this exact structure:

## Summary
Brief explanation of what the symbol does.

## Analysis
Detailed technical breakdown based only on provided context.

## Key Observations
Important behaviors, dependencies, or patterns.

## Call Flow / Usage
Where and how it is used in the system.

## Potential Issues (if any)
Risks, coupling, performance concerns, or unclear logic.
"""

    # -------------------------

    def _system_instructions(self) -> str:
        return """
        You are a senior software engineering assistant embedded inside a codebase analysis system.

        Your job is to help developers debug, understand, and reason about a local codebase.

        You do NOT behave like a chatbot.

        You behave like a static analysis + reasoning engine.
        """

    def _intent_prompt(self, intent: str) -> str:
        if intent == "explain_symbol":
            return """
            TASK:
            Explain the given symbol from the codebase.

            Focus:
            - What it does
            - Where it is used
            - What it interacts with
            """

        if intent == "find_callers":
            return """
            TASK:
            Find where this symbol is called in the system.

            Focus:
            - Direct callers
            - Indirect callers (via wrappers)
            - Class / worker / async chains
            """

        if intent == "unknown":
            return """
            TASK:
            Try to interpret developer intent using code context only.
            """

        if intent == "impact_analysis":
            return """
            TASK:

            Analyze the impact of modifying or deleting this symbol.

            Focus:

            - direct callers
            - indirect callers
            - related methods
            - possible side effects
            - refactoring risks
            """

        if intent == "dependency_analysis":
            return """
            TASK:

            Analyze dependencies involving this symbol.

            Focus:

            - incoming dependencies
            - outgoing dependencies
            - coupling
            - architecture implications
            """

        return "TASK: General code analysis."

    def _build_context(self, symbol_data: Dict[str, Any]) -> str:
        if not symbol_data:
            return "No symbol context found."

        lines = []

        lines.append(f"Symbol: {symbol_data.get('symbol')}")
        lines.append(f"Type: {symbol_data.get('type')}")
        lines.append(f"File: {symbol_data.get('file')}")
        lines.append(f"Parent: {symbol_data.get('parent')}")

        calls = symbol_data.get("calls", [])
        if calls:
            lines.append("\nDirect Calls:")
            lines.append(", ".join(calls[:20]))  # prevent prompt explosion

        related = symbol_data.get("related_symbols", [])
        if related:
            lines.append("\nRelated Symbols:")
            lines.append(", ".join(related[:10]))

        callers = symbol_data.get("called_by", [])
        if callers:
            lines.append("\nCalled By:")
            for c in callers[:10]:
                lines.append(f"- {c}")
                
        reasoning = symbol_data.get("reasoning", {})

        if reasoning:
            lines.append("\nCall Graph Reasoning:")

            callers = reasoning.get("callers_chain", [])
            if callers:
                lines.append("\nCallers Chain:")
                for c in callers[:10]:
                    lines.append(f"{c['from']} → {c['to']} (depth {c['depth']})")

            callees = reasoning.get("callees_chain", [])
            if callees:
                lines.append("\nCallees Chain:")
                for c in callees[:10]:
                    lines.append(f"{c['from']} → {c['to']} (depth {c['depth']})")

        return "\n".join(lines)