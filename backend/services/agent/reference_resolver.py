import re


class ReferenceResolver:

    def __init__(self):

        self.reference_patterns = [

            r"\bit\b",
            r"\bthis\b",
            r"\bthat\b",
            r"\bthis method\b",
            r"\bthat method\b",
            r"\bthis function\b",
            r"\bthat function\b",
            r"\bthis class\b",
            r"\bthat class\b",
            r"\bthe method\b",
            r"\bthe function\b",
            r"\bthe class\b"

        ]

    def should_use_memory(
        self,
        question: str
    ):

        q = question.lower()

        for pattern in self.reference_patterns:

            if re.search(pattern, q):
                return True

        return False