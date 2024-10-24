# readme-generator

Template repository for GitHub Action-based agents with dynamic documentation

## Introduction

This is a template repository that provides a foundation for GitHub Action-based agents. It includes a modular system for dynamic documentation generation and other reusable components that make it easier to build and maintain agent-driven workflows.

### Key Features

- Modular documentation system with Jinja2 templates
- Automatic project structure documentation
- Reusable GitHub Actions workflows
- Centralized configuration management
- Utility functions for common operations
- Clean, maintainable architecture optimized for AI agents

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
   pip install -e .
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

### Development

This project follows a modular design principle to make it easier for AI agents to work with the codebase:

- Each component is self-contained and focused
- Configuration is centralized in `pyproject.toml`
- Utilities are designed to be reusable across workflows
- Git operations are handled through utility functions

To add new README sections:
1. Create a new template in `docs/readme/sections/`
2. Include it in `docs/readme/base.md.j2`
3. Add any necessary configuration to `pyproject.toml`
## Project Structure

```
ai-gha
├── LICENSE
├── README.md
├── docs
│   └── readme
│       ├── base.md.j2
│       ├── config.toml
│       ├── sections
│       │   ├── introduction.md.j2
│       │   ├── prerequisites.md.j2
│       │   ├── structure.md.j2
│       │   ├── todo.md.j2
│       │   └── usage.md.j2
│       └── todo.md
├── pyproject.toml
└── src
    └── readme_generator
        ├── __init__.py
        ├── __main__.py
        ├── generators.py
        └── utils.py

```
## TODO

- [ ] Add more utility functions for common agent operations
- [ ] Create workflow templates for common agent tasks
- [ ] Expand documentation with more examples
- [ ] Add testing framework
- [ ] Add more reusable components

## Support

If you encounter any issues or have questions, please check the prerequisites section first, then file an issue in the GitHub repository.