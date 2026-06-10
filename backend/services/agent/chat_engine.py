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

        intent = self.intent_classifier.classify(
            question
        )

        extracted_symbol = self.entity_extractor.extract_symbol(
            question
        )

        # ---------------------------------
        # Explicit symbol always wins
        # ---------------------------------

        if extracted_symbol:

            symbol = extracted_symbol

        else:

            # ---------------------------------
            # Use memory ONLY for references
            # ---------------------------------

            if self.reference_resolver.should_use_memory(
                question
            ):

                symbol = self.memory.get_last_symbol()

            else:

                symbol = None

        # ---------------------------------
        # Debug logging
        # ---------------------------------

        print("=" * 60)
        print("Question:", question)
        print("Extracted Symbol:", extracted_symbol)
        print("Memory Symbol:", self.memory.get_last_symbol())
        print(
            "Reference Detected:",
            self.reference_resolver.should_use_memory(question)
        )
        print("Resolved Symbol:", symbol)
        print("=" * 60)

        # ---------------------------------
        # General software chat
        # ---------------------------------

        if symbol is None:

            prompt = f"""
You are an expert software engineering assistant.

Answer clearly and concisely.

Question:

{question}
"""

            answer = self.llm.generate(prompt)

            return {

                "question": question,

                "intent": "general_chat",

                "symbol": None,

                "answer": answer

            }

        # ---------------------------------
        # Execute project-aware request
        # ---------------------------------

        result = self.execution_engine.execute(

            intent=intent,

            symbol=symbol,

            question=question

        )

        # ---------------------------------
        # Update conversation memory
        # ---------------------------------

        self.memory.remember(
            symbol=result.get("symbol"),
            intent=result.get("intent"),
            question=question,
            answer=result.get("answer")
        )
        
        print("=" * 60)
        print("Conversation Memory Updated")
        print("Last Symbol:", self.memory.get_last_symbol())
        print("Last Intent:", self.memory.get_last_intent())
        print("Last Question:", self.memory.get_last_question())
        print("=" * 60)

        return {

            "question": question,

            "intent": result.get("intent"),

            "symbol": result.get("symbol"),

            "answer": result.get("answer"),

            "context_used": result.get("context_used"),

            "metrics": result.get("metrics")

        }