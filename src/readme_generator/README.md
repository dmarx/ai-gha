# README Generator Package

Core package for dynamic README generation and maintenance.

## Conventions

- Use `loguru` for all logging
- Use `fire` for CLI interfaces
- Use `pytest` for all testing
- Keep files short and focused (see development guidelines in main README)
- Avoid filenames that conflict with GitHub conventions (e.g., no `readme.py`)
- Use relative imports within the package
- All git operations should use `utils.commit_and_push`

## Project-Wide Dependencies

Dependencies should be declared in `pyproject.toml`, not in individual `requirements.txt` files or `setup.py`. This keeps our dependency management centralized and modern.

## Testing

- Write tests for all new functionality
- Use `pytest` fixtures for common test setups
- Keep tests focused and well-documented
- Run tests locally before pushing: `pytest tests/`
- All workflows depend on tests passing

## Directory Structure

- `generators/`: Individual generation components
- `utils.py`: Shared utilities
- `__main__.py`: CLI entrypoint

## Development Workflow

1. Write tests first (TDD approach)
2. Implement functionality
3. Ensure tests pass locally
4. Push changes (workflows will verify tests)
