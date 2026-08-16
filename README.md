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

## Optional AI Agent Skills

Install only the skills you want for this repository. The curated catalog includes
[Blueprint](https://github.com/imbue-ai/blueprint) and [Addy Osmani's agent
skills](https://github.com/addyosmani/agent-skills), plus [Matt Pocock's
skills](https://github.com/mattpocock/skills). List the exact available names:

```shell
uv run python devtools/install_agent_skills.py --list
```

You can also install a complete collection when it fits the project:

```shell
# Guided planning and plan generation (2 skills)
uv run python devtools/install_agent_skills.py --bundle planning-with-blueprint

# Addy's engineering-oriented collection (24 skills)
uv run python devtools/install_agent_skills.py --bundle addy-engineering-skills

# Matt Pocock's development workflow collection (41 skills)
uv run python devtools/install_agent_skills.py --bundle mattpocock-workflows
```

`--bundle all` installs all 67 skills and requires `--yes` as an explicit
confirmation. Use `--dry-run` first if you want to inspect the commands.

### Choosing Skills

The catalog has 67 individually selectable skills. Start with the workflow you
actually want; do not install several skills that solve the same problem just
because they are available.

| If you want to… | Consider these skills |
| --- | --- |
| Turn a vague idea into a plan | `blueprint` (guided questions), `blueprint-generate` (write the plan), `interview-me`, `idea-refine`, `spec-driven-development`, `grill-me`, `to-spec`, `to-tickets`, `wayfinder` |
| Design boundaries, APIs, and domain language | `api-and-interface-design`, `codebase-design`, `design-an-interface`, `domain-modeling`, `ubiquitous-language` |
| Implement carefully | `incremental-implementation`, `test-driven-development`, `source-driven-development`, `doubt-driven-development`, `implement`, `tdd` |
| Debug, research, or prototype | `debugging-and-error-recovery`, `diagnosing-bugs`, `research`, `prototype`, `browser-testing-with-devtools` |
| Review and improve code | `code-review-and-quality`, `code-review`, `code-simplification`, `security-and-hardening`, `performance-optimization` |
| Build UI or production visibility | `frontend-ui-engineering`, `observability-and-instrumentation` |
| Ship and maintain software | `git-workflow-and-versioning`, `ci-cd-and-automation`, `documentation-and-adrs`, `shipping-and-launch`, `deprecation-and-migration`, `triage` |

Some choices intentionally overlap: choose either `test-driven-development` or
`tdd` as your default testing workflow, and either `code-review-and-quality` or
`code-review` as your default review workflow. Install both only if you want to
compare their approaches. `browser-testing-with-devtools` additionally requires
the Chrome DevTools MCP server.

Then install specific skills into this repository. For example:

```shell
uv run python devtools/install_agent_skills.py \
  blueprint \
  api-and-interface-design \
  test-driven-development
```

Pass `--dry-run` to preview commands or `--remove` to remove selected skills or
bundles. By default, the installer copies selected skills for both Codex
(`.agents/skills/`) and Claude Code (`.claude/skills/`). Use `--agent codex` or
`--agent claude-code` to target just one. It disables anonymous installer telemetry
and never installs skills unless you name them. Antigravity CLI (`agy`) also discovers
the shared `.agents/skills/` directory.

## Project Docs

For how to install uv and Python, see [installation.md](installation.md).

For development workflows, see [development.md](development.md).

For instructions on publishing to PyPI, see [publishing.md](publishing.md).

* * *

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
