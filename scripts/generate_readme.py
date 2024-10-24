from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from .utils import load_config

def generate_readme():
    # Load configurations
    project_config = load_config("pyproject.toml")
    readme_config = load_config("docs/readme/config.toml")
    
    # Create Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(['docs/readme', 'docs/readme/sections']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Load base template
    template = env.get_template('base.md.j2')
    
    # Create variables structure
    variables = {
        'project': project_config['project'],
        'readme': readme_config['readme']
    }
    
    # Render template
    output = template.render(**variables)
    
    # Write to README.md in root directory
    with open('README.md', 'w') as f:
        f.write(output)

if __name__ == '__main__':
    generate_readme()
