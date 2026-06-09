from backend.services.agent.intent_classifier import IntentClassifier
from backend.services.agent.entity_extractor import EntityExtractor
from backend.services.agent.execution_engine import ExecutionEngine
from backend.services.llm.ollama_client import OllamaClient


class ChatEngine:

    def __init__(self):

        self.intent_classifier = IntentClassifier()

        self.entity_extractor = EntityExtractor()

        self.execution_engine = ExecutionEngine()

        self.llm = OllamaClient(
            model="qwen2.5-coder:3b"
        )

    def chat(
        self,
        question: str
    ):

        intent = self.intent_classifier.classify(
            question
        )

        symbol = self.entity_extractor.extract_symbol(
            question
        )

        # ---------------------------------
        # General software chat
        # ---------------------------------

        if symbol is None:

            prompt = f"""
You are an expert software engineering assistant.

Answer the following question clearly and concisely.

Question:

{question}
"""

            answer = self.llm.generate(
                prompt
            )

            return {

                "question": question,

                "intent": "general_chat",

                "symbol": None,

                "answer": answer

            }

        # ---------------------------------
        # Project-aware execution
        # ---------------------------------

        result = self.execution_engine.execute(

            intent=intent,

            symbol=symbol,

            question=question

        )

        return {

            "question": question,

            "intent": result.get("intent"),

            "symbol": result.get("symbol"),

            "answer": result.get("answer"),

            "context_used": result.get("context_used"),

            "metrics": result.get("metrics")

        }