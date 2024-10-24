from pathlib import Path
from typing import Set, List
from loguru import logger
from jinja2 import Environment, FileSystemLoader
from tree_format import format_tree
from .utils import load_config, get_project_root, commit_and_push

def node_to_tree(path: Path, ignore_patterns: Set[str]) -> tuple:
    """Convert a path to a tree node format"""
    if any(pattern in str(path) for pattern in ignore_patterns):
        return None
    
    if path.is_file():
        return path.name, []
    
    children = []
    for child in sorted(path.iterdir()):
        node = node_to_tree(child, ignore_patterns)
        if node is not None:
            children.append(node)
    
    return path.name, children

def generate_tree(root_dir: str = ".") -> str:
    """Generate a pretty directory tree"""
    logger.info(f"Generating tree from {root_dir}")
    
    # Load ignore patterns from config
    project_config = load_config("pyproject.toml")
    ignore_patterns = set(project_config["tool"]["readme"]["tree"]["ignore_patterns"])
    
    root_path = Path(root_dir)
    tree_root = node_to_tree(root_path, ignore_patterns)
    
    if tree_root is None:
        return ""
    
    return format_tree(
        tree_root,
        format_node=lambda x: x[0],
        get_children=lambda x: x[1]
    )

def generate_readme() -> None:
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

def update_structure() -> None:
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
