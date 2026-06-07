from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

INDEX_DIR = DATA_DIR / "index"

CACHE_DIR = DATA_DIR / "cache"

SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".json"
]

IGNORED_DIRECTORIES = [
    ".git",
    "node_modules",
    "__pycache__",
    "agent_env",
    ".idea",
    ".vscode"
]