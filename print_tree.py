# print_tree.py
from pathlib import Path

def print_directory_tree(root_dir: Path, current_dir: Path, prefix: str = "", ignore_dirs=None):
    if ignore_dirs is None:
        # Explicitly omit environments, caches, and raw data indexing paths
        ignore_dirs = {
            ".git", 
            "__pycache__", 
            "agent_env", 
            "venv", 
            ".venv", 
            "node_modules", 
            "data", 
            "index", 
            "index_data"
        }
        
    try:
        # Gather and sort files so folders appear cleanly structured
        paths = sorted(list(current_dir.iterdir()), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        # Handle system folders or restricted files gracefully
        return

    for i, path in enumerate(paths):
        if path.name in ignore_dirs:
            continue
            
        is_last = (i == len(paths) - 1)
        connector = "└── " if is_last else "├── "
        
        print(f"{prefix}{connector}{path.name}")
        
        # Recurse if the path is a directory
        if path.is_dir():
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_directory_tree(root_dir, path, new_prefix, ignore_dirs)

if __name__ == "__main__":
    project_root = Path(".")
    print(f"\n📁 {project_root.resolve().name}/")
    print_directory_tree(project_root, project_root)