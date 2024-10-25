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
