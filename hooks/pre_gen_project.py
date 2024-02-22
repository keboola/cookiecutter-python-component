import subprocess

repo_url = '{{ cookiecutter.repository_url }}'
if repo_url:
    try:
        subprocess.run(["git", "--version"])
    except:
        print('ERROR: git is not installed! Either install it or leave the repository_url empty')
