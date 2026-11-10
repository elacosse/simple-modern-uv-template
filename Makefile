# Makefile for easy development workflows.
# The optional CI workflow uses the same checks.

.DEFAULT_GOAL := default

UV_CONFIG_FILE := $(CURDIR)/uv.toml
export UV_CONFIG_FILE

.PHONY: default setup install check lint format test template-test upgrade build clean

PYTHON_PATHS := src tests devtools
DOC_PATHS := README.md AGENTS.md agent-skills.md CHANGELOG.md development.md installation.md publishing.md
YAML_PATHS := .github openspec $(wildcard .copier-answers.yml) .yamllint.yaml

default: check

setup: install
	uv run pre-commit install

install:
	uv sync --all-extras --dev

lint:
	uv run codespell $(PYTHON_PATHS) $(DOC_PATHS)
	uv run ruff check $(PYTHON_PATHS)
	uv run ruff format --check $(PYTHON_PATHS)
	uv check --locked
	uv run yamllint --config-file .yamllint.yaml $(YAML_PATHS)

format:
	uv run codespell --write-changes $(PYTHON_PATHS) $(DOC_PATHS)
	uv run ruff check --fix $(PYTHON_PATHS)
	uv run ruff format $(PYTHON_PATHS)

test:
	uv run pytest

check: lint test

template-test:
	uv run python devtools/template_smoke.py

upgrade:
	uv lock --upgrade
	uv sync

build:
	uv sync --locked --group build
	uv build --no-build-isolation

clean:
	-rm -rf dist/
	-rm -rf *.egg-info/
	-rm -rf .coverage coverage.xml htmlcov/
	-rm -rf .pytest_cache/
	-rm -rf .ruff_cache/
	-rm -rf .venv/
	-find . -type d -name "__pycache__" -exec rm -rf {} +
