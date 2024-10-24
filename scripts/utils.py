from pathlib import Path
import tomli
from typing import Dict, Any

def load_config(config_path: Path) -> dict:
    """
    Load configuration from a TOML file
    
    Args:
        config_path (Path): Path to the TOML configuration file
        
    Returns:
        dict: Parsed configuration data
    """
    with open(config_path, "rb") as f:
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
