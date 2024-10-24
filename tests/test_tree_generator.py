from pathlib import Path
import pytest
from readme_generator.generators.tree_generator import (
    should_include_path,
    node_to_tree,
    generate_tree
)

def test_should_include_workflows():
    """Test that workflow files are included when configured"""
    config = {
        "tool": {
            "readme": {
                "tree": {
                    "ignore_patterns": [],
                    "show_workflows": True
                }
            }
        }
    }
    path = Path(".github/workflows/test.yml")
    assert should_include_path(path, config) is True

def test_workflow_directory_shown():
    """Test that .github directory is preserved even when empty"""
    config = {
        "tool": {
            "readme": {
                "tree": {
                    "ignore_patterns": [],
                    "show_workflows": True
                }
            }
        }
    }
    path = Path(".github")
    result = node_to_tree(path, config)
    assert result is not None
    assert result[0] == ".github"

@pytest.fixture
def mock_repo_with_workflows(mock_repo):
    """Create a mock repository with workflow files"""
    workflow_dir = mock_repo / ".github" / "workflows"
    workflow_dir.mkdir(parents=True)
    
    # Add some workflow files
    (workflow_dir / "test.yml").write_text("name: Test")
    (workflow_dir / "build.yml").write_text("name: Build")
    
    # Add a .github/README.md to test handling of non-workflow files
    (mock_repo / ".github" / "README.md").write_text("# GitHub Config")
    
    return mock_repo

def test_generate_tree_with_workflows(mock_repo_with_workflows, monkeypatch):
    """Test full tree generation with workflows"""
    monkeypatch.chdir(mock_repo_with_workflows)
    
    # Create minimal pyproject.toml with necessary config
    (mock_repo_with_workflows / "pyproject.toml").write_text("""
[tool.readme.tree]
ignore_patterns = ["__pycache__", "*.pyc"]
show_workflows = true
    """)
    
    tree = generate_tree(".")
    print(f"Generated tree:\n{tree}")  # Debug output
    
    assert ".github" in tree
    assert "workflows" in tree
    assert "test.yml" in tree
    assert "build.yml" in tree

def test_hidden_dirs_handling():
    """Test handling of hidden directories"""
    config = {
        "tool": {
            "readme": {
                "tree": {
                    "ignore_patterns": [],
                    "show_workflows": True
                }
            }
        }
    }
    
    # .github/workflows should be included
    workflow_path = Path(".github/workflows/test.yml")
    assert should_include_path(workflow_path, config) is True
    
    # Other hidden dirs should be excluded
    hidden_path = Path(".vscode/settings.json")
    assert should_include_path(hidden_path, config) is False

def test_debug_path_processing(mock_repo_with_workflows):
    """Debug test to print path processing details"""
    config = {
        "tool": {
            "readme": {
                "tree": {
                    "ignore_patterns": ["__pycache__", "*.pyc"],
                    "show_workflows": True
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
    debug_walk(mock_repo_with_workflows)
