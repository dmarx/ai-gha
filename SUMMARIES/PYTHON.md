# Python Project Structure

## src/readme_generator/__main__.py
```python
class ReadmeGenerator
    """CLI for README generation and maintenance"""

    def readme(self) -> None
        """Generate and update the README.md file"""

    def structure(self) -> None
        """Update the project structure documentation"""

    def tree(self, path: str) -> None
        """Print the project structure tree"""


```

## src/readme_generator/generators/readme_generator.py
```python
def get_section_templates(template_dir: Path) -> List[str]
    """
    Get all section templates in proper order.
    Args:
        template_dir: Path to template directory containing sections/
    Returns:
        List of template names in desired order
    """

def generate_readme() -> None
    """Generate README from templates and commit changes"""

```

## src/readme_generator/generators/structure_generator.py
```python
def update_structure() -> None
    """Update the structure template and commit changes"""

```

## src/readme_generator/generators/tree_generator.py
```python
def should_include_path(path: Path, config: dict) -> bool
    """
    Determine if a path should be included in the tree.
    Only excludes paths that exactly match ignore patterns.
    """

def node_to_tree(path: Path, config: dict) -> Optional[Tuple[[str, list]]]
    """Convert a path to a tree node format"""

def generate_tree(root_dir: str) -> str
    """Generate a pretty directory tree"""

```

## src/readme_generator/utils.py
```python
def get_project_root() -> Path
    """
    Get the project root directory by looking for pyproject.toml
    Returns the absolute path to the project root
    """

def load_config(config_path: str) -> dict
    """
    Load configuration from a TOML file
    Args:
        config_path (str): Path to the TOML configuration file relative to project root
    Returns:
        dict: Parsed configuration data
    """

def commit_and_push(file_to_commit)
    """Commit and push changes for a specific file"""

```

## src/site_generator/__main__.py
```python
class SiteGenerator
    """CLI for static site generation."""

    def build(self, output_dir: str) -> None
        """
        Build the static site.
        Args:
            output_dir: Output directory for the site. Defaults to '_site'.
        """


def main() -> None
    """CLI entry point."""

```

## src/site_generator/generator.py
```python
def get_project_root() -> Path
    """Get the project root directory."""

def build_site(output_dir: Optional[str]) -> None
    """
    Build a static site from README content.
    Args:
        output_dir: Optional directory for site output. Defaults to '_site'.
    """

```

## src/summary_generator/__main__.py
```python
def commit_and_push(message: str, branch: str, paths: list[str | Path], base_branch: Optional[str], force: bool) -> None
    """
    Commit changes and push to specified branch.
    Args:
        message: Commit message
        branch: Branch to push to
        paths: List of paths to commit
        base_branch: Optional base branch to create new branch from
        force: If True, create fresh branch and force push (for generated content)
    """

def generate(root_dir: str, push: bool) -> list[Path]
    """
    Generate directory summaries and special summaries.
    Args:
        root_dir: Root directory to generate summaries for
        push: Whether to commit and push changes
    Returns:
        List of paths to generated summary files
    """

def main()
    """CLI entry point."""

```

## src/summary_generator/generator.py
```python
class SummaryGenerator
    """Generate summary files for each directory in the project."""

    def __init__(self, root_dir: str | Path)
        """
        Initialize generator with root directory.
        Args:
            root_dir: Root directory to generate summaries for
        """

    def should_include_file(self, file_path: Path) -> bool
        """
        Determine if a file should be included in the summary.
        Args:
            file_path: Path to file to check
        Returns:
            True if file should be included in summary
        """

    def should_include_directory(self, directory: Path) -> bool
        """
        Determine if a directory should have a summary generated.
        Args:
            directory: Directory to check
        Returns:
            True if directory should have a summary
        """

    def _collect_directories(self) -> Set[Path]
        """
        Collect all directories containing files to summarize.
        Returns:
            Set of directory paths
        """

    def generate_directory_summary(self, directory: Path) -> str
        """
        Generate a summary for a single directory.
        Args:
            directory: Directory to generate summary for
        Returns:
            Generated summary text
        """

    def generate_all_summaries(self) -> List[Path]
        """
        Generate summary files for all directories.
        Returns:
            List of paths to generated summary files
        """


```

## src/summary_generator/signature_extractor.py
```python
@dataclass
class Signature
    """Represents a Python function or class signature with documentation."""

class ParentNodeTransformer
    """Add parent references to all nodes in the AST."""

    def visit(self, node: Any) -> Any
        """Visit a node and add parent references to all its children."""


class SignatureExtractor
    """Extracts detailed signatures from Python files."""

    def get_type_annotation(self, node: Any) -> str
        """Convert AST annotation node to string representation."""

    def get_arg_string(self, arg: Any) -> str
        """Convert function argument to string with type annotation."""

    def extract_signatures(self, source: str) -> List[Signature]
        """Extract all function and class signatures from source code."""

    def format_signature(self, sig: Signature, indent: int) -> List[str]
        """Format a signature for display with proper indentation."""


def generate_python_summary(root_dir: str | Path) -> str
    """
    Generate enhanced Python project structure summary.
    Args:
        root_dir: Root directory of the project
    Returns:
        Formatted markdown string of Python signatures
    """

```

## src/summary_generator/special_summaries.py
```python
class SpecialSummariesGenerator
    """Generate special project-wide summary files."""

    def __init__(self, root_dir: str | Path)
        """Initialize generator with root directory."""

    def _find_readmes(self, include_root: bool) -> List[Path]
        """Find all README files in the project."""

    def generate_special_summaries(self) -> List[Path]
        """
        Generate all special summary files.
        Returns:
            List of paths to generated summary files
        """


def generate_special_summaries(root_dir: str | Path) -> List[Path]
    """Generate special summaries for the project."""

```

## tests/conftest.py
```python
def temp_dir()
    """Provide a clean temporary directory"""

def mock_repo(temp_dir)
    """Create a mock repository structure for testing"""

```

## tests/test_generators.py
```python
def test_tree_generator(mock_repo)
    """Test tree generation with mock repository"""

def test_load_config(mock_repo)
    """Test configuration loading"""

def test_project_root(mock_repo, monkeypatch)
    """Test project root detection"""

```

## tests/test_site_generator.py
```python
def temp_site_dir(tmp_path)
    """Provide a temporary directory for site output."""

def mock_readme(tmp_path)
    """Create a mock README file."""

def mock_template(tmp_path)
    """Create a mock template file."""

def test_build_site(temp_site_dir, mock_readme, mock_template, monkeypatch)
    """Test basic site generation."""

def test_build_site_missing_template(temp_site_dir, mock_readme, monkeypatch)
    """Test handling of missing template."""

def test_build_site_missing_readme(temp_site_dir, mock_template, monkeypatch)
    """Test handling of missing README."""

```

## tests/test_summary_generator.py
```python
def temp_project(tmp_path)
    """Create a temporary project structure."""

def generator(temp_project)
    """Create a summary generator instance."""

def test_should_include_file(generator)
    """Test file inclusion logic."""

def test_generate_directory_summary(generator, temp_project)
    """Test summary generation for a directory."""

def test_generate_all_summaries(generator, temp_project)
    """Test generating summaries for all directories."""

```

## tests/test_tree_generator.py
```python
def mock_repo_with_files(mock_repo)
    """Create a mock repository with various file types"""

def test_ignore_patterns()
    """Test that ignore patterns work correctly"""

def test_full_tree_generation(mock_repo_with_files, monkeypatch)
    """Test complete tree generation with various file types"""

def test_empty_directory_handling(mock_repo)
    """Test handling of empty directories"""

def test_debug_path_processing(mock_repo_with_files)
    """Debug test to print path processing details"""

def debug_walk(path: Path, indent)

```
