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
- Follow consistent commit message patterns
- Let workflows handle automated commits

## Current Packages
- `readme_generator/`: Dynamic README generation and maintenance
- `site_generator/`: Static site generation for demo purposes
