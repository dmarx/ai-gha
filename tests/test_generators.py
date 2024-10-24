from pathlib import Path
import pytest
from readme_generator.generators.tree_generator import generate_tree
from readme_generator.generators.readme_generator import generate_readme
from readme_generator.utils import get_project_root, load_config

def test_tree_generator(mock_repo):
    """Test tree generation with mock repository"""
    tree = generate_tree(str(mock_repo))
    assert "docs" in tree
    assert "src" in tree
    assert "pyproject.toml" in tree

def test_load_config(mock_repo):
    """Test configuration loading"""
    config = load_config(str(mock_repo / "pyproject.toml"))
    assert config["project"]["name"] == "test-project"
    assert config["project"]["version"] == "0.1.0"

def test_project_root(mock_repo, monkeypatch):
    """Test project root detection"""
    monkeypatch.chdir(mock_repo)
    root = get_project_root()
    assert root.samefile(mock_repo)
