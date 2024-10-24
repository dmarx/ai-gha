from pathlib import Path
from loguru import logger
from jinja2 import Environment, FileSystemLoader
from ..utils import load_config, get_project_root, commit_and_push

def generate_readme() -> None:
    """Generate README from templates and commit changes"""
    project_root = get_project_root()
    logger.debug(f"Project root identified as: {project_root}")
    
    logger.info("Loading configurations")
    project_config = load_config("pyproject.toml")
    
    logger.info("Setting up Jinja2 environment")
    template_dirs = [
        project_root / 'docs/readme',
        project_root / 'docs/readme/sections'
    ]
    logger.debug(f"Template directories: {template_dirs}")
    
    env = Environment(
        loader=FileSystemLoader(template_dirs),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    template = env.get_template('base.md.j2')
    
    variables = {
        'project': project_config['project'],
        'readme': project_config['tool']['readme']
    }
    
    logger.info("Rendering README template")
    output = template.render(**variables)
    
    readme_path = project_root / 'README.md'
    logger.debug(f"Writing README to: {readme_path}")
    with open(readme_path, 'w') as f:
        f.write(output)
    
    logger.info("Committing changes")
    commit_and_push('README.md')
