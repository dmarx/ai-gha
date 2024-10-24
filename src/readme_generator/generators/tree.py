from pathlib import Path
from typing import Optional, Tuple
from loguru import logger
from tree_format import format_tree
from ..utils import load_config

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
