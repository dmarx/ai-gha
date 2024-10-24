from pathlib import Path
from typing import Set, List, Optional, Tuple
from loguru import logger
from jinja2 import Environment, FileSystemLoader
from tree_format import format_tree
from .utils import load_config, get_project_root, commit_and_push

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

def should_include_path(path: Path, config: dict) -> bool:
    """Determine if a path should be included in the tree"""
    path_str = str(path)
    
    # Always exclude paths matching ignore patterns
    ignore_patterns = set(config["tool"]["readme"]["tree"]["ignore_patterns"])
    if any(pattern in path_str for pattern in ignore_patterns):
        return False
    
    # Special handling for .github/workflows
    if ".github/workflows" in path_str:
        return config["tool"]["readme"]["tree"].get("show_workflows", True)
    
    # Exclude hidden files/directories unless explicitly allowed
    if path.name.startswith('.') and not ".github/workflows" in path_str:
        return False
        
    return True

def node_to_tree(path: Path, config: dict) -> Optional[Tuple[str, list]]:
    """Convert a path to a tree node format"""
    if not should_include_path(path, config):
        return None
    
    if path.is_file():
        return path.name, []
    
    children = []
    for child in sorted(path.iterdir()):
        node = node_to_tree(child, config)
        if node is not None:
            children.append(node)
    
    # If it's a directory and has no visible children, don't show it
    if not children and path.name not in {'.github', 'docs', 'src'}:
        return None
        
    return path.name, children

def generate_tree(root_dir: str = ".") -> str:
    """Generate a pretty directory tree"""
    logger.info(f"Generating tree from {root_dir}")
    
    # Load config
    project_config = load_config("pyproject.toml")
    
    root_path = Path(root_dir)
    tree_root = node_to_tree(root_path, project_config)
    
    if tree_root is None:
        return ""
    
    return format_tree(
        tree_root,
        format_node=lambda x: x[0],
        get_children=lambda x: x[1]
    )

def update_structure() -> None:
    """Update the structure template and commit changes"""
    project_root = get_project_root()
    template_path = "docs/readme/sections/structure.md.j2"
    full_template_path = project_root / template_path
    
    tree = generate_tree(str(project_root))
    template_content = f"""## Project Structure

The repository is organized as follows:

```
{tree}
```

### Key Components

- `.github/workflows/`: GitHub Actions workflow definitions
  - `build-readme.yml`: Automatically rebuilds README when content changes
  - `update-structure.yml`: Updates project structure documentation

- `docs/readme/`: README template files
  - `base.md.j2`: Main template file
  - `sections/`: Individual section templates

- `src/readme_generator/`: Core Python package
  - `generators.py`: Main generation logic
  - `utils.py`: Shared utility functions
  - `__main__.py`: CLI entry point

- `pyproject.toml`: Project configuration and dependencies
"""
    
    full_template_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_template_path, 'w') as f:
        f.write(template_content)
    
    commit_and_push(template_path)

# ... rest of the file remains the same ...
