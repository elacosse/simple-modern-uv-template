# Optional AI Agent Skills

## OpenSpec

[OpenSpec](https://openspec.dev/) helps plan and track changes with specifications.
This template includes the core workflow for Codex and Claude Code. After creating
a project, [install the CLI](https://openspec.dev/docs/installation) to use it.
To initialize or refresh integrations for the assistants you use, run:

```shell
openspec init --tools codex,claude --profile core
```

Commit the generated `openspec/` directory and agent files alongside your project.
In Codex, invoke `$openspec-propose` with your idea; in Claude Code, use
`/opsx:propose`. Use OpenSpec for changes that benefit from a written plan.
See the [quickstart](https://openspec.dev/docs/quickstart) for the full workflow.
After upgrading the CLI, preview generated-file changes with `openspec update --dry-run`.

Keep shared project instructions in `AGENTS.md`; a separate `CLAUDE.md` is not
needed when Claude Code is configured to read `AGENTS.md`.

## Other skills

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
