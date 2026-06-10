from backend.services.agent.intent_classifier import IntentClassifier
from backend.services.agent.entity_extractor import EntityExtractor
from backend.services.agent.execution_engine import ExecutionEngine
from backend.services.agent.conversation_memory import ConversationMemory
from backend.services.agent.reference_resolver import ReferenceResolver
from backend.services.llm.ollama_client import OllamaClient


class ChatEngine:

    def __init__(self):

        self.intent_classifier = IntentClassifier()

        self.entity_extractor = EntityExtractor()

        self.execution_engine = ExecutionEngine()

        self.memory = ConversationMemory()

        self.reference_resolver = ReferenceResolver()

        self.llm = OllamaClient(
            model="qwen2.5-coder:3b"
        )

    def chat(
        self,
        question: str
    ):

        # ---------------------------------
        # Store user message
        # ---------------------------------

        self.memory.remember(
            role="user",
            content=question
        )

        intent = self.intent_classifier.classify(
            question
        )

        extracted_symbol = self.entity_extractor.extract_symbol(
            question
        )

        if extracted_symbol:

            symbol = extracted_symbol

        else:

            if self.reference_resolver.should_use_memory(
                question
            ):

                symbol = self.memory.get_last_symbol()

            else:

                symbol = None

        print("=" * 60)
        print("Question:", question)
        print("Resolved Symbol:", symbol)
        print("=" * 60)

        # ---------------------------------
        # General chat
        # ---------------------------------

        if symbol is None:

            prompt = f"""
You are an expert software engineering assistant.

Question:

{question}
"""

            answer = self.llm.generate(prompt)

            self.memory.remember(
                role="assistant",
                content=answer
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

            question=question,

            history=self.memory.get_recent_history()

        )

        self.memory.remember(

            role="assistant",

            content=result.get("answer"),

            symbol=result.get("symbol"),

            intent=result.get("intent")

        )

        return {

            "question": question,

            "intent": result.get("intent"),

            "symbol": result.get("symbol"),

            "answer": result.get("answer"),

            "context_used": result.get("context_used"),

            "metrics": result.get("metrics")

        }