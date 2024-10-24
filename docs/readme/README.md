# README Templates

Templates and sections for dynamic README generation.

## Conventions

- Use Jinja2 templates with `.md.j2` extension
- Base template goes in this directory
- Individual sections go in `sections/`
- Section templates should be focused and modular
- Variables come from `pyproject.toml`
- Follow markdown best practices

## Directory Structure

- `base.md.j2`: Main README template
- `sections/`: Individual section templates
  - Each section should focus on one aspect
  - Name templates descriptively: `<topic>.md.j2`
  - Keep sections modular and independent

## Adding New Sections

1. Create new section in `sections/`
2. Add to `base.md.j2` using include
3. Add any needed variables to `pyproject.toml`
