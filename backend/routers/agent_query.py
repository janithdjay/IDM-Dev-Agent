from fastapi import APIRouter

from backend.services.agent.intent_classifier import IntentClassifier
from backend.services.agent.entity_extractor import EntityExtractor

router = APIRouter(
    prefix="/agent",
    tags=["Agent Query"]
)

classifier = IntentClassifier()
extractor = EntityExtractor()


@router.post("/classify")
def classify(payload: dict):

    question = payload.get("question", "")

    intent = classifier.classify(question)
    symbol = extractor.extract_symbol(question)

    return {
        "question": question,
        "intent": intent.value,
        "symbol": symbol
    }