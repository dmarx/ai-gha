from pathlib import Path
from loguru import logger
from ..utils import get_project_root, commit_and_push
from .tree_generator import generate_tree

def update_structure() -> None:
    """Update the structure template and commit changes"""
    project_root = get_project_root()
    template_path = "docs/readme/sections/structure.md.j2"
    full_template_path = project_root / template_path
    
    tree = generate_tree(str(project_root))
    template_content = f"""## Project Structure

The repository is organized as follows:

```
{tree}
```

### Key Components

- `.github/workflows/`: GitHub Actions workflow definitions
  - `build-readme.yml`: Automatically rebuilds README when content changes
  - `update-structure.yml`: Updates project structure documentation

- `docs/readme/`: README template files
  - `base.md.j2`: Main template file
  - `sections/`: Individual section templates

- `src/readme_generator/`: Core Python package
  - `generators/`: Generation components
    - `tree_generator.py`: Tree generation utilities
    - `readme_generator.py`: README generation logic
    - `structure_generator.py`: Structure documentation
  - `utils.py`: Shared utility functions
  - `__main__.py`: CLI entry point

- `pyproject.toml`: Project configuration and dependencies
"""
    
    full_template_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_template_path, 'w') as f:
        f.write(template_content)
    
    commit_and_push(template_path)
