import os
import shutil
import subprocess

KDP_COMPID_PLACEHOLDER = "COOKIECUTTER_DEV_PORTAL_COMPONENT_ID"
KDP_VENDOR_PLACEHOLDER = "COOKIECUTTER_DEV_PORTAL_VENDOR_NAME"


def modify_portal_properties(repo_url):
    with open(".github/workflows/push.yml", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if KDP_COMPID_PLACEHOLDER in line:
                output = line.replace(KDP_COMPID_PLACEHOLDER, "{{ cookiecutter.dev_portal_component_id }}")
            elif KDP_VENDOR_PLACEHOLDER in line:
                output = line.replace(KDP_VENDOR_PLACEHOLDER, "{{ cookiecutter.dev_portal_vendor_name }}")
            else:
                output = line
            f.write(output)
        f.truncate()  # truncate the file to remove any leftover content

    with open("component_config/sourceCodeUrl.md", "w") as f:
        f.write(repo_url)

    with open("component_config/documentationUrl.md", "w") as f:
        f.write(repo_url + "/blob/master/README.md")

    with open("component_config/licenseUrl.md", "w") as f:
        f.write(repo_url + "/blob/master/LICENSE.md")


platform = "{{ cookiecutter.template_variant }}"
repo_url = "{{ cookiecutter.repository_url }}"

if platform == "GitHub":
    modify_portal_properties(repo_url=repo_url)

REMOVE_PATHS = [
    '{% if cookiecutter.template_variant == "GitHub" %} bitbucket-pipelines.yml {% endif %}',
    '{% if cookiecutter.template_variant == "Bitbucket" %} .github {% endif %}',
    "tmp",
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
subprocess.run(["git", "init", "-b", "main"])

if repo_url:
    print(f"\nSetting up remote to {repo_url}")
subprocess.run(["git", "remote", "add", "origin", repo_url])

print("\nAdding first commit")
subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Initial cookiecutter-template-based commit"])

if not repo_url:
    print(
        "\nWARNING: No repository_url was set. To set the remote to your repository later, run the following command:\n"
        "git remote add origin PATH_TO_YOUR_REPOSITORY"
    )
