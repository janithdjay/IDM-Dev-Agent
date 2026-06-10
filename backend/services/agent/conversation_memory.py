from collections import deque


class ConversationMemory:

    def __init__(self, max_messages=20):

        self.max_messages = max_messages

        self.messages = deque(maxlen=max_messages)

        self.last_symbol = None

        self.last_intent = None

    def remember(
        self,
        role: str,
        content: str,
        symbol=None,
        intent=None
    ):

        self.messages.append({

            "role": role,

            "content": content

        })

        if symbol:

            self.last_symbol = symbol

        if intent:

            self.last_intent = intent

    def get_last_symbol(self):

        return self.last_symbol

    def get_last_intent(self):

        return self.last_intent

    def get_recent_history(
        self,
        limit=6
    ):

        return list(self.messages)[-limit:]

    def clear(self):

        self.messages.clear()

        self.last_symbol = None

        self.last_intent = None