"""Core site generation functionality."""
from pathlib import Path
from typing import Optional

from loguru import logger
import markdown2

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent

def build_site(output_dir: Optional[str] = None) -> None:
    """
    Build a static site from README content.
    
    Args:
        output_dir: Optional directory for site output. Defaults to '_site'.
    """
    logger.info("Starting site generation")
    
    root = get_project_root()
    output_path = Path(output_dir or "_site")
    template_path = root / "docs" / "site" / "template.html"
    readme_path = root / "README.md"
    
    logger.debug(f"Using output directory: {output_path}")
    logger.debug(f"Using template: {template_path}")
    logger.debug(f"Using README: {readme_path}")
    
    # Validate paths
    if not template_path.exists():
        logger.error(f"Template not found: {template_path}")
        raise FileNotFoundError(f"Template not found: {template_path}")
        
    if not readme_path.exists():
        logger.error(f"README not found: {readme_path}")
        raise FileNotFoundError(f"README not found: {readme_path}")
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    logger.debug("Created output directory")
    
    # Read template
    logger.debug("Loading template")
    with template_path.open() as f:
        template = f.read()
    
    # Convert README
    logger.info("Converting README to HTML")
    with readme_path.open() as f:
        md_content = f.read()
        html_content = markdown2.markdown(
            md_content,
            extras=['fenced-code-blocks', 'tables', 'header-ids']
        )
    
    # Generate final HTML
    logger.debug("Generating final HTML")
    final_html = template.replace('{{content}}', html_content)
    
    # Write output
    output_file = output_path / "index.html"
    logger.info(f"Writing site to: {output_file}")
    with output_file.open('w') as f:
        f.write(final_html)
    
    logger.success("Site generation complete")

if __name__ == "__main__":
    build_site()
