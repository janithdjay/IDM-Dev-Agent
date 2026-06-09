import re

from backend.services.agent.query_models import Intent


class IntentClassifier:

    def classify(self, question: str):

        q = question.lower().strip()

        # -----------------------------------
        # Find Callers
        # -----------------------------------

        caller_patterns = [

            r"where.*called",
            r"who.*calls",
            r"called by",
            r"find callers?",
            r"show callers?",
            r"list callers?"

        ]

        for pattern in caller_patterns:

            if re.search(pattern, q):

                return Intent.FIND_CALLERS

        # -----------------------------------
        # Dependency Analysis
        # -----------------------------------

        dependency_patterns = [

            r"depends on",
            r"\buses\b",
            r"\breferences\b",
            r"what.*uses",
            r"what.*references",
            r"dependencies?",
            r"external dependencies?"

        ]

        for pattern in dependency_patterns:

            if re.search(pattern, q):

                return Intent.DEPENDENCY_ANALYSIS

        # -----------------------------------
        # Impact Analysis
        # -----------------------------------

        impact_patterns = [

            r"can.*delete",
            r"safe.*remove",
            r"safe.*delete",
            r"should.*remove",
            r"should.*delete",
            r"can.*refactor",
            r"safe.*modify",
            r"what.*depends",
            r"impact",
            r"what.*break",
            r"what happens if",
            r"remove.*will",
            r"delete.*will"

        ]

        for pattern in impact_patterns:

            if re.search(pattern, q):

                return Intent.IMPACT_ANALYSIS

        # -----------------------------------
        # Explain Symbol
        # -----------------------------------

        explain_patterns = [

            r"what.*does",
            r"explain",
            r"describe",
            r"summarize",
            r"tell me about",
            r"walk me through",
            r"overview",
            r"give me an overview",
            r"how.*works",
            r"how.*implemented",
            r"how.*written",
            r"how.*designed",
            r"purpose of",
            r"what is",
            r"why.*exist",
            r"why.*used"

        ]

        for pattern in explain_patterns:

            if re.search(pattern, q):

                return Intent.EXPLAIN_SYMBOL

        # -----------------------------------
        # Unknown
        # -----------------------------------

        return Intent.UNKNOWN