# Repository Guidelines

## Project Structure & Module Organization

```
/ (project root)
├── AGENTS.md
├── Dockerfile -- do not change unless absolutelly necessary
├── LICENSE.md -- do not change
├── README.md
├── component_config/
│   ├── component_long_description.md -- detailed description of the component for the Keboola Developer Portal
│   ├── component_short_description.md -- short description of the service the component integrates with
│   ├── configRowSchema.json -- JSON schema for individual configuration rows (if applicable)
│   ├── configSchema.json -- JSON schema for the overall configuration
│   ├── configuration_description.md -- do not touch
│   ├── documentationUrl.md
│   ├── licenseUrl.md -- do not change
│   ├── logger -- do not touch
│   ├── loggerConfiguration.json -- do not touch
├── data/ -- mounted as KBC_DATADIR in the container, holds user configuration and I/O
│   ├── config.json -- conatins user parameters
│   ├── in/
│   │   ├── state.json -- optional state file to persist data between runs (from previous run)
│   │   └── tables/ -- input tables go here
│   └── out/
│       ├── files/ -- output files go here
│       ├── state.json -- optional state file to persist data between runs
│       └── tables/ -- output tables go here
├── deploy.sh
├── docker-compose.yml
├── flake8.cfg
├── pyproject.toml
├── scripts/ -- utility scripts
├── src/
│   ├── component.py -- main component logic, should contain run function and any sync actions
│   ├── configuration.py -- configuration validation and helper functions
│   ├── + Usually a client file and/or utils.py for helper functions
├── tests -- unit tests
```

The component code lives in `src/`, with `component.py` as the main entrypoint. Maintain best practices by isolating configuration logic in `configuration.py` 
and encapsulating API interactions within a dedicated client module. Use `utils.py` for shared helper functions.

## Build, Test, and Development Commands

Bootstrap the container toolchain with `docker-compose build`, then launch an interactive development shell via
`docker-compose run --rm dev` (mounts the repo and `data/` folder). Run the full lint-and-test check with
`docker-compose run --rm test`, which executes `/code/scripts/build_n_test.sh`. For quick local cycles you can call
`flake8 --config=flake8.cfg` and `python -m unittest discover` directly; both assume Python 3.13 per the `Dockerfile`.

## Coding Style & Naming Conventions

Follow PEP 8 with four-space indentation and keep lines ≤120 characters (enforced by `flake8`). The `flake8` profile
ignores `E203` and `W503` to align with Black-style slicing; respect that when formatting diffs. Ruff is installed for
supplemental linting—run it before opening a PR if you touch validation logic. Modules and functions stay snake_case,
classes use PascalCase, and environment variables remain upper snake to match existing usage (`KBC_DATADIR`).

- avoid using nested functions unless necessary
- Prefer initializing configuration as a class parameter of the main component class instead of passing it around
- Avoid deep nesting of code blocks (e.g. if statements, loops); extract to helper functions instead

## Testing Guidelines

Unit tests use the standard library’s `unittest` runner alongside `freezegun` and `mock` for deterministic behavior.
Name files `test_*.py` and match fixture structure to `src/` modules. Prefer fast, isolated tests that exercise the
Keboola interface contract—freeze time when asserting manifest timestamps. Run `python -m unittest tests.test_component`
for focused checks, and always finish with the docker-compose test target before requesting review.

## Commit & Pull Request Guidelines

Keep commits concise and purposeful; Pull requests should list test evidence (
`docker-compose run --rm test` output), link related Keboola tasks, and include screenshots or sample manifests when UI
or schema changes are involved.

## Environment & Deployment Tips

Configuration values may include secrets such as `#api_token`; rely on Keboola parameters rather than committing them.
When iterating locally, adjust the `docker-compose.yml` volume mapping to point `./data` at a safe scratch directory.


# Component Development Guidelines

## User configuration

Component configuration is stored in `data/config.json` file. User parameters live in `parameters` section of the configuration file.

Create appropriate configuration schema in `component_config/configSchema.json` file. 

If you decide the component should multiple configuration rows, create also `component_config/configRowSchema.json` file. During execution, each configuration row is processed separately in a loop. 
During runtime the component receives both configSchema and configRowSchema merged into a single "parameters" section of the configuration file.

## Configuration schema elements

Use JSON schema elements to define the configuration schema Keboola UI provides a special syntax for some of them, refer to @docs/JSON_SCHEMA_UI_ELEMENTS.md for details.

When creating sync actions always use the supported elements only as described in @docs/JSON_SCHEMA_SUPPORTED_ELEMENTS.md in the `Json Schema UI elements with Sync Actions` section.

Note that the supported sync actions need to be defined in code using the appropriate annotation (see @docs/CODE_EXAMPLES.md) + their names must be listed in the @component_config/actions.json file (which is an array of strings).

Use standard config blocks as suggested in @docs/json_schema_blocks.json to cover common use cases.

## Code examples

You work with https://github.com/keboola/python-component library to interact with the Keboola platform. 

Here @docs/CODE_EXAMPLES.md are code examples for the most common tasks. Note that since you are using ComponentBase examples that show CommonInterface are for reference only, you should use ComponentBase class which inherits from CommonInterface. So instead of ci.xxx use self.xxx in your component class that inherits from ComponentBase.
