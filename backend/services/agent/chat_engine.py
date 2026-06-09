from backend.services.agent.intent_classifier import IntentClassifier
from backend.services.agent.entity_extractor import EntityExtractor
from backend.services.agent.execution_engine import ExecutionEngine


class ChatEngine:

    def __init__(self):

        self.intent_classifier = IntentClassifier()

        self.entity_extractor = EntityExtractor()

        self.execution_engine = ExecutionEngine()

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

        if symbol is None:

            return {

                "question": question,

                "intent": str(intent),

                "symbol": None,

                "answer": "Unable to identify a code symbol from the question."

            }

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