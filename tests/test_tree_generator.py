from loguru import logger
from pathlib import Path
import pytest
from readme_generator.generators.tree_generator import (
    should_include_path,
    node_to_tree,
    generate_tree
)

@pytest.fixture
def mock_repo_with_files(mock_repo):
    """Create a mock repository with various file types"""
    # Add workflow files
    workflow_dir = mock_repo / ".github" / "workflows"
    workflow_dir.mkdir(parents=True)
    (workflow_dir / "test.yml").write_text("name: Test")
    (workflow_dir / "build.yml").write_text("name: Build")
    
    # Add various hidden files
    (mock_repo / ".env").write_text("SECRET=123")
    (mock_repo / ".github" / "README.md").write_text("# GitHub Config")
    
    # Add some regular files and directories
    docs_dir = mock_repo / "docs" / "readme" / "sections"
    docs_dir.mkdir(parents=True)
    (docs_dir / "introduction.md").write_text("# Intro")
    
    # Add some files that should typically be ignored
    cache_dir = mock_repo / "__pycache__"
    cache_dir.mkdir()
    (cache_dir / "module.pyc").write_text("cache")
    
    return mock_repo

def test_ignore_patterns():
    """Test that ignore patterns work correctly"""
    config = {
        "tool": {
            "readme": {
                "tree": {
                    "ignore_patterns": ["__pycache__", "*.pyc", ".git"]
                }
            }
        }
    }
    
    # Should exclude based on ignore patterns
    assert should_include_path(Path(".git/config"), config) is False
    assert should_include_path(Path("foo/__pycache__/bar.pyc"), config) is False
    
    # Should include everything else, including hidden files not in ignore patterns
    assert should_include_path(Path(".github/workflows/test.yml"), config) is True
    assert should_include_path(Path(".env"), config) is True
    assert should_include_path(Path("docs/readme/file.md"), config) is True
    assert should_include_path(Path(".vscode/settings.json"), config) is True  # Not in ignore patterns

def test_full_tree_generation(mock_repo_with_files, monkeypatch):
    """Test complete tree generation with various file types"""
    monkeypatch.chdir(mock_repo_with_files)
    
    # Create config that only ignores specific patterns
    (mock_repo_with_files / "pyproject.toml").write_text("""
[tool.readme.tree]
ignore_patterns = ["__pycache__", "*.pyc", ".git"]
    """)
    
    tree = generate_tree(".")
    print(f"Generated tree:\n{tree}")  # Debug output
    
    # Should include .github and workflows
    assert ".github" in tree
    assert "workflows" in tree
    assert "test.yml" in tree
    assert "build.yml" in tree
    
    # Should include other hidden files not explicitly ignored
    assert ".env" in tree
    
    # Should include regular files and directories
    assert "docs" in tree
    assert "readme" in tree
    assert "sections" in tree
    
    # Should exclude ignored patterns
    assert "__pycache__" not in tree
    assert "*.pyc" not in tree

def test_empty_directory_handling(mock_repo):
    """Test handling of empty directories"""
    # Create some empty directories
    (mock_repo / "docs" / "empty").mkdir(parents=True)
    (mock_repo / "src" / "empty").mkdir(parents=True)
    (mock_repo / "temp" / "empty").mkdir(parents=True)
    
    config = {
        "tool": {
            "readme": {
                "tree": {
                    "ignore_patterns": []
                }
            }
        }
    }
    
    # Empty directories should be excluded unless they're essential
    assert node_to_tree(mock_repo / "temp" / "empty", config) is None
    
    # Essential directories should be kept even if empty
    assert node_to_tree(mock_repo / "docs", config) is not None
    assert node_to_tree(mock_repo / "src", config) is not None

def test_debug_path_processing(mock_repo_with_files):
    """Debug test to print path processing details"""
    config = {
        "tool": {
            "readme": {
                "tree": {
                    "ignore_patterns": ["__pycache__", "*.pyc"]
                }
            }
        }
    }
    
    def debug_walk(path: Path, indent=""):
        logger.debug(f"{indent}Processing: {path}")
        logger.debug(f"{indent}Should include: {should_include_path(path, config)}")
        
        if path.is_dir():
            for child in sorted(path.iterdir()):
                debug_walk(child, indent + "  ")
    
    logger.debug("Starting debug walk of repository")
    debug_walk(mock_repo_with_files)
