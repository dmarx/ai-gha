"""Special summary generators for project-wide summaries."""
import ast
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger

class SpecialSummariesGenerator:
    """Generate special project-wide summary files."""
    
    def __init__(self, root_dir: str | Path):
        """Initialize generator with root directory.
        
        Args:
            root_dir: Root directory to generate summaries for
        """
        self.root_dir = Path(root_dir)
        self.summaries_dir = self.root_dir / "SUMMARIES"
    
    def _find_readmes(self, include_root: bool = True) -> List[Path]:
        """Find all README files in the project.
        
        Args:
            include_root: Whether to include the root README.md
            
        Returns:
            List of paths to README files
        """
        readmes = []
        for file in self.root_dir.rglob("README.md"):
            # Skip the root README if not included
            if not include_root and file.parent == self.root_dir:
                continue
            readmes.append(file)
        return sorted(readmes)
    
    def _get_python_signatures(self, file_path: Path) -> List[str]:
        """Extract function and class signatures from a Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            List of signature strings
        """
        try:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())
            
            signatures = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = []
                    for arg in node.args.args:
                        args.append(arg.arg)
                    signatures.append(f"def {node.name}({', '.join(args)})")
                    
                elif isinstance(node, ast.ClassDef):
                    bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                    base_str = f"({', '.join(bases)})" if bases else ""
                    signatures.append(f"class {node.name}{base_str}")
                    
            return signatures
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return []
    
    def _build_python_tree(self) -> Dict[Path, List[str]]:
        """Build a tree of Python files and their signatures.
        
        Returns:
            Dictionary mapping file paths to lists of signatures
        """
        tree = {}
        for file in self.root_dir.rglob("*.py"):
            if any(part.startswith('.') for part in file.parts):
                continue
            if '__pycache__' in file.parts:
                continue
            signatures = self._get_python_signatures(file)
            if signatures:  # Only include files with actual signatures
                tree[file] = signatures
        return tree
    
    def generate_special_summaries(self) -> List[Path]:
        """Generate all special summary files.
        
        Returns:
            List of paths to generated summary files
        """
        self.summaries_dir.mkdir(exist_ok=True)
        generated_files = []
        
        # Generate READMEs.md
        readmes_path = self.summaries_dir / "READMEs.md"
        readme_content = []
        for readme in self._find_readmes(include_root=True):
            rel_path = readme.relative_to(self.root_dir)
            readme_content.extend([
                "=" * 80,
                f"# {rel_path}",
                "=" * 80,
                readme.read_text(),
                "\n"
            ])
        readmes_path.write_text("\n".join(readme_content))
        generated_files.append(readmes_path)
        
        # Generate README_SUBs.md
        subs_path = self.summaries_dir / "README_SUBs.md"
        subs_content = []
        for readme in self._find_readmes(include_root=False):
            rel_path = readme.relative_to(self.root_dir)
            subs_content.extend([
                "=" * 80,
                f"# {rel_path}",
                "=" * 80,
                readme.read_text(),
                "\n"
            ])
        subs_path.write_text("\n".join(subs_content))
        generated_files.append(subs_path)
        
        # Generate PYTHON.md
        python_path = self.summaries_dir / "PYTHON.md"
        python_content = ["# Python Project Structure\n"]
        
        tree = self._build_python_tree()
        for file_path in sorted(tree.keys()):
            rel_path = file_path.relative_to(self.root_dir)
            python_content.extend([
                f"## {rel_path}",
                "```python",
                *tree[file_path],
                "```\n"
            ])
            
        python_path.write_text("\n".join(python_content))
        generated_files.append(python_path)
        
        return generated_files

def generate_special_summaries(root_dir: str | Path = ".") -> List[Path]:
    """Generate special summaries for the project.
    
    Args:
        root_dir: Root directory of the project
        
    Returns:
        List of paths to generated summary files
    """
    generator = SpecialSummariesGenerator(root_dir)
    return generator.generate_special_summaries()
