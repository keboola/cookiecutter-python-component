run:
	uv sync --frozen
	uv run cookiecutter gh:keboola/cookiecutter-python-component

dev:
	uv sync --frozen
	uv run cookiecutter -v -c ENTER_YOUR_DEV_BRANCH_NAME gh:keboola/cookiecutter-python-component
