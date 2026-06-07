import re


class EntityExtractor:

    def extract_symbol(self, question: str):

        patterns = [
            r"called\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"explain\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"remove\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"delete\s+([A-Za-z_][A-Za-z0-9_]*)",
            r"does\s+([A-Za-z_][A-Za-z0-9_]*)"
        ]

        for pattern in patterns:

            match = re.search(pattern, question.lower())

            if match:
                return match.group(1)

        return None