from pathlib import Path
import tomli
import os
import subprocess
from typing import Dict, Any, List, Optional, Union, Tuple

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

def commit_and_push(
    path: Optional[str] = None,
    commit_message: str = "update",
    *,
    author_name: str = "github-actions[bot]",
    author_email: str = "github-actions[bot]@users.noreply.github.com",
    skip_ci: bool = True,
    cwd: Optional[Union[str, Path]] = None
) -> None:
    """
    Add a specific file (if provided), commit, and push changes.
    If no file is specified, commits all staged changes.
    
    Args:
        path (Optional[str]): Specific file path to commit
        commit_message (str): Commit message
        author_name (str): Git author name
        author_email (str): Git author email
        skip_ci (bool): Whether to append [skip ci] to commit message
        cwd (Optional[Union[str, Path]]): Working directory for git commands
        
    Raises:
        subprocess.CalledProcessError: If any git command fails
    """
    # Set git configuration
    subprocess.run(['git', 'config', '--local', 'user.name', author_name], cwd=cwd, check=True)
    subprocess.run(['git', 'config', '--local', 'user.email', author_email], cwd=cwd, check=True)
    
    # Add specific file if provided
    if path:
        subprocess.run(['git', 'add', path], cwd=cwd, check=True)
    
    # Prepare commit message
    if skip_ci:
        commit_message = f"{commit_message} [skip ci]"
    
    try:
        # Attempt to commit
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=cwd, check=True)
        # Push if commit succeeds
        subprocess.run(['git', 'push'], cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        # If the error is due to nothing to commit, that's fine
        if "nothing to commit" not in str(e.stderr):
            raise
