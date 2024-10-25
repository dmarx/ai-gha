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
# README.md
================================================================================
# 

## Introduction

This is a template repository that provides a foundation for GitHub Action-based agents. It includes a modular system for dynamic documentation generation and other reusable components that make it easier to build and maintain agent-driven workflows.

### Key Features

- Modular documentation system with Jinja2 templates
- Automatic project structure documentation
- Reusable GitHub Actions workflows
- Centralized configuration management
- Utility functions for common operations
- Clean, maintainable architecture optimized for AI agents
- Built-in test framework with pytest
- Automated workflow dependencies
- Git operations handled through utilities
## Repository Setup

### Required Repository Settings

1. **Workflow Permissions**
   - Go to Repository Settings → Actions → General → Workflow permissions
   - Enable "Read and write permissions"
   - Check "Allow GitHub Actions to create and approve pull requests"

2. **Branch Protection** (Optional but recommended)
   - Go to Repository Settings → Branches → Branch protection rules
   - Add rule for your main branch (e.g., `main` or `master`)
   - Enable:
     - "Require pull request reviews before merging"
     - "Require status checks to pass before merging"
   - Allow:
     - "Allow specific actors to bypass required pull requests"
     - Add "github-actions[bot]" to the bypass list

### Required Secrets and Variables

No additional secrets are required for basic functionality. The workflows use the default `GITHUB_TOKEN` which is automatically provided.

### Repository Setup Commands

If you're setting up using GitHub CLI, you can run these commands:
```bash
# Enable workflows
gh repo edit --enable-actions

# Set workflow permissions
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/OWNER/REPO/actions/permissions/workflow" \
  -f default_workflow_permissions='write' \
  -F can_approve_pull_request_reviews=true

# Enable Issues (recommended for tracking)
gh repo edit --enable-issues
```

Replace `OWNER/REPO` with your repository details.

### Common Issues

1. **Workflow Permission Errors**
   - Error: "Resource not accessible by integration"
   - Solution: Ensure workflow permissions are set to "Read and write"

2. **Git Push Failures**
   - Error: "GitHub Actions is not permitted to create or approve pull requests"
   - Solution: Check "Allow GitHub Actions to create and approve pull requests"

3. **Workflow Trigger Issues**
   - Error: Workflows not triggering each other
   - Solution: Ensure `GITHUB_TOKEN` has sufficient permissions and "Read and write permissions" is enabled
## Usage

### Installation

This project is designed to be used as a template repository. To get started:

1. Click "Use this template" on GitHub
2. Clone your new repository
3. Install the development dependencies:
   ```bash
   pip install -e ".[test]"
   ```

### Dynamic README Generation

The README is automatically generated from templates in `docs/readme/`. The system works as follows:

1. Base template (`docs/readme/base.md.j2`) defines the overall structure
2. Individual sections are stored in `docs/readme/sections/` as separate templates
3. Configuration is centralized in `pyproject.toml`
4. GitHub Actions automatically rebuild the README when:
   - Templates are modified
   - Project structure changes
   - Configuration is updated

To manually trigger a README rebuild:
```bash
python -m readme_generator readme
```

### Project Structure Management

The repository includes automatic project structure documentation:

1. Structure is updated on file changes
2. Tree output is formatted as a template
3. README is automatically rebuilt to include the new structure

To manually update the structure:
```bash
python -m readme_generator structure
```

### Testing

The project uses pytest for testing. To run tests:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=readme_generator

# Run specific test file
pytest tests/test_tree_generator.py
```

Tests are automatically run:
- On every push to main
- When workflows are triggered
- Before README updates
- Before structure updates

### Development

This project follows a modular design principle to make it easier for AI agents to work with the codebase:

- Each component is self-contained and focused
- Configuration is centralized in `pyproject.toml`
- Utilities are designed to be reusable across workflows
- Git operations are handled through utility functions
- All features are tested using pytest

To add new README sections:
1. Create a new template in `docs/readme/sections/`
2. Include it in `docs/readme/base.md.j2`
3. Add any necessary configuration to `pyproject.toml`
4. Add tests for new functionality
## Development Guidelines

### Code Organization for LLM Interaction

When developing this project (or using it as a template), keep in mind these guidelines for effective collaboration with Large Language Models:

1. **Separation of Concerns**
   - Each package should have a single, clear responsibility
   - New features should be separate packages when appropriate
   - Avoid coupling between packages
   - Use consistent patterns across packages, but implement independently
   - Cross-cutting concerns should use shared conventions

2. **File Length and Modularity**
   - Keep files short and focused on a single responsibility
   - If you find yourself using comments like "... rest remains the same" or "... etc", the file is too long
   - Files should be completely replaceable in a single LLM interaction
   - Long files should be split into logical components

3. **Dependencies**
   - All dependencies managed in `pyproject.toml`
   - Optional dependencies grouped by feature:
     ```toml
     [project.optional-dependencies]
     test = ["pytest", ...]
     site = ["markdown2", ...]
     all = ["pytest", "markdown2", ...]  # Everything
     ```
   - Use appropriate groups during development:
     ```bash
     pip install -e ".[test]"  # Just testing
     pip install -e ".[all]"   # Everything
     ```

4. **Testing Standards**
   - Every new feature needs tests
   - Tests should be clear and focused
   - Use pytest fixtures for common setups
   - All workflows depend on tests passing
   - Test files should follow same modularity principles

5. **Why This Matters**
   - LLMs work best with clear, focused contexts
   - Complete file contents are better than partial updates with ellipsis
   - Tests provide clear examples of intended behavior
   - Shorter files make it easier for LLMs to:
     - Understand the complete context
     - Suggest accurate modifications
     - Maintain consistency
     - Avoid potential errors from incomplete information

6. **Real World Example**
   Our own organization follows these principles:
   ```
   src/
   ├── readme_generator/  # Core README generation
   │   ├── generators/
   │   └── utils.py
   └── site_generator/    # Demo site generation
       ├── generator.py
       └── __main__.py
   ```

7. **Best Practices**
   - Aim for files under 200 lines
   - Each file should have a single, clear purpose
   - Use directory structure to organize related components
   - Prefer many small files over few large files
   - Consider splitting when files require partial updates
   - Write tests alongside new features
   - Run tests locally before pushing
# LLM-Focused Summary System

## Overview
The project includes an automated summary generation system designed to help LLMs efficiently work with the codebase. This system generates both local directory summaries and project-wide summaries to provide focused, relevant context for different tasks.

## Types of Summaries

### Directory Summaries
Each directory in the project contains a `SUMMARY` file that concatenates all text files in that directory. This provides focused, local context when working on directory-specific tasks.

### Project-Wide Summaries
Special project-wide summaries are maintained in the `SUMMARIES/` directory on the `summaries` branch:

- `READMEs.md`: Concatenation of all README files in the project
- `README_SUBs.md`: Same as above but excluding the root README
- `PYTHON.md`: Structured view of all Python code including:
  - Function and class signatures
  - Type hints
  - Docstrings
  - Clear indication of class membership

## Accessing Summaries

### Directory Summaries
These are available on any branch in their respective directories:
```bash
# Example: View summary for the readme_generator package
cat src/readme_generator/SUMMARY
```

### Project-Wide Summaries
These live exclusively on the `summaries` branch:
```bash
# Switch to summaries branch
git checkout summaries

# View available summaries
ls SUMMARIES/
```

## Using Summaries Effectively

### For Local Development
Directory summaries are useful when:
- Getting up to speed on a specific package
- Understanding local code context
- Planning modifications to a package

### For Project-Wide Understanding
The `SUMMARIES/` directory helps with:
- Understanding overall project structure
- Finding relevant code across packages
- Reviewing API signatures and documentation
- Planning cross-package changes

### For LLM Interactions
- Point LLMs to specific summaries based on the task
- Use directory summaries for focused work
- Use project-wide summaries for architectural decisions
- Combine different summaries as needed for context

## Implementation Notes
- Summaries are automatically updated on every push to `main`
- The `summaries` branch is workflow-owned and force-pushed on updates
- Summary generation is configured in `pyproject.toml` under `[tool.summary]`
- Don't modify summaries directly - they're automatically generated
## GitHub Pages

### Requirements

1. **Public Repository**
   - GitHub Pages is available out-of-the-box for public repositories
   - For private repositories, a GitHub Enterprise plan is required
   - If you plan to make your repository public later, you can still set up and test the site generation locally

2. **Repository Settings**
   - Once your repository is public (or on an Enterprise plan):
     - Go to Repository Settings → Pages
     - Under "Build and deployment":
       - Set Source to "GitHub Actions"

### Installation

```bash
# Install with site generation dependencies
pip install -e ".[all]"
```

### Local Development

The site generator can be used locally regardless of repository visibility:

```bash
# Generate site locally
python -m site_generator build

# Site will be generated in _site/ directory (git-ignored)
# View the generated site by opening _site/index.html in your browser
```

### GitHub Actions Integration

When requirements are met (public repository or Enterprise plan), the site automatically rebuilds and deploys when:
- The README is updated through the `build-readme` workflow
- The deployment workflow is modified
- The workflow is manually triggered

### File Structure

```
your-repo/
├── _site/           # Generated directory (git-ignored)
│   └── index.html   # Generated site
├── docs/
│   └── site/       
│       └── template.html  # Site template
└── src/
    └── site_generator/   # Generator package
```

### Customization

The site template is located in `docs/site/template.html` and can be customized with:
- Custom CSS styles
- Additional JavaScript
- Modified layout and structure
- Custom header/footer content

### Command Line Usage

```bash
# Generate site with default settings
python -m site_generator build

# Specify custom output directory
python -m site_generator build --output_dir="custom_dir"
```

### Testing

The site generation can be tested locally even if GitHub Pages deployment isn't available:
```bash
# Run the test suite
pytest tests/test_site_generator.py
```
## Project Structure

The repository is organized as follows:

```
ai-gha
├── .github
│   └── workflows
│       ├── README.md
│       ├── build-readme.yml
│       ├── deploy-gh-pages.yml
│       ├── generate-summaries.yml
│       ├── test.yml
│       └── update-structure.yml
├── .gitignore
├── LICENSE
├── README.md
├── docs
│   ├── README.md
│   ├── readme
│   │   ├── README.md
│   │   ├── base.md.j2
│   │   └── sections
│   │       ├── development.md.j2
│   │       ├── introduction.md.j2
│   │       ├── prerequisites.md.j2
│   │       ├── site.md.j2
│   │       ├── structure.md.j2
│   │       ├── summaries.md.j2
│   │       ├── todo.md.j2
│   │       └── usage.md.j2
│   └── site
│       ├── README.md
│       └── template.html
├── pyproject.toml
├── src
│   ├── README.md
│   ├── readme_generator
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── generators
│   │   │   ├── README.md
│   │   │   ├── __init__.py
│   │   │   ├── readme_generator.py
│   │   │   ├── structure_generator.py
│   │   │   └── tree_generator.py
│   │   └── utils.py
│   ├── site_generator
│   │   ├── README.md
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── generator.py
│   └── summary_generator
│       ├── README.md
│       ├── __init__.py
│       ├── __main__.py
│       ├── generator.py
│       ├── signature_extractor.py
│       └── special_summaries.py
└── tests
    ├── conftest.py
    ├── test_generators.py
    ├── test_site_generator.py
    ├── test_summary_generator.py
    └── test_tree_generator.py

```

### Key Components

- `.github/workflows/`: GitHub Actions workflow definitions
  - `build-readme.yml`: Automatically rebuilds README when content changes
  - `update-structure.yml`: Updates project structure documentation

- `docs/readme/`: README template files
  - `base.md.j2`: Main template file
  - `sections/`: Individual section templates

- `src/readme_generator/`: Core Python package
  - `generators/`: Generation components
    - `tree_generator.py`: Tree generation utilities
    - `readme_generator.py`: README generation logic
    - `structure_generator.py`: Structure documentation
  - `utils.py`: Shared utility functions
  - `__main__.py`: CLI entry point

- `pyproject.toml`: Project configuration and dependencies
## TODO

### Documentation Improvements
- [ ] Add automatic table of contents generation
- [ ] Add module summary with function signatures
- [ ] Expand documentation with more examples
- [ ] Add API integration instructions

### Feature Additions
- [ ] Add more utility functions for common agent operations
- [ ] Create workflow templates for common agent tasks
- [ ] Add more reusable components
- [ ] Add GitHub Pages integration for project documentation

### Testing Enhancements
- [ ] Add more test cases for edge cases
- [ ] Add integration tests for workflows
- [ ] Improve test coverage



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


