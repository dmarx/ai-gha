from pathlib import Path
from typing import Set
from loguru import logger
from jinja2 import Environment, FileSystemLoader
from .utils import load_config, get_project_root, commit_and_push

def generate_readme():
    """Generate README from templates and commit changes"""
    project_root = get_project_root()
    logger.debug(f"Project root identified as: {project_root}")
    
    logger.info("Loading configurations")
    project_config = load_config("pyproject.toml")
    
    logger.info("Setting up Jinja2 environment")
    template_dirs = [
        project_root / 'docs/readme',
        project_root / 'docs/readme/sections'
    ]
    logger.debug(f"Template directories: {template_dirs}")
    
    env = Environment(
        loader=FileSystemLoader(template_dirs),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    template = env.get_template('base.md.j2')
    
    variables = {
        'project': project_config['project'],
        'readme': project_config['tool']['readme']
    }
    
    logger.info("Rendering README template")
    output = template.render(**variables)
    
    readme_path = project_root / 'README.md'
    logger.debug(f"Writing README to: {readme_path}")
    with open(readme_path, 'w') as f:
        f.write(output)
    
    logger.info("Committing changes")
    commit_and_push('README.md')


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
        if any(pattern in str(path) for pattern in ignore_patterns):
            continue
            
        relative_path = path.relative_to(root_path)
        if any(part.startswith(".") for part in relative_path.parts):
            continue
            
        depth = len(relative_path.parts) - 1
        prefix = "    " * depth + "├── " if depth > 0 else ""
        tree_lines.append(f"{prefix}{relative_path.name}")
    
    return "\n".join(tree_lines)

def update_structure():
    """Update the structure template and commit changes"""
    project_root = get_project_root()
    template_path = "docs/readme/sections/structure.md.j2"
    full_template_path = project_root / template_path
    
    tree = generate_tree(str(project_root))
    template_content = f"""## Project Structure

```
{tree}
```
"""
    
    full_template_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_template_path, 'w') as f:
        f.write(template_content)
    
    commit_and_push(template_path)
