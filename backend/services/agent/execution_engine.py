from backend.services.context.context_builder import ContextBuilder
from backend.services.llm.ollama_client import OllamaClient
from backend.services.agent.prompt_builder import PromptBuilder
from backend.services.agent.reasoning_engine import ReasoningEngine
from backend.services.graph.call_graph_service import CallGraphService
from config import INDEX_DIR


class ExecutionEngine:

    def __init__(self):

        self.context_builder = ContextBuilder(INDEX_DIR / "idm")
        self.graph_service = CallGraphService(INDEX_DIR / "idm")
        self.prompt_builder = PromptBuilder()
        self.llm = OllamaClient(model="qwen2.5-coder:7b")
        self.reasoning_engine = ReasoningEngine(self.graph_service)
        

    def execute(self, intent: str, symbol: str, question: str = None):

        # 1. Build context
        context = self.context_builder.build(symbol)

        reasoning_context = self.reasoning_engine.build_reasoning_context(
            symbol if symbol else "unknown"
        )

        context = {
            **context,
            "reasoning": reasoning_context
        }

        if not context:
            return {
                "error": "Symbol not found"
            }

        # 2. If no LLM needed (future optimization hook)
        if intent == "find_callers":
            prompt = self.prompt_builder.build(
                intent=intent,
                symbol_data=context,
                question=question
            )

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