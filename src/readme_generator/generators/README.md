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
