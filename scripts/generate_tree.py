from pathlib import Path
import os
from typing import Set
from loguru import logger
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
    logger.info(f"Generating tree from {root_dir}")
    tree_lines = []
    root_path = Path(root_dir)

    for path in sorted(Path(root_dir).rglob("*")):
        if should_ignore(str(path), ignore_patterns):
            logger.debug(f"Ignoring {path}")
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
    
    logger.debug(f"Generated tree with {len(tree_lines)} entries")
    return "\n".join(tree_lines)

def update_structure_template():
    """Update the structure template and commit changes"""
    project_root = get_project_root()
    template_path = "docs/readme/sections/structure.md.j2"
    full_template_path = project_root / template_path
    
    logger.info("Generating directory tree")
    tree = generate_tree(str(project_root))
    
    logger.debug("Formatting template content")
    template_content = f"""## Project Structure

```
{tree}
```
"""
    
    logger.info(f"Writing template to {template_path}")
    full_template_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_template_path, 'w') as f:
        f.write(template_content)
    
    logger.info("Committing and pushing changes")
    commit_and_push(template_path)
    logger.success("Structure template update completed")

if __name__ == "__main__":
    update_structure_template()
