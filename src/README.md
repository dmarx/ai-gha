# Source Packages

This directory contains the core packages for the project. Each package follows consistent conventions and patterns to maintain clean, maintainable, and LLM-friendly code.

## Package Organization

- Each package is self-contained and focused
- READMEs document package-specific details
- Tests live in the root `tests/` directory

## Development Conventions

### Code Style
- Keep files short and focused (see development guidelines in main README)
- Use relative imports within packages
- Follow consistent naming patterns
- Avoid filenames that conflict with GitHub conventions

### Dependencies
- All dependencies declared in root `pyproject.toml`
- No package-level `requirements.txt` or `setup.py`
- Use optional dependencies for package-specific needs

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
- Follow consistent commit message patterns
- Let workflows handle automated commits

## Current Packages
- `readme_generator/`: Dynamic README generation and maintenance
- `site_generator/`: Static site generation for demo purposes
