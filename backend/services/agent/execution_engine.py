from backend.services.context.context_builder import ContextBuilder
from backend.services.llm.ollama_client import OllamaClient
from backend.services.llm.prompt_builder import PromptBuilder
from backend.services.agent.prompt_builder import PromptBuilder
from config import INDEX_DIR


class ExecutionEngine:

    def __init__(self):

        self.context_builder = ContextBuilder(INDEX_DIR / "idm")
        self.prompt_builder = PromptBuilder()
        self.llm = OllamaClient(model="qwen2.5-coder:7b")
        

    def execute(self, intent: str, symbol: str, question: str = None):

        # 1. Build context
        context = self.context_builder.build(symbol)

        if not context:
            return {
                "error": "Symbol not found"
            }

        # 2. If no LLM needed (future optimization hook)
        if intent == "find_callers":
            return context["called_by"]

        # 3. Build prompt        
        prompt = self.prompt_builder.build(
            intent=intent,
            symbol_data=context,
            question=question
        )

        # 4. Call LLM
        response = self.llm.generate(prompt)

        return {
            "symbol": symbol,
            "intent": intent,
            "answer": response,
            "context_used": context
        }