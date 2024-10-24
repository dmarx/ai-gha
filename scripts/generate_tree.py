from pathlib import Path
import os
from typing import Set
from utils import get_project_root, commit_and_push

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

def update_structure_template():
    """Update the structure template and commit changes"""
    project_root = get_project_root()
    template_path = "docs/readme/sections/structure.md.j2"
    full_template_path = project_root / template_path
    
    # Generate tree
    tree = generate_tree(str(project_root))
    
    # Format as template content
    template_content = f"""## Project Structure

```
{tree}
```
"""
    
    # Ensure directory exists
    full_template_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write template
    with open(full_template_path, 'w') as f:
        f.write(template_content)
    
    # Commit and push changes
    try:
        commit_and_push(
            path=template_path,
            commit_message="docs: update structure template",
            cwd=project_root
        )
    except Exception as e:
        print(f"Warning: Failed to commit structure template: {e}")
        raise

if __name__ == "__main__":
    update_structure_template()
