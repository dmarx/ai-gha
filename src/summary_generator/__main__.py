"""CLI entry point for summary generator."""
import fire
from loguru import logger
from pathlib import Path
from . import generator
from readme_generator.utils import commit_and_push

def generate(root_dir: str = ".", push: bool = True) -> list[Path]:
    """Generate directory summaries.
    
    Args:
        root_dir: Root directory to generate summaries for
        push: Whether to commit and push changes
        
    Returns:
        List of paths to generated summary files
    """
    logger.info(f"Generating summaries for {root_dir}")
    gen = generator.SummaryGenerator(root_dir)
    summary_files = gen.generate_all_summaries()
    
    if push:
        logger.info("Committing and pushing changes")
        commit_and_push(
            message="Update directory summaries",
            branch="summaries",
            paths=summary_files,
            base_branch="main"
        )
    
    return summary_files

def main():
    """CLI entry point."""
    fire.Fire(generate)

if __name__ == "__main__":
    main()
