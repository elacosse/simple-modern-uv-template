# changeme

<!-- template-setup:start -->
## Start a New Project

Create a repository from this GitHub template, clone it, install
[uv](https://docs.astral.sh/uv/getting-started/installation/), and run:

```shell
uv run python devtools/bootstrap.py \
  --project-name my-project \
  --github-org my-github-name \
  --author-name "My Name" \
  --author-email me@example.com \
  --description "What this project does"
```

The command renames the package, updates project metadata and documentation, and refreshes
`uv.lock`.

Then run `make setup` to install dependencies and Git hooks, followed by `make check`.
<!-- template-setup:end -->

[![CI](https://github.com/changeme/changeme/actions/workflows/ci.yml/badge.svg)](https://github.com/changeme/changeme/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/changeme.svg)](https://pypi.org/project/changeme/)
[![Codecov](https://codecov.io/gh/changeme/changeme/branch/main/graph/badge.svg)](https://codecov.io/gh/changeme/changeme)

A modern Python project template with `uv`, `pre-commit`, and `pytest`.

## Installation

To install the package, run:

```shell
pip install changeme
```

## Usage

To use the CLI, run:

```shell
changeme --name "Your Name"
```

This will output:

```
Hello, Your Name!
```

## Project Docs

For how to install uv and Python, see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

For instructions on publishing to PyPI, see [publishing.md](publishing.md).

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
