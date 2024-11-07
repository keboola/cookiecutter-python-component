import os
import shutil
import subprocess

from pathlib import Path


def modify_portal_properties(repo_url):
    with open(Path('component_config/sourceCodeUrl.md'), 'w') as inp:
        inp.write(repo_url)

    with open(Path('component_config/documentationUrl.md'), 'w') as inp:
        inp.write(repo_url+"/blob/master/README.md")

    with open(Path('component_config/licenseUrl.md'), 'w') as inp:
        inp.write(repo_url+"/blob/master/LICENSE.md")


def check_precommit_module() -> None:
    if subprocess.run(["python", "-m", "pip", "show", "pre-commit"]).returncode != 0:
        print('\n[COOKIECUTTER][ERROR]: Pre-commit module is not installed! Installing..')
        subprocess.run(["python", "-m", "pip", "install", "pre-commit"])
    else:
        print('\n[COOKIECUTTER][INFO]: Module pre-commit is already installed. Proceeding...')

    print('\n[COOKIECUTTER][INFO]: Installing pre-commit hooks...')
    subprocess.run(["pre-commit", "install"])


def check_virtualenv_module() -> None:
    if subprocess.run(["python", "-m", "virtualenv", "--version"]).returncode != 0:
        print('\n[COOKIECUTTER][ERROR]: Virtualenv module is not installed! Installing...')
        subprocess.run(["python", "-m", "pip", "install", "virtualenv"])
        check_virtualenv_module()
    else:
        print('\n[COOKIECUTTER][INFO]: Module virtualenv is already installed. Proceeding...')


def create_venv_and_install_libraries() -> None:
    print('\n[COOKIECUTTER][INFO]: Creating virtual environment...')
    subprocess.run(["python", "-m", "virtualenv", "venv"])
    print('\n[COOKIECUTTER][INFO]: Virtual environment created.')

    if os.name.lower().startswith('nt'):
        pip_exec = os.path.join('venv', 'Scripts', 'pip')
        
    else:
        pip_exec = os.path.join('venv', 'bin', 'pip')

    print('\n[COOKIECUTTER][INFO]: Installing libraries...')
    subprocess.run([pip_exec, "install", "-r", "requirements.txt"])
    print('\n[COOKIECUTTER][INFO]: Libraries installed. Proceeding...')


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
        print(f"\n[COOKIECUTTER][ERROR]: Command failed with error: {err_out}")
        exit(1)

# initialize GitHub repository
print("\n[COOKIECUTTER][INFO]: Initializing github repository")
subprocess.run(["git", "init"])

if repo_url:
    print(f'\n[COOKIECUTTER][INFO]: Setting up remote to {repo_url}')
subprocess.run(["git", "remote", "add", "origin", repo_url])

print("\n[COOKIECUTTER][INFO]: Adding first commit")
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", '"Initial commit"'])

if not repo_url:
    print(
        '\n [COOKIECUTTER][WARNING]: No repository_url was set. To set the remote to your repository please use following command:\n '
        'git remote add '
        'origin PATH_TO_YOUR_REPOSITORY')


# virtualenv setup process
print("\n[COOKIECUTTER][INFO]: Pre-commit module checking...")
check_precommit_module()
print("\n[COOKIECUTTER][INFO]: Virtual environment setup process starting...")
check_virtualenv_module()
print("\n[COOKIECUTTER][INFO]: Virtual environment module was checked. Proceeding...")
create_venv_and_install_libraries()
print("\n[COOKIECUTTER][INFO]: Virtual environment setup process completed.")

project_name = '{{ cookiecutter.repository_folder_name }}'
print(f"\n[COOKIECUTTER][INFO]: Project \"{project_name}\" initialized successfully!")
