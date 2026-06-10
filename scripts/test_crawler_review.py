import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.indexing.index_service import IndexService
from backend.services.graph.call_graph_service import CallGraphService
from backend.services.analysis.crawler_review_service import CrawlerReviewService


def run_test():

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    # ✅ unified config
    project_config = {
        "project_id": "idm-dev-agent",
        "root_path": project_root,
        "name": "IDM-Dev-Agent",
        "index_cache_enabled": False,
        "language": "python"
    }

    # ----------------------------
    # INDEX LAYER
    # ----------------------------
    index_service = IndexService(project_config)

    # ----------------------------
    # GRAPH LAYER (FIX HERE)
    # ----------------------------
    index_path = os.path.join(project_root, "backend", "services", "indexing")

    graph_service = CallGraphService(index_path)

    # ----------------------------
    # REVIEW LAYER
    # ----------------------------
    review_service = CrawlerReviewService(
        index_service=index_service,
        graph_service=graph_service
    )

    result = review_service.build_review_context()

    print("\n===== ARCHITECTURE SUMMARY =====\n")
    print(result.get("architecture_summary"))

    print("\n===== HOTSPOTS =====\n")
    for h in result.get("hotspots", [])[:10]:
        print(h)

    print("\n===== MODULES =====\n")
    print(result.get("modules")[:20])


if __name__ == "__main__":
    run_test()