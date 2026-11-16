# AGENTS.md — Repository Engineering & No-Slop Protocol

## Core Mandate
Optimize for **human comprehension, minimal diffs, and root-cause fixes**—not lines of code generated. Treat human review attention as the scarcest resource.

## Mechanical Guardrails (Mandatory Before Handoff)
Run these commands and resolve all errors before concluding any task:
- **Full Check (Recommended):** `make check` (runs `codespell`, `ruff`, `uv check --locked`, `yamllint`, and `pytest` with 100% coverage)
- **Format & Lint:** `make format` (or `uv run ruff check --fix src tests devtools && uv run ruff format src tests devtools`)
- **Typecheck:** `uv check --locked` (runs `ty`)
- **Single-File Verification:** `./devtools/verify_file.sh <path>` (or `make verify-file FILE=<path>`)
- **Targeted Tests:** `uv run pytest path/to/test.py`

## Architectural & Anti-Slop Boundaries
- **Subtraction over addition:** Prefer deleting dead code or simplifying existing modules over adding new abstractions, wrapper classes, or helper files.
- **No silent workarounds:** Fix broken upstream logic rather than masking failures with broad `try/except`, fallback defaults, or type suppressions (`# type: ignore`).
- **Explore before writing:** Read existing module patterns and shared utilities before introducing new ones. Zero speculative features.
- **Dependency freeze:** Never add new packages to `pyproject.toml` without explicit human approval. When approved, use `UV_CONFIG_FILE=uv.toml uv add` (or `uv add --dev`) and commit `uv.lock`. Note the 14-day dependency release cooling-off period in `uv.toml`; use an explicit `--exclude-newer` cutoff only for urgent exceptions.
- **Two-strike rule:** If a mistake or lint failure occurs twice, propose a concrete rule addition to this file or a deterministic linter/test guardrail.

## Execution & Handoff Protocol
1. **Plan First (Non-Trivial Tasks):** For multi-file or architectural changes, output a 3–5 bullet plan (what changes, what gets deleted, key trade-offs) and wait for approval before writing code.
2. **Handoff Summary (<= 5 Bullets):**
   - **Intent / Root Cause:** What was actually broken or needed.
   - **Changes:** Exact files modified/deleted and why.
   - **Verification:** Commands run and pass status.
   - **Human Review Focus:** Specific high-stakes logic, edge cases, or assumptions requiring human judgment.

## Project Layout & Template Notes
- Application code lives in `src/changeme`, tests in `tests`, and development utilities in `devtools`.
- Run `make build` to build distributions using the locked build dependencies.
- CI is disabled by default. To enable it, move `.github/ci.yml` into `.github/workflows/`; it is manually triggered until other triggers are added.
- Versions come from Git tags; see `publishing.md` before creating a release.
