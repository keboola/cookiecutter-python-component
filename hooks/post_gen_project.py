import os
import shutil
import subprocess

KDP_COMPID_PLACEHOLDER = "COOKIECUTTER_DEV_PORTAL_COMPONENT_ID"
KDP_VENDOR_PLACEHOLDER = "COOKIECUTTER_DEV_PORTAL_VENDOR_NAME"


def replace_placeholders_in_file(filepath):
    with open(filepath, "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            output = line
            if KDP_COMPID_PLACEHOLDER in output:
                output = output.replace(KDP_COMPID_PLACEHOLDER, "{{ cookiecutter.dev_portal_component_id }}")
            if KDP_VENDOR_PLACEHOLDER in output:
                output = output.replace(KDP_VENDOR_PLACEHOLDER, "{{ cookiecutter.dev_portal_vendor_name }}")
            f.write(output)
        f.truncate()


PIPELINE_TEMPLATES = {
    "single": "push.yml",
    "matrix": "push.matrix.yml.example",
    "monorepo": "push.monorepo.yml.example",
}


def setup_pipeline_workflow():
    """Install the selected pipeline template as push.yml and remove the rest."""
    workflows_dir = ".github/workflows"
    pipeline_type = "{{ cookiecutter.pipeline_type }}"
    selected = PIPELINE_TEMPLATES[pipeline_type]

    # If not the default, rename the selected template to push.yml
    if selected != "push.yml":
        os.replace(
            os.path.join(workflows_dir, selected),
            os.path.join(workflows_dir, "push.yml"),
        )

    # Remove leftover example files
    for filename in os.listdir(workflows_dir):
        if filename.endswith(".yml.example"):
            os.remove(os.path.join(workflows_dir, filename))


def modify_portal_properties(repo_url):
    setup_pipeline_workflow()

    workflows_dir = ".github/workflows"
    for filename in os.listdir(workflows_dir):
        if filename.endswith(".yml"):
            replace_placeholders_in_file(os.path.join(workflows_dir, filename))

    with open("component_config/sourceCodeUrl.md", "w") as f:
        f.write(repo_url)

    with open("component_config/documentationUrl.md", "w") as f:
        f.write(repo_url + "/blob/master/README.md")

    with open("component_config/licenseUrl.md", "w") as f:
        f.write(repo_url + "/blob/master/LICENSE.md")


repo_url = "{{ cookiecutter.repository_url }}"

modify_portal_properties(repo_url=repo_url)

REMOVE_PATHS = [
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
subprocess.run(["git", "commit", "-m", "initial cookiecutter-template-based commit"])

if not repo_url:
    print(
        "\nWARNING: No repository_url was set. To set the remote to your repository later, run the following command:\n"
        "git remote add origin PATH_TO_YOUR_REPOSITORY"
    )
