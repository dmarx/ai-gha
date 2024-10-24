from pathlib import Path
import tomli
import os
import subprocess
from loguru import logger

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

def merge_configs(*configs: dict) -> dict:
    """
    Merge multiple configuration dictionaries"""
    result = {}
    for config in configs:
        result.update(config)
    return result

def commit_and_push(file_to_commit):
    try:
        # Configure Git for GitHub Actions
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Action"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "action@github.com"], check=True)
        
        # Check if there are any changes to commit
        status = subprocess.run(["git", "status", "--porcelain", file_to_commit], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            logger.info(f"No changes to commit for {file_to_commit}")
            return
        
        subprocess.run(["git", "add", file_to_commit], check=True)
        subprocess.run(["git", "commit", "-m", f"Update {file_to_commit}"], check=True)
        subprocess.run(["git", "push"], check=True)
        
        logger.success(f"Changes to {file_to_commit} committed and pushed successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during git operations: {e}")
        if "nothing to commit" in str(e):
            logger.info("No changes to commit. Continuing execution")
        else:
            logger.warning("Exiting early due to Git error")
            raise
