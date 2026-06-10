class ConversationMemory:

    def __init__(self):

        self.last_symbol = None

        self.last_intent = None

        self.last_question = None

        self.last_answer = None

    def remember(

        self,

        symbol,

        intent,

        question=None,

        answer=None

    ):

        self.last_symbol = symbol

        self.last_intent = intent

        self.last_question = question

        self.last_answer = answer

    def get_last_symbol(self):

        return self.last_symbol

    def get_last_intent(self):

        return self.last_intent

    def get_last_question(self):

        return self.last_question

    def get_last_answer(self):

        return self.last_answer

    def clear(self):

        self.last_symbol = None

        self.last_intent = None

        self.last_question = None

        self.last_answer = None