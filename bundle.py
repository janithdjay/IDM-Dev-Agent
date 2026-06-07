import os

# Directories we absolutely want to skip
ignored_dirs = {'agent_env', '.git', '__pycache__', 'data', 'index'}
output_file = 'codebase_snapshot.txt'

print("Bundling source code files...")
with open(output_file, 'w', encoding='utf-8') as outfile:
    for root, dirs, files in os.walk('.'):
        # Skip ignored directories in-place
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if file.endswith('.py') and file != 'bundle.py':
                file_path = os.path.join(root, file)
                outfile.write(f"\n\n# ========================================\n")
                outfile.write(f"# FILE: {file_path}\n")
                outfile.write(f"# ========================================\n\n")
                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"# Error reading file: {str(e)}\n")

print(f"Done! Open '{output_file}' and copy-paste its contents here.")