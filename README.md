# Keboola Python Component cookiecutter template

Cookiecutter template for Keboola Python component creation. Currently supports Git and Bitbucket CI deployments.

## Prerequisite

Python > 3

[Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html) installed

- installation: `pip install cookiecutter`

## Usage


1. Run `cookiecutter bb:kds_consulting_team/cookiecutter-python-component.git`
2. Fill in requested parameters:
    - `template_variant` - Where is your empty repository (Github, Bitbucket)
    - `repository_url` - (OPT) URL of your repository, if filled in the template git repository is initialised and remote set to your repository.
    - `component_name` - Name of your component
    - `repository_folder_name` - (OPT) Name of the destination folder. By default normalized component name.
    - `component_short_description` - (OPT) short description that will be pushed to Developer Portal. May be edited in `component_config/component_short_description.md` later.
    - `component_long_description` - (OPT) long description that will be pushed to Developer Portal. May be edited in `component_config/component_long_description.md` later.
    - `ci_use_flake8_checks` - if set to `y` flake8 checks will be run on each CI build (push to repository)
    - `ci_push_test_tag_in_branch` - if set to `y` image with tag `test` will be pushed to ECR on every build (push to repository)
3. Set up CI environment variables (see the [CI Setup section](## CI Setup))
4. Navigate to newly created folder and run `git push`. The CI pipeline (action) should be now executed. If you add a tag to the commit, component will be pushed to your Developer Portal.
5. Modify the code in `src/component.py` as you like.
    - You can set the configuration parameters in `data/config.json`
    - You can execute the component via normal local environment without docker installed.
    - Set any additional dependencies for your project in `requirements.txt`
 
 More information on the template [here](https://bitbucket.org/kds_consulting_team/kbc-python-template/src/master/README.md)
   
## CI Setup
 - Bitbucket: Enable [pipelines](https://confluence.atlassian.com/bitbucket/get-started-with-bitbucket-pipelines-792298921.html) in the repository.
    - For Github: Check that the [workflows are enabled](https://docs.github.com/en/actions/managing-workflow-runs/disabling-and-enabling-a-workflow).
    The actions are present in `.github/workflows/` folder. 
 - Set `KBC_DEVELOPERPORTAL_APP` env variable (dev portal app id)
 
 In case it is not set on the account level, set also other required dev portal env variables:
 
 - `KBC_DEVELOPERPORTAL_PASSWORD` - service account password
 - `KBC_DEVELOPERPORTAL_USERNAME` - service account username
 - `KBC_DEVELOPERPORTAL_VENDOR` - dev portal vendor
 - `KBC_STORAGE_TOKEN` - (optional) in case you wish to run KBC automated tests
  
 
 ![picture](docs/imgs/ci_variable.png)
  
    
 