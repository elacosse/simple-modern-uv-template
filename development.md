# Development

## Setting Up uv

This project is set up to use [uv](https://docs.astral.sh/uv/) to manage Python and
dependencies. First, be sure you
[have uv installed](https://docs.astral.sh/uv/getting-started/installation/).

Then [fork the changeme/changeme
repo](https://github.com/changeme/changeme/fork) (having your own
fork will make it easier to contribute) and
[clone it](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## Basic Developer Workflows

The `Makefile` offers shortcuts to `uv` commands for developer convenience. CI is
disabled by default. To enable the provided CI workflow, move `.github/ci.yml` to
`.github/workflows/ci.yml`. It can then be started manually from the GitHub Actions
tab; add push and pull request triggers if automatic runs are desired. Publishing a
GitHub release independently starts the release workflow.

```shell
# First, install all dependencies and set up your virtual environment.
# This simply runs `uv sync --all-extras --dev` to install all packages,
# including dev dependencies and optional dependencies.
make install

# Install dependencies and Git hooks on a new checkout:
make setup

# Run all read-only checks and tests:
make check

# Build a wheel and source distribution with locked build dependencies:
make build

# Read-only linting, formatting, spelling, typing, and YAML checks:
make lint

# Apply safe automatic fixes and formatting:
make format

# Run tests:
make test

# Delete all the build artifacts:
make clean

# Upgrade and install dependencies:
make upgrade

# To run tests by hand:
uv run pytest   # all tests
uv run pytest --no-cov tests/ -k test_name  # focused tests without the full-suite coverage threshold

# Build and install current dev executables, to let you use your dev copies
# as local tools:
uv tool install --editable .

# Dependency management directly with uv:
# Add a new dependency:
uv add package_name
# Add a development dependency:
uv add --dev package_name
# Update to latest compatible versions (including dependencies on git repos):
uv sync --upgrade
# Update a specific package:
uv lock --upgrade-package package_name
# Update dependencies on a package:
uv add package_name@latest

# Run a shell within the Python environment:
uv venv
source .venv/bin/activate
```

See [uv docs](https://docs.astral.sh/uv/) for details.

The checked-in `uv.toml` sets a 14-day cooling-off period for dependency resolution.
The Makefile uses this configuration explicitly; for direct commands, set
`UV_CONFIG_FILE=uv.toml` to prevent user-level uv settings from being merged. To
resolve an urgent update, override the period for that command with
`--exclude-newer` and an explicit cutoff timestamp. Lockfile changes should be
reviewed and committed. Building uses the locked `build` dependency group with
build isolation disabled so the installed backend dependencies match the lockfile.

## Pre-commit Hooks

`make setup` installs the pre-commit hooks. To install only the hooks, run:

```shell
uv run pre-commit install
```

Now, the hooks will run automatically every time you make a commit. You can also run them manually:

```shell
uv run pre-commit run --all-files
```

## IDE setup

If you use VSCode or a fork like Cursor or Windsurf, you can install the following
extensions:

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

- [ty](https://marketplace.visualstudio.com/items?itemName=astral-sh.ty) for fast type
  checking and Python language-server features. The extension disables the Python
  extension's language server by default to avoid running two language servers.

## Documentation

- [uv docs](https://docs.astral.sh/uv/)

- [ty docs](https://docs.astral.sh/ty/)

* * *

*This file was built with
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
