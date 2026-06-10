from backend.services.agent.prompt_templates.impact_analysis import ImpactAnalysisTemplate
from backend.services.agent.prompt_templates.run_crawl import RunCrawlTemplate
from backend.services.agent.prompt_templates.codebase_review import CodebaseReviewTemplate


class PromptRegistry:

    _registry = {
        "impact_analysis": ImpactAnalysisTemplate(),
        "run_crawl": RunCrawlTemplate(),

        # NEW PRIMARY INTENT
        "codebase_review": CodebaseReviewTemplate(),
    }

    @classmethod
    def get(cls, intent: str):
        return cls._registry.get(intent)