import os
import shutil
import subprocess
import sys

from pathlib import Path

python_exec = sys.executable

def modify_portal_properties(repo_url):
    with open(Path('component_config/sourceCodeUrl.md'), 'w') as inp:
        inp.write(repo_url)

    with open(Path('component_config/documentationUrl.md'), 'w') as inp:
        inp.write(repo_url+"/blob/master/README.md")

    with open(Path('component_config/licenseUrl.md'), 'w') as inp:
        inp.write(repo_url+"/blob/master/LICENSE.md")

    
def check_virtualenv_module() -> None:
    if subprocess.run([python_exec, "-m", "virtualenv", "--version"]).returncode != 0:
        print('ERROR: virtualenv module is not installed! Installing..."')
        subprocess.run(["pip", "install", "virtualenv"])
        check_virtualenv_module()
    else:
        print('Module virtualenv is already installed. Proceeding...')


def create_venv_and_install_libraries() -> None:
    print('Creating virtual environment...')
    subprocess.run([python_exec, "-m", "virtualenv", "venv"])
    print('Virtual environment created.')

    if os.name.lower().startswith('nt'):
        pip_exec = os.path.join('venv', 'Scripts', 'pip')
    else:
        venv_path = os.path.join(os.getcwd(), "venv")
        pip_exec = os.path.join(venv_path, 'bin', 'pip')

    print('Installing libraries...')
    subprocess.run([pip_exec, "install", "-r", "requirements.txt"])
    print('Libraries installed. Proceeding...')



# remove redundant files and directories 
platform = '{{ cookiecutter.template_variant }}'
repo_url = '{{ cookiecutter.repository_url }}'

if platform == 'GitHub':
    modify_portal_properties(repo_url=repo_url)

REMOVE_PATHS = [
    '{% if cookiecutter.template_variant == "GitHub" %} bitbucket-pipelines.yml {% endif %}',
    '{% if cookiecutter.template_variant == "Bitbucket" %} .github {% endif %}',
    'tmp'
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

def handle_error(err_out):
    if err_out:
        print(f"Command failed with error: {err_out}")
        exit(1)

# initialize GitHub repository
print("Initializing github repository")
subprocess.run(["git", "init"])

if repo_url:
    print(f'\nSetting up remote to {repo_url}')
subprocess.run(["git", "remote", "add", "origin", repo_url])

print("\nAdding first commit")
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", '"Initial commit"'])

if not repo_url:
    print(
        '\n WARNING: No repository_url was set. To set the remote to your repository please use following command:\n '
        'git remote add '
        'origin PATH_TO_YOUR_REPOSITORY')


# virtualenv setup process
check_virtualenv_module()
create_venv_and_install_libraries()

project_name = '{{ cookiecutter.repository_folder_name }}'
print(f"\nProject \"{project_name}\" initialized successfully!")
