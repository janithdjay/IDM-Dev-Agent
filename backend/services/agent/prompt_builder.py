from typing import Dict, Any, List
from backend.services.agent.prompt_templates.registry import PromptRegistry


class PromptBuilder:
    """
    Central prompt construction layer for the agent.
    """

    def __init__(self):
        pass

    def build(
        self,
        intent: str,
        crawler_review_data: Dict[str, Any],
        question: str,
        history: List[Dict[str, str]] = None
    ) -> str:

        template = PromptRegistry.get(intent)

        base_instructions = self._system_instructions()

        # ---------------------------
        # TEMPLATE HANDLING (NEW CORE LOGIC)
        # ---------------------------

        if template:
            system_block = template.system()
            task_block = template.task()
            format_block = template.output_format()
        else:
            system_block = base_instructions
            task_block = self._fallback_task(intent)
            format_block = ""

        history_block = self._build_history(history or [])

        context_block = self._build_context(crawler_review_data)

        return f"""
{system_block}

{task_block}

{format_block}

# RECENT CONVERSATION

{history_block}

# CURRENT USER QUESTION

{question}

# CODE CONTEXT

{context_block}

# IMPORTANT RULES

- The recent conversation is additional context.
- The current user question has highest priority.
- Use the conversation history to resolve references like:
    - it
    - this
    - that method
    - summarize it
    - explain further
    - make it shorter
- Never invent symbols.
- Only use symbols present in the supplied context.
- If uncertain, say "unknown from context".
"""

    # -------------------------------------------------

    def _system_instructions(self):

        return """
You are a senior software engineering assistant.

You help developers understand a local codebase.

You are a reasoning engine.

You do not invent APIs or functions.

You answer only from supplied context.
"""

    # -------------------------------------------------

    def _fallback_task(self, intent: str):

        if str(intent) == "explain_symbol":

            return "TASK: Explain the requested symbol."

        if str(intent) == "find_callers":

            return "TASK: Identify callers and call chains."

        if str(intent) == "impact_analysis":

            return """
TASK: Assess modification or deletion impact.
Include callers, dependencies, and risks.
"""

        if str(intent) == "dependency_analysis":

            return """
TASK: Analyze dependencies (incoming and outgoing).
"""

        if str(intent) == "codebase_review":
            return """
    TASK: Review codebase structure and suggest improvements.
    Focus on architecture, design, and maintainability.
    """

        return "TASK: General code analysis."

    # -------------------------------------------------

    def _build_history(
        self,
        history
    ):

        if not history:
            return "No previous conversation."

        lines = []

        for item in history:

            role = item.get("role", "unknown")
            content = item.get("content", "")

            lines.append(f"{role.upper()}: {content}")

        return "\n\n".join(lines)

    # -------------------------------------------------

    def _build_context(
        self,
        symbol_data
    ):

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
            lines.append(", ".join(calls[:20]))

        related = symbol_data.get("related_symbols", [])
        if related:
            lines.append("\nRelated Symbols:")
            lines.append(", ".join(related[:10]))

        callers = symbol_data.get("called_by", [])
        if callers:
            lines.append("\nCalled By:")
            for caller in callers[:10]:
                lines.append(str(caller))

        reasoning = symbol_data.get("reasoning", {})
        if reasoning:
            lines.append("\nReasoning:")

            for item in reasoning.get("callers_chain", [])[:10]:
                lines.append(f"{item['from']} -> {item['to']}")

            for item in reasoning.get("callees_chain", [])[:10]:
                lines.append(f"{item['from']} -> {item['to']}")

        return "\n".join(lines)