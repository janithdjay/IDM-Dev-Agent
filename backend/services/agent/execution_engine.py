from backend.services.context.context_builder import ContextBuilder
from backend.services.llm.ollama_client import OllamaClient
from backend.services.agent.prompt_builder import PromptBuilder
from backend.services.agent.reasoning_engine import ReasoningEngine
from backend.services.graph.call_graph_service import CallGraphService
from backend.services.cache.context_cache import ContextCache
from config import INDEX_DIR


class ExecutionEngine:

    def __init__(self):

        self.context_builder = ContextBuilder(INDEX_DIR / "idm")
        self.graph_service = CallGraphService(INDEX_DIR / "idm")
        self.prompt_builder = PromptBuilder()
        self.llm = OllamaClient(model="qwen2.5-coder:7b")
        self.reasoning_engine = ReasoningEngine(self.graph_service)
        self.cache = ContextCache(ttl_seconds=300)
        

    def execute(self, intent: str, symbol: str, question: str = None):

        # 1. Build cached context
        cache_key = f"symbol:{symbol}"

        context = self.cache.get(cache_key)
        if not context:
            context = self.context_builder.build(symbol)
            self.cache.set(cache_key, context)

        if not context:
            return {"error": "Symbol not found"}

        reasoning_key = f"reasoning:{symbol}"

        reasoning_context = self.cache.get(reasoning_key)
        if not reasoning_context:
            reasoning_context = self.reasoning_engine.build_reasoning_context(symbol)
            self.cache.set(reasoning_key, reasoning_context)

        context = {
            **context,
            "reasoning": reasoning_context
        }

        # 2. FAST PATH (NO LLM)
        if intent == "find_callers":
            return {
                "symbol": symbol,
                "intent": intent,
                "answer": context.get("called_by", []),
                "context_used": context
            }

        # 3. LLM PATH
        prompt = self.prompt_builder.build(
            intent=intent,
            symbol_data=context,
            question=question
        )

        response = self.llm.generate(prompt)

        return {
            "symbol": symbol,
            "intent": intent,
            "answer": response,
            "context_used": context
        }