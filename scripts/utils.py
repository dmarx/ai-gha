from pathlib import Path
import tomli
from typing import Dict, Any
import os

def get_project_root() -> Path:
    """Get the project root directory"""
    return Path(os.getcwd()).parent

def load_config(config_path: str) -> dict:
    """
    Load configuration from a TOML file
    
    Args:
        config_path (str): Path to the TOML configuration file relative to project root
        
    Returns:
        dict: Parsed configuration data
    """
    full_path = get_project_root() / config_path
    with open(full_path, "rb") as f:
        return tomli.load(f)

def merge_configs(*configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple configuration dictionaries
    
    Args:
        *configs: Variable number of configuration dictionaries
        
    Returns:
        dict: Merged configuration dictionary
    """
    result = {}
    for config in configs:
        result.update(config)
    return result
