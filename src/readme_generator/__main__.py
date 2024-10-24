from loguru import logger
import fire
from .generators import generate_readme, update_structure, generate_tree

class ReadmeGenerator:
    """CLI for README generation and maintenance"""
    
    def readme(self) -> None:
        """Generate and update the README.md file"""
        generate_readme()
    
    def structure(self) -> None:
        """Update the project structure documentation"""
        update_structure()
    
    def tree(self, path: str = ".") -> None:
        """Print the project structure tree"""
        print(generate_tree(path))

if __name__ == "__main__":
    fire.Fire(ReadmeGenerator)
