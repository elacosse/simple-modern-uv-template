# Project instructions for coding agents

This is a Python project managed with uv. Application code lives in `src/changeme`,
tests in `tests`, and development utilities in `devtools`.

- Run `make check` for lint, formatting, spelling, type, YAML, and test checks.
- Run `make build` to build distributions using the locked build dependencies.
- Use `uv add` and `uv add --dev` to manage dependencies and commit `uv.lock`.
  Use `UV_CONFIG_FILE=uv.toml` for direct uv commands to avoid user-level settings.
- Project uv settings include a 14-day dependency release cooling-off period. When an
  urgent update needs an exception, use an explicit `--exclude-newer` cutoff.
- CI is disabled by default. To enable it, move `.github/ci.yml` into
  `.github/workflows/`; it is manually triggered until other triggers are added.
- Versions come from Git tags; see `publishing.md` before creating a release.
