================================================================================
# .github/workflows/README.md
================================================================================
# GitHub Actions Workflows

Automated workflows for project maintenance.

## Conventions
- Use Python's `commit_and_push` utility instead of git steps
- Keep workflows focused and modular
- Reuse virtual environments when possible
- Install project as package instead of managing dependencies directly
- All workflows should have a `workflow_dispatch` event trigger
- Each workflow should trigger on changes to its own file
- Use `.[all]` for complete dependency installation

## Key Workflows
- `build-readme.yml`: README generation
- `update-structure.yml`: Structure documentation
- `deploy-pages.yml`: GitHub Pages deployment
- `test.yml`: Core test suite

## Creating New Workflows
1. Follow existing workflow patterns
2. Use Python scripts for complex operations
3. Install project with `pip install -e ".[all]"`
4. Use `commit_and_push` from utils for git operations
5. Add workflow file to its own trigger paths
6. Consider adding workflow descriptions to structure documentation



================================================================================
# docs/README.md
================================================================================
# Documentation

Project documentation and templates.

## Conventions

- Use Jinja2 for templates
- Keep documentation focused and modular
- Put README templates in `readme/`
- Follow markdown best practices
- Keep sections independent

## Directory Structure

- `readme/`: README generation templates
  - Templates use `.md.j2` extension
  - Sections are modular and focused
  - Configuration in `pyproject.toml`

## Adding Documentation

1. Choose appropriate subdirectory
2. Follow existing patterns and conventions
3. Update structure documentation if needed



================================================================================
# docs/readme/README.md
================================================================================
# README Templates

Templates and sections for dynamic README generation.

## Conventions

- Use Jinja2 templates with `.md.j2` extension
- Base template goes in this directory
- Individual sections go in `sections/`
- Section templates should be focused and modular
- Variables come from `pyproject.toml`
- Follow markdown best practices

## Directory Structure

- `base.md.j2`: Main README template
- `sections/`: Individual section templates
  - Each section should focus on one aspect
  - Name templates descriptively: `<topic>.md.j2`
  - Keep sections modular and independent

## Adding New Sections

1. Create new section in `sections/`
2. Add to `base.md.j2` using include
3. Add any needed variables to `pyproject.toml`



================================================================================
# docs/site/README.md
================================================================================
# Site Templates

This directory contains templates and assets for the project's GitHub Pages site.

## Overview
The site generator creates a simple static site that displays the project's README with GitHub-style formatting.

## Files
- `template.html`: Base template for the generated site
  - Uses GitHub markdown styling
  - Supports dark/light mode
  - Responsive design
  - Code syntax highlighting

## Customization
To customize the site appearance:
1. Modify `template.html`
2. Add custom CSS in the template
3. Add custom JavaScript if needed

Note: The site generator is intentionally minimal, serving only as a demo of GitHub Actions integration.



================================================================================
# src/README.md
================================================================================
# Source Packages
This directory contains the core packages for the project. The codebase follows strict separation of concerns and modular design principles to maintain clean, maintainable, and LLM-friendly code.

## Core Principles
### Separation of Concerns
- Each package has a single, well-defined responsibility
- Packages are independent and self-contained
- Cross-cutting concerns (logging, CLI) use consistent patterns
- New features should be built as separate packages when appropriate
- Shared utilities only for truly common functionality

### Package Organization
- Each package is self-contained and focused
- READMEs document package-specific details
- Tests live in the root `tests/` directory
- Common patterns implemented independently per package

## Development Conventions
### Code Style
- Keep files short and focused (see development guidelines in main README)
- Use relative imports within packages
- Follow consistent naming patterns
- Avoid filenames that conflict with GitHub conventions
- Type hints should use:
  - Built-in generics over typing module (PEP 585)
    ```python
    # Good
    def process_items(items: list[str]) -> dict[str, int]:
        pass
        
    # Avoid
    from typing import List, Dict
    def process_items(items: List[str]) -> Dict[str, int]:
        pass
    ```
  - Union operator (`|`) over Optional (PEP 604)
    ```python
    # Good
    def get_value(key: str) -> str | None:
        pass
        
    # Avoid
    from typing import Optional
    def get_value(key: str) -> Optional[str]:
        pass
    ```
  - Enable flake8-pep585 in your editor to automatically flag outdated syntax

### Dependencies
- All dependencies declared in root `pyproject.toml`
- Dependencies organized into optional feature groups
- Use `[all]` for complete development environment
- Example usage:
  ```bash
  # Install specific features
  pip install -e ".[test]"     # Just testing deps
  pip install -e ".[site]"     # Just site generation deps
  
  # Install everything
  pip install -e ".[all]"      # All optional dependencies
  ```

### Logging & CLI
- Use `loguru` for all logging
- Use `fire` for CLI interfaces
- Consistent command patterns across packages

### Testing
- Write tests first (TDD approach)
- Use `pytest` fixtures for common setups
- Keep tests focused and well-documented
- Run tests locally before pushing
- All workflows depend on tests passing

### Git Operations
- Use `utils.commit_and_push` for all git operations
  - Set `force=True` for workflow-owned branches (e.g., generated content)
  - Use default behavior for normal collaborative branches
- Follow consistent commit message patterns
- Let workflows handle automated commits

## Current Packages
- `readme_generator/`: Dynamic README generation and maintenance
- `site_generator/`: Static site generation for demo purposes
- `summary_generator/`: Project content summary generation for LLM context. Outputs to `summaries` branch.



================================================================================
# src/readme_generator/README.md
================================================================================
# README Generator Package

Core package for dynamic README generation and maintenance.

## Components

### Generators
- `readme_generator.py`: Core README generation logic
- `structure_generator.py`: Project structure documentation
- `tree_generator.py`: Directory tree visualization

### Utilities
- `utils.py`: Shared utility functions
- `__main__.py`: CLI entrypoint

## Features
- Template-based README generation
- Automatic structure documentation
- Directory tree visualization
- Git integration for automated updates

## Usage

```bash
# Generate README
python -m readme_generator readme

# Update structure documentation
python -m readme_generator structure

# Generate directory tree
python -m readme_generator tree
```

## Testing

Package-specific tests are in `tests/`:
- `test_generators.py`
- `test_tree_generator.py`

Run tests with:
```bash
pytest tests/
```



================================================================================
# src/readme_generator/generators/README.md
================================================================================
# Generators

Component generators for various parts of the project.

## Conventions

- Each generator should be in its own file
- Keep files focused on a single generation task
- Follow naming pattern: `*_generator.py`
- Expose public functions through `__init__.py`
- All git operations should use `utils.commit_and_push`
- Each generator should be independently usable

## Key Components

- `readme_generator.py`: Main README generation
- `structure_generator.py`: Project structure documentation
- `tree_generator.py`: Directory tree generation utilities

## Adding New Generators

1. Create a new `*_generator.py` file
2. Implement the generator function
3. Export it in `__init__.py`
4. Update CLI if needed



================================================================================
# src/site_generator/README.md
================================================================================
# Site Generator Package

Simple static site generator for demo purposes. Currently focused on serving the project's README as a GitHub Pages site.

## Components

### Core Modules
- `generator.py`: Core site generation logic
- `__main__.py`: CLI entrypoint

## Features
- Markdown to HTML conversion
- Template-based page generation
- GitHub-style rendering
- Dark/light mode support
- Mobile-responsive design

## Usage

```bash
# Generate site with default settings
python -m site_generator build

# Specify custom output directory
python -m site_generator build --output_dir="custom_dir"
```

## Templates
Templates are stored in `docs/site/`:
- `template.html`: Base HTML template
- Additional assets (if added)

## Testing

Package-specific tests are in `tests/`:
- `test_site_generator.py`

Run tests with:
```bash
pytest tests/
```

## Customization
The site can be customized by:
- Modifying the HTML template
- Adding custom CSS/JS
- Extending the generator for additional pages



================================================================================
# src/summary_generator/README.md
================================================================================
# Summary Generator

Generate directory summaries to assist LLM interactions by providing focused context for each directory.

## Features

- Generates `SUMMARY` files containing concatenated content of all text files
- Skips binary files and common excludes
- Uses relative paths for file references
- Integrates with project git utilities
- Provides both API and CLI interfaces

## Usage

### Command Line

```bash
# Generate summaries for current directory
python -m summary_generator

# Generate for specific directory
python -m summary_generator /path/to/dir

# Generate without pushing changes
python -m summary_generator --push=false
```

### Python API

```python
from summary_generator import SummaryGenerator

# Create generator
generator = SummaryGenerator(".")

# Generate summaries
summary_files = generator.generate_all_summaries()
```

## Development

This package follows the project's development guidelines:

- Files are short and focused
- Uses loguru for logging
- Provides CLI through fire
- Follows consistent patterns
- Uses shared git utilities

## Testing

Tests are located in the root `tests/` directory. Run with:

```bash
pytest tests/test_summary_generator.py
```


