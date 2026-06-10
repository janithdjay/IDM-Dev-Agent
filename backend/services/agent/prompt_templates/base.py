class BasePromptTemplate:
    def system(self) -> str:
        raise NotImplementedError

    def task(self) -> str:
        return ""

    def output_format(self) -> str:
        return ""