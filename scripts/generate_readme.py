from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from utils import load_config, get_project_root, commit_and_push

def generate_readme():
    project_root = get_project_root()
    
    # Load configurations
    project_config = load_config("pyproject.toml")
    readme_config = load_config("docs/readme/config.toml")
    
    # Create Jinja2 environment with paths relative to project root
    env = Environment(
        loader=FileSystemLoader([
            project_root / 'docs/readme',
            project_root / 'docs/readme/sections'
        ]),
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
    
    # Write to README.md in project root
    readme_path = project_root / 'README.md'
    with open(readme_path, 'w') as f:
        f.write(output)
    
    # Commit and push changes
    try:
        commit_and_push(
            path='README.md',
            commit_message="docs: update README",
            cwd=project_root
        )
    except subprocess.CalledProcessError as e:
        print(f"Warning: Git operation failed: {e}")
        raise

if __name__ == '__main__':
    generate_readme()
