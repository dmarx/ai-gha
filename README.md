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
## GitHub Pages

### Site Generation

The project includes automated GitHub Pages deployment through GitHub Actions. The site is automatically rebuilt whenever the README is updated.

### Setup

1. **Enable GitHub Pages**
   - Go to Repository Settings → Pages
   - Set Source to "GitHub Actions"

2. **Install Dependencies**
   ```bash
   # Install with docs dependencies
   pip install -e ".[docs]"
   ```

3. **Local Development**
   ```bash
   # Generate site locally
   python -m readme_generator site
   
   # Specify custom output directory
   python -m readme_generator site --output_dir="custom_dir"
   ```

### Features

- Automatic dark/light mode support
- Mobile-responsive design
- GitHub-style markdown rendering
- Code syntax highlighting
- Automatic deployment
- Table of contents with anchor links

### GitHub Actions Integration

The site automatically rebuilds and deploys when:
- The README is updated through the `build-readme` workflow
- The workflow is manually triggered

### Command Line Usage

```bash
# Basic site generation
python -m readme_generator site

# Custom output directory
python -m readme_generator site --output_dir="custom_dir"
```

### Development

The site generator follows the project's modular design principles:
- Located in `generators/site_generator.py`
- Uses `loguru` for logging
- Implements comprehensive error handling
- Includes pytest-based test suite

### Customization

The site template is located in `docs/site/template.html` and can be customized with:
- Custom CSS styles
- Additional JavaScript
- Modified layout and structure
- Custom header/footer content
## Project Structure

The repository is organized as follows:

```
ai-gha
├── .github
│   └── workflows
│       ├── README.md
│       ├── build-readme.yml
│       ├── deploy-gh-pages.yml
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
│   └── site_generator
│       ├── README.md
│       ├── __init__.py
│       ├── __main__.py
│       └── generator.py
└── tests
    ├── conftest.py
    ├── test_generators.py
    ├── test_site_generator.py
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