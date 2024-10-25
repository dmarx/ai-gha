"""Tests for summary generator package."""
import pytest
from pathlib import Path
from summary_generator import SummaryGenerator

@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure."""
    # Create some test files
    (tmp_path / "README.md").write_text("# Test Project")
    (tmp_path / "src").mkdir()
    (tmp_path / "src/main.py").write_text("print('hello')")
    (tmp_path / "src/utils.py").write_text("def test(): pass")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git/config").write_text("git config")
    return tmp_path

@pytest.fixture
def generator(temp_project):
    """Create a summary generator instance."""
    return SummaryGenerator(temp_project)

def test_should_include_file(generator):
    """Test file inclusion logic."""
    # Should include normal text files
    assert generator.should_include_file(Path("test.py"))
    assert generator.should_include_file(Path("test.md"))
    assert generator.should_include_file(Path("test.yml"))
    
    # Should exclude special files
    assert not generator.should_include_file(Path(".git/config"))
    assert not generator.should_include_file(Path("__pycache__/test.pyc"))
    assert not generator.should_include_file(Path("SUMMARY"))
    
    # Should exclude binary files
    assert not generator.should_include_file(Path("test.png"))
    assert not generator.should_include_file(Path("test.pyc"))

def test_generate_directory_summary(generator, temp_project):
    """Test summary generation for a directory."""
    summary = generator.generate_directory_summary(temp_project / "src")
    
    # Should include both Python files
    assert "main.py" in summary
    assert "utils.py" in summary
    assert "print('hello')" in summary
    assert "def test(): pass" in summary
    
    # Should have proper separators
    assert "=" * 80 in summary
    assert "File:" in summary

def test_generate_all_summaries(generator, temp_project):
    """Test generating summaries for all directories."""
    summary_files = generator.generate_all_summaries()
    
    # Should generate summaries in correct locations
    assert len(summary_files) == 2  # Root and src directories
    assert (temp_project / "SUMMARY") in summary_files
    assert (temp_project / "src/SUMMARY") in summary_files
    
    # Summaries should contain correct content
    root_summary = (temp_project / "SUMMARY").read_text()
    assert "# Test Project" in root_summary
    
    src_summary = (temp_project / "src/SUMMARY").read_text()
    assert "print('hello')" in src_summary
    assert "def test(): pass" in src_summary
