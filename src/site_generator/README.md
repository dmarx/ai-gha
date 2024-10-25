# Site Generator Package

Simple static site generator for demo purposes. Currently focused on serving the project's README as a GitHub Pages site.

## Components

### Core Modules
- `generator.py`: Core site generation logic
- `__main__.py`: CLI entrypoint

## Features
- Markdown to HTML conversion
- Template-based page generation
- GitHub-style rendering
- Dark/light mode support
- Mobile-responsive design

## Usage

```bash
# Generate site with default settings
python -m site_generator build

# Specify custom output directory
python -m site_generator build --output_dir="custom_dir"
```

## Templates
Templates are stored in `docs/site/`:
- `template.html`: Base HTML template
- Additional assets (if added)

## Testing

Package-specific tests are in `tests/`:
- `test_site_generator.py`

Run tests with:
```bash
pytest tests/
```

## Customization
The site can be customized by:
- Modifying the HTML template
- Adding custom CSS/JS
- Extending the generator for additional pages
