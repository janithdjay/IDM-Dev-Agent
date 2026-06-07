import re


class EntityExtractor:

    def extract_symbol(self, question: str):

        q = question.strip()

        patterns = [

            r"where\s+is\s+([A-Za-z_][A-Za-z0-9_]*)\s+called",
            r"who\s+calls\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"explain\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"what\s+does\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"can\s+i\s+delete\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"safe\s+to\s+remove\s+([A-Za-z_][A-Za-z0-9_]*)"

        ]

        for pattern in patterns:

            match = re.search(pattern, q, re.IGNORECASE)

            if match:
                return match.group(1)

        return None