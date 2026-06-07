import re

from backend.services.agent.query_models import Intent


class IntentClassifier:

    def classify(self, question: str):

        q = question.lower()

        if re.search(r"where.*called", q):
            return Intent.FIND_CALLERS

        if re.search(r"who.*calls", q):
            return Intent.FIND_CALLERS

        if re.search(r"what.*does", q):
            return Intent.EXPLAIN_SYMBOL

        if re.search(r"explain", q):
            return Intent.EXPLAIN_SYMBOL

        if re.search(r"can.*delete", q):
            return Intent.IMPACT_ANALYSIS

        if re.search(r"safe.*remove", q):
            return Intent.IMPACT_ANALYSIS

        return Intent.UNKNOWN