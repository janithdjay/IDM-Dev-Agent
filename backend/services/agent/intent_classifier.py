import re

from backend.services.agent.query_models import Intent


class IntentClassifier:

    def classify(self, question: str):

        q = question.lower().strip()

        # -------------------
        # Find Callers
        # -------------------

        if re.search(r"where.*called", q):
            return Intent.FIND_CALLERS

        if re.search(r"who.*calls", q):
            return Intent.FIND_CALLERS

        if re.search(r"called by", q):
            return Intent.FIND_CALLERS

        # -------------------
        # Explain Symbol
        # -------------------

        if re.search(r"what.*does", q):
            return Intent.EXPLAIN_SYMBOL

        if re.search(r"explain", q):
            return Intent.EXPLAIN_SYMBOL

        if re.search(r"how.*works", q):
            return Intent.EXPLAIN_SYMBOL

        if re.search(r"how.*implemented", q):
            return Intent.EXPLAIN_SYMBOL

        # -------------------
        # Impact Analysis
        # -------------------

        if re.search(r"can.*delete", q):
            return Intent.IMPACT_ANALYSIS

        if re.search(r"safe.*remove", q):
            return Intent.IMPACT_ANALYSIS

        if re.search(r"what.*depends", q):
            return Intent.IMPACT_ANALYSIS

        if re.search(r"impact", q):
            return Intent.IMPACT_ANALYSIS

        # -------------------
        # Dependency Analysis
        # -------------------

        if re.search(r"uses", q):
            return Intent.DEPENDENCY_ANALYSIS

        if re.search(r"depends on", q):
            return Intent.DEPENDENCY_ANALYSIS

        if re.search(r"references", q):
            return Intent.DEPENDENCY_ANALYSIS

        # -------------------

        return Intent.UNKNOWN