"""CLI entry point for site generator."""
import fire
from loguru import logger

from .generator import build_site

class SiteGenerator:
    """CLI for static site generation."""
    
    def build(self, output_dir: str = "_site") -> None:
        """
        Build the static site.
        
        Args:
            output_dir: Output directory for the site. Defaults to '_site'.
        """
        logger.info("Building static site")
        build_site(output_dir)

def main() -> None:
    """CLI entry point."""
    fire.Fire(SiteGenerator)

if __name__ == "__main__":
    main()
