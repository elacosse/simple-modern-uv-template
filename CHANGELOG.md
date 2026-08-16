# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- A one-command project configurator.
- Python 3.14 support and a generated-project smoke test.
- Dependabot updates for pinned GitHub Actions.
- Dependency auditing and minimum-version test coverage in CI.
- Pinned build backend dependencies and required uv 0.12.1 or newer.
- An opt-in installer for individually selected Codex and Antigravity agent skills.
- Matt Pocock's individually selectable agent skills in the installer catalog.
- Clearly named opt-in bundles for complete skill collections from each source.
- Claude Code as a default target for selected project-local agent skills.

### Changed

- Split read-only checks from automatic formatting.
- Replaced BasedPyright with Astral's ty type checker and language server.
- Reduced duplicated CI work and isolated PyPI publishing credentials.
- Restricted source distributions to package source and required metadata.
- Made project configuration fail before changing files when template markers are missing.
- Disabled persisted GitHub checkout credentials in CI and release workflows.
