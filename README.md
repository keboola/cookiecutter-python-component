- [Keboola Python Component Cookiecutter Template](#keboola-python-component-cookiecutter-template)
  - [Running](#running)
    - [Direcly using cookiecutter 🍪](#direcly-using-cookiecutter-)
    - [With cloning the repository 🐑](#with-cloning-the-repository-)
  - [Usage](#usage)
  - [CI Setup](#ci-setup)

# Keboola Python Component Cookiecutter Template

Cookiecutter template for Keboola Python component creation. Currently supports Git and Bitbucket CI deployments.

## Running

You can use this template with just the [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html) installed or you can clone this whole repository to your drive so uv can handle cookiecutter installation for you.

### Direcly using cookiecutter 🍪

1. Prerequisite: [Install cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html#installation)
1. Run `cookiecutter gh:keboola/cookiecutter-python-component`

### With cloning the repository 🐑

1. Prerequisite: [Install uv 💜](https://docs.astral.sh/uv/#installation)
1. Clone the repository
1. Run `make run` (which will install cookiecutter in a venv and run it just like above)

## Usage

1. Enter the desired parameters (those marked with ❗ are mandatory):
   - ❗ `template_variant` – Where is your empty repository (GitHub, Bitbucket)
   - `repository_url` – URL of your repository, if filled in the template git repository is initialised and remote set to your repository.
   - ❗ `component_name` – Name of your component
   - `dev_portal_vendor_name` – Vendor name for publishing on Keboola Developer Portal. Default value is `keboola`.
   - `dev_portal_component_id` – Component ID for publishing on Keboola Developer Portal. Defaults to normalized component name.
   - `repository_folder_name` – Name of the destination folder. Defaults to prefixed & normalized component name.
   - `component_short_description` – Short description that will be pushed to Developer Portal. May be edited in `component_config/component_short_description.md` later.
   - `component_long_description` – Long description that will be pushed to Developer Portal. May be edited in `component_config/component_long_description.md` later.
1. Set up CI environment variables (see the [CI Setup section](#ci-setup))
1. Navigate to newly created folder and run `git push`. The CI pipeline (action) should be now executed. If you add a tag to the commit, component will be pushed to your Developer Portal.
1. Modify the code in `src/component.py` as you like.
   - You can set the configuration parameters in `data/config.json`
   - You can execute the component via normal local environment without docker installed.
   - Set any additional dependencies for your project in `requirements.txt`

More information on the template [here](https://bitbucket.org/kds_consulting_team/kbc-python-template/src/master/README.md)

## CI Setup

- Bitbucket: Enable [pipelines](https://confluence.atlassian.com/bitbucket/get-started-with-bitbucket-pipelines-792298921.html) in the repository.
 - For GitHub: Check that the [workflows are enabled](https://docs.github.com/en/actions/managing-workflow-runs/disabling-and-enabling-a-workflow).
   The actions are present in `.github/workflows/` folder.
- Set `KBC_DEVELOPERPORTAL_APP` env variable (dev portal app id)

In case it is not set on the account level, set also other required dev portal env variables:

- `KBC_DEVELOPERPORTAL_PASSWORD – service account password
- `KBC_DEVELOPERPORTAL_USERNAME – service account username
- `KBC_DEVELOPERPORTAL_VENDOR – dev portal vendor
- `KBC_STORAGE_TOKEN – (optional) in case you wish to run KBC automated tests

![picture](docs/imgs/ci_variable.png)
