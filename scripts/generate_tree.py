from pathlib import Path
import os
from typing import List, Set

def should_ignore(path: str, ignore_patterns: Set[str]) -> bool:
    """Check if path should be ignored based on patterns"""
    return any(
        pattern in path
        for pattern in ignore_patterns
    )

def generate_tree(
    root_dir: str = ".",
    ignore_patterns: Set[str] = {
        "__pycache__", 
        ".git", 
        ".venv", 
        "*.pyc", 
        ".github",
        ".pytest_cache",
        ".vscode",
        ".idea"
    }
) -> str:
    """Generate a markdown-formatted directory tree"""
    tree_lines = []
    root_path = Path(root_dir)

    for path in sorted(Path(root_dir).rglob("*")):
        if should_ignore(str(path), ignore_patterns):
            continue
            
        # Get relative path from root
        relative_path = path.relative_to(root_path)
        depth = len(relative_path.parts) - 1
        
        # Skip if it's in the ignore list
        if any(part.startswith(".") for part in relative_path.parts):
            continue
            
        # Add the tree line
        prefix = "    " * depth + "├── " if depth > 0 else ""
        tree_lines.append(f"{prefix}{relative_path.name}")
    
    return "\n".join(tree_lines)

if __name__ == "__main__":
    # Generate tree and write to structured output for GitHub Actions
    tree = generate_tree()
    print(f"::set-output name=tree::{tree}")
