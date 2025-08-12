# Keboola Python Component cookiecutter template

Cookiecutter template for Keboola Python component creation. Currently supports Git and Bitbucket CI deployments.

## Prerequisite

- [uv 💜](https://docs.astral.sh/uv/#installation)

## Usage

1. `make run`
2. Enter the desired parameters (those marked with ❗ are mandatory):
   - ❗ `template_variant – Where is your empty repository (GitHub, Bitbucket)
   - `repository_url – URL of your repository, if filled in the template git repository is initialised and remote set to your repository.
   - ❗ `component_name – Name of your component
   - `dev_portal_vendor_name – Vendor name for publishing on Keboola Developer Portal. Default value is `keboola`.
   - `dev_portal_component_id` – Component ID for publishing on Keboola Developer Portal. Defaults to normalized component name.
   - `repository_folder_name – Name of the destination folder. Defaults to prefixed & normalized component name.
   - `component_short_description – Short description that will be pushed to Developer Portal. May be edited in `component_config/component_short_description.md` later.
   - `component_long_description – Long description that will be pushed to Developer Portal. May be edited in `component_config/component_long_description.md` later.
3. Set up CI environment variables (see the [CI Setup section](#ci-setup))
4. Navigate to newly created folder and run `git push`. The CI pipeline (action) should be now executed. If you add a tag to the commit, component will be pushed to your Developer Portal.
5. Modify the code in `src/component.py` as you like.
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
