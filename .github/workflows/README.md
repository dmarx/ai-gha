# GitHub Actions Workflows

Automated workflows for project maintenance.

## Conventions

- Use Python's `commit_and_push` utility instead of git steps
- Keep workflows focused and modular
- Reuse virtual environments when possible
- Install project as package instead of managing dependencies directly
- All workflows should have a `workflow_dispatch` event trigger.

## Key Workflows

- `build-readme.yml`: README generation
- `update-structure.yml`: Structure documentation

## Creating New Workflows

1. Follow existing workflow patterns
2. Use Python scripts for complex operations
3. Install project with `pip install -e .`
4. Use `commit_and_push` from utils for git operations
5. Consider adding workflow descriptions to structure documentation
