# README Generator Package

Core package for dynamic README generation and maintenance.

## Conventions

- Use `loguru` for all logging
- Use `fire` for CLI interfaces
- Keep files short and focused (see development guidelines in main README)
- Avoid filenames that conflict with GitHub conventions (e.g., no `readme.py`)
- Use relative imports within the package
- All git operations should use `utils.commit_and_push`

## Project-Wide Dependencies

Dependencies should be declared in `pyproject.toml`, not in individual `requirements.txt` files or `setup.py`. This keeps our dependency management centralized and modern.

## Directory Structure

- `generators/`: Individual generation components
- `utils.py`: Shared utilities
- `__main__.py`: CLI entrypoint
