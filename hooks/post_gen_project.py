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


# initialize GitHub repository

def handle_error(err_out):
    if err_out:
        print(f"Command failed with error: {err_out}")
        exit(1)


stderr = ''
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
