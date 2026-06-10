from .base import BasePromptTemplate


class RunCrawlTemplate(BasePromptTemplate):

    def system(self):
        return """
You are a system execution analysis assistant.
You analyze crawl execution flows and data movement.
"""

    def task(self):
        return """
TASK:

Explain crawl execution behavior and flow.
"""

    def output_format(self):
        return """
## Summary
## Execution Flow
## Data Movement
## Bottlenecks
"""