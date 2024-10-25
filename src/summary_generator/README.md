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
