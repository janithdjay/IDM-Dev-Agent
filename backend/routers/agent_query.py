from fastapi import APIRouter

from backend.services.agent.intent_classifier import IntentClassifier

router = APIRouter(
    prefix="/agent",
    tags=["Agent Query"]
)

classifier = IntentClassifier()


@router.post("/classify")
def classify(payload: dict):

    question = payload.get("question", "")

    intent = classifier.classify(question)

    return {
        "question": question,
        "intent": intent.value
    }