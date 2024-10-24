from pathlib import Path
from typing import Optional, Tuple
from loguru import logger
from tree_format import format_tree
from ..utils import load_config
import fnmatch

def should_include_path(path: Path, config: dict) -> bool:
    """
    Determine if a path should be included in the tree.
    Only excludes paths that exactly match ignore patterns.
    """
    path_str = str(path)
    logger.debug(f"Checking path: {path_str}")
    
    # Check against ignore patterns
    ignore_patterns = set(config["tool"]["readme"]["tree"]["ignore_patterns"])
    
    # Split path into parts and check each part against patterns
    path_parts = path_str.split('/')
    for pattern in ignore_patterns:
        for part in path_parts:
            if fnmatch.fnmatch(part, pattern):
                logger.debug(f"Path {path_str} matched ignore pattern {pattern}")
                return False
    
    logger.debug(f"Path {path_str} included")
    return True

def node_to_tree(path: Path, config: dict) -> Optional[Tuple[str, list]]:
    """Convert a path to a tree node format"""
    logger.debug(f"Processing node: {path}")
    
    if not should_include_path(path, config):
        logger.debug(f"Excluding node: {path}")
        return None
    
    if path.is_file():
        logger.debug(f"Including file: {path}")
        return path.name, []
    
    children = []
    logger.debug(f"Processing children of: {path}")
    for child in sorted(path.iterdir()):
        node = node_to_tree(child, config)
        if node is not None:
            children.append(node)
    
    # Keep directories that have children or are essential
    if not children and path.name not in {'docs', 'src'}:
        logger.debug(f"Excluding empty directory: {path}")
        return None
    
    logger.debug(f"Including directory: {path} with {len(children)} children")
    return path.name, children

def generate_tree(root_dir: str = ".") -> str:
    """Generate a pretty directory tree"""
    logger.info(f"Generating tree from {root_dir}")
    
    # Load config
    project_config = load_config("pyproject.toml")
    logger.debug(f"Loaded config: {project_config}")
    
    root_path = Path(root_dir)
    logger.debug(f"Root path: {root_path.absolute()}")
    
    tree_root = node_to_tree(root_path, project_config)
    
    if tree_root is None:
        logger.warning("No tree generated - root excluded")
        return ""
    
    return format_tree(
        tree_root,
        format_node=lambda x: x[0],
        get_children=lambda x: x[1]
    )
