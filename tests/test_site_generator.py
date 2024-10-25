"""Tests for site generation functionality."""
import pytest
from pathlib import Path

from site_generator.generator import build_site

@pytest.fixture
def temp_site_dir(tmp_path):
    """Provide a temporary directory for site output."""
    return tmp_path / "site"

@pytest.fixture
def mock_readme(tmp_path):
    """Create a mock README file."""
    readme = tmp_path / "README.md"
    readme.write_text("# Test\nThis is a test README.")
    return readme

@pytest.fixture
def mock_template(tmp_path):
    """Create a mock template file."""
    template_dir = tmp_path / "docs" / "site"
    template_dir.mkdir(parents=True)
    template = template_dir / "template.html"
    template.write_text("<html><body>{{content}}</body></html>")
    return template

def test_build_site(temp_site_dir, mock_readme, mock_template, monkeypatch):
    """Test basic site generation."""
    # Mock get_project_root to use our temp directory
    monkeypatch.setattr(
        "site_generator.generator.get_project_root",
        lambda: mock_readme.parent
    )
    
    # Build site
    build_site(str(temp_site_dir))
    
    # Verify output
    assert temp_site_dir.exists()
    assert (temp_site_dir / "index.html").exists()
    
    # Check content
    content = (temp_site_dir / "index.html").read_text()
    assert '<h1 id="test">Test</h1>' in content
    assert "This is a test README." in content

def test_build_site_missing_template(temp_site_dir, mock_readme, monkeypatch):
    """Test handling of missing template."""
    # Mock get_project_root to use our temp directory
    monkeypatch.setattr(
        "site_generator.generator.get_project_root",
        lambda: mock_readme.parent
    )
    
    with pytest.raises(FileNotFoundError, match="Template not found"):
        build_site(str(temp_site_dir))

def test_build_site_missing_readme(temp_site_dir, mock_template, monkeypatch):
    """Test handling of missing README."""
    # Mock get_project_root to use template directory parent
    monkeypatch.setattr(
        "site_generator.generator.get_project_root",
        lambda: mock_template.parent.parent.parent
    )
    
    with pytest.raises(FileNotFoundError, match="README not found"):
        build_site(str(temp_site_dir))
