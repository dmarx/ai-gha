from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from loguru import logger
from utils import load_config, get_project_root, commit_and_push

def generate_readme():
    project_root = get_project_root()
    
    logger.info("Loading configurations")
    project_config = load_config("pyproject.toml")
    readme_config = load_config("docs/readme/config.toml")
    
    logger.info("Setting up Jinja2 environment")
    env = Environment(
        loader=FileSystemLoader([
            project_root / 'docs/readme',
            project_root / 'docs/readme/sections'
        ]),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    logger.debug("Loading base template")
    template = env.get_template('base.md.j2')
    
    logger.debug("Preparing template variables")
    variables = {
        'project': project_config['project'],
        'readme': readme_config['readme']
    }
    
    logger.info("Rendering README template")
    output = template.render(**variables)
    
    readme_path = project_root / 'README.md'
    logger.info(f"Writing README to {readme_path}")
    with open(readme_path, 'w') as f:
        f.write(output)
    
    logger.info("Committing and pushing changes")
    commit_and_push('README.md')
    logger.success("README generation completed")

if __name__ == '__main__':
    generate_readme()
