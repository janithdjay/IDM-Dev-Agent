from fastapi import APIRouter

from backend.services.agent.intent_classifier import IntentClassifier
from backend.services.agent.entity_extractor import EntityExtractor
from backend.services.agent.execution_engine import ExecutionEngine

router = APIRouter(
    prefix="/agent",
    tags=["Agent Execute"]
)

classifier = IntentClassifier()
extractor = EntityExtractor()
engine = ExecutionEngine()


@router.post("/execute")
def execute(payload: dict):

    question = payload.get("question", "")

    intent = classifier.classify(question)
    symbol = extractor.extract_symbol(question)

    if symbol is None:
        return {
            "error": "No symbol detected."
        }

    return engine.execute(intent.value, symbol)