from backend.services.context.context_builder import ContextBuilder
from backend.services.llm.ollama_client import OllamaClient
from backend.services.agent.prompt_builder import PromptBuilder
from backend.services.agent.reasoning_engine import ReasoningEngine
from backend.services.graph.call_graph_service import CallGraphService
from backend.services.cache.context_cache import ContextCache
from backend.services.agent.context_compressor import ContextCompressor
from config import INDEX_DIR
import time


class ExecutionEngine:

    def __init__(self):

        self.context_builder = ContextBuilder(INDEX_DIR / "idm")
        self.graph_service = CallGraphService(INDEX_DIR / "idm")
        self.prompt_builder = PromptBuilder()
        # self.llm = OllamaClient(model="qwen2.5-coder:7b")
        self.llm = OllamaClient(model="qwen2.5-coder:3b")
        self.reasoning_engine = ReasoningEngine(self.graph_service)
        self.cache = ContextCache(ttl_seconds=300)
        self.compressor = ContextCompressor()
        

    def execute(self, intent: str, symbol: str, question: str = None):
        start = time.perf_counter()

        # 1. Build cached context
        cache_key = f"{intent}:{symbol}"

        context = self.cache.get(cache_key)
        if not context:
            context = self.context_builder.build(
                symbol_name=symbol,
                intent=intent
            )
            self.cache.set(cache_key, context)
        print("=" * 60)
        print("Intent:", intent)
        print("Context keys:", list(context.keys()))
        print(
            "Context chars:",
            len(str(context))
        )
        print("=" * 60)

        if not context:
            return {"error": "Symbol not found"}
        
        t1 = time.perf_counter()
        print(f"Context: {t1 - start:.3f}s")

        reasoning_key = f"reasoning:{symbol}"

        reasoning_context = self.cache.get(reasoning_key)
        if not reasoning_context:
            reasoning_context = self.reasoning_engine.build_reasoning_context(symbol)
            self.cache.set(reasoning_key, reasoning_context)
            
        t2 = time.perf_counter()
        print(f"Reasoning: {t2 - t1:.3f}s")

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
        compressed_context = self.compressor.compress(
            context=context,
            intent=intent
        )
        
        print("=" * 60)
        prompt = self.prompt_builder.build(
            intent=intent,
            symbol_data=compressed_context,
            question=question
        )
        print("Prompt length:", len(prompt))
        print("=" * 60)
        
        t3 = time.perf_counter()
        print(f"Prompt: {t3 - t2:.3f}s")

        response = self.llm.generate(prompt)

        t4 = time.perf_counter()

        print(f"LLM: {t4 - t3:.3f}s")
        print(f"TOTAL: {t4 - start:.3f}s")
        print("=" * 60)

        return {
            "symbol": symbol,
            "intent": intent,
            "answer": response,
            "context_used": compressed_context,
            "metrics": {
                "context_ms": round((t1 - start) * 1000, 1),
                "reasoning_ms": round((t2 - t1) * 1000, 1),
                "prompt_ms": round((t3 - t2) * 1000, 1),
                "llm_ms": round((t4 - t3) * 1000, 1),
                "total_ms": round((t4 - start) * 1000, 1),
                "context_chars": len(str(context)),
                "prompt_chars": len(prompt),
                "model": "qwen2.5-coder:3b"
            }
        }