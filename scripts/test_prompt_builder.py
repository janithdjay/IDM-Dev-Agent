from backend.services.agent.prompt_builder import PromptBuilder
from backend.services.analysis.crawler_review_service import CrawlerReviewService
from backend.services.indexing.index_service import IndexService
from backend.services.graph.call_graph_service import CallGraphService


def run_test():
    index_service = IndexService()
    graph_service = CallGraphService()

    crawler = CrawlerReviewService(index_service, graph_service)
    crawler_data = crawler.build_review_context()

    builder = PromptBuilder()

    prompt = builder.build(
        intent="codebase_review",
        symbol_data={
            "symbol": "IDM-CODEBASE",
            "type": "system",
            "file": "ALL",
            "parent": None,
            "reasoning": crawler_data
        },
        question="Review the entire IDM crawler system and suggest improvements",
        history=[]
    )

    print("\n================ PROMPT OUTPUT ================\n")
    print(prompt)


if __name__ == "__main__":
    run_test()