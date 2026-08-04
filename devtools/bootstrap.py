"""Configure a repository created from this GitHub template."""

from __future__ import annotations

import argparse
import keyword
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

PLACEHOLDER = "change" + "me"
TEMPLATE_START = "<!-- template-setup:start -->"
TEMPLATE_END = "<!-- template-setup:end -->"


@dataclass(frozen=True)
class ProjectConfig:
    project_name: str
    package_module: str
    github_org: str
    author_name: str
    author_email: str
    description: str
    copyright_year: int


def _replace(path: Path, replacements: list[tuple[str, str]]) -> None:
    content = path.read_text()
    for old, new in replacements:
        if old not in content:
            raise ValueError(f"Expected template marker {old!r} in {path}")
        content = content.replace(old, new)
    path.write_text(content)


def _remove_template_setup(readme: Path) -> None:
    content = readme.read_text()
    start = content.find(TEMPLATE_START)
    end = content.find(TEMPLATE_END)
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"Template setup markers are missing or invalid in {readme}")
    readme.write_text(content[:start] + content[end + len(TEMPLATE_END) :].lstrip("\n"))


def _require_markers(path: Path, markers: tuple[str, ...]) -> None:
    content = path.read_text()
    for marker in markers:
        if marker not in content:
            raise ValueError(f"Expected template marker {marker!r} in {path}")


def _validate(config: ProjectConfig) -> None:
    if re.fullmatch(r"[a-z0-9]+(?:[-_.][a-z0-9]+)*", config.project_name) is None:
        raise ValueError("Project name must be a normalized lowercase package name")
    if (
        not config.package_module.isidentifier()
        or not config.package_module.isascii()
        or keyword.iskeyword(config.package_module)
    ):
        raise ValueError("Package module must be an ASCII Python identifier")
    if re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", config.github_org) is None:
        raise ValueError("GitHub owner must contain only letters, numbers, or internal hyphens")
    if "@" not in config.author_email:
        raise ValueError("Author email must look like an email address")
    for label, value in (
        ("Author name", config.author_name),
        ("Author email", config.author_email),
        ("Description", config.description),
    ):
        if "\n" in value or "\r" in value:
            raise ValueError(f"{label} must be a single line")
    if not 1900 <= config.copyright_year <= 9999:
        raise ValueError("Copyright year must have four digits")


def configure_project(root: Path, config: ProjectConfig, *, update_lock: bool = True) -> None:
    """Apply project metadata and package names to a fresh template copy."""
    root = root.resolve()
    _validate(config)
    source_package = root / "src" / PLACEHOLDER
    target_package = root / "src" / config.package_module
    if not source_package.is_dir():
        raise ValueError(f"Expected an unconfigured template at {source_package}")
    if target_package.exists() and target_package != source_package:
        raise ValueError(f"Target package already exists: {target_package}")

    # Verify the complete template before changing anything, so a locally edited or
    # incomplete template fails safely instead of being only partly configured.
    _require_markers(
        root / "pyproject.toml",
        (
            f"https://github.com/{PLACEHOLDER}/{PLACEHOLDER}",
            f'name = "{PLACEHOLDER}"',
            f'description = "{PLACEHOLDER}"',
            f'{{ name="{PLACEHOLDER}", email="{PLACEHOLDER}@example.com" }}',
            f'{PLACEHOLDER} = "{PLACEHOLDER}:cli"',
            f'packages = ["src/{PLACEHOLDER}"]',
            f"--cov={PLACEHOLDER}",
        ),
    )
    _require_markers(
        root / "README.md",
        (f"{PLACEHOLDER}/{PLACEHOLDER}", PLACEHOLDER, TEMPLATE_START, TEMPLATE_END),
    )
    _require_markers(root / "development.md", (f"{PLACEHOLDER}/{PLACEHOLDER}",))
    _require_markers(root / "LICENSE", (f"Copyright (c) 2026 {PLACEHOLDER}",))
    _require_markers(
        root / "tests" / f"test_{PLACEHOLDER}.py",
        (
            f"from {PLACEHOLDER}.{PLACEHOLDER} import",
            f'patch("{PLACEHOLDER}.{PLACEHOLDER}.load_dotenv")',
            f'["{PLACEHOLDER}",',
        ),
    )
    _require_markers(root / "src" / PLACEHOLDER / "__init__.py", (f"from .{PLACEHOLDER} import",))
    _require_markers(root / ".github" / "workflows" / "publish.yml", (f"https://pypi.org/p/{PLACEHOLDER}",))
    _require_markers(
        root / ".github" / "workflows" / "ci.yml",
        (
            "name: Quality and template smoke test",
            "\n      - name: Smoke-test a configured project\n        run: make template-test\n",
        ),
    )
    _require_markers(
        root / "Makefile",
        (" test template-test upgrade", "\ntemplate-test:\n\tuv run python devtools/template_smoke.py\n"),
    )

    toml_author = config.author_name.replace("\\", "\\\\").replace('"', '\\"')
    toml_email = config.author_email.replace("\\", "\\\\").replace('"', '\\"')
    toml_description = config.description.replace("\\", "\\\\").replace('"', '\\"')

    _replace(
        root / "pyproject.toml",
        [
            (
                f"https://github.com/{PLACEHOLDER}/{PLACEHOLDER}",
                f"https://github.com/{config.github_org}/{config.project_name}",
            ),
            (f'name = "{PLACEHOLDER}"', f'name = "{config.project_name}"'),
            (f'description = "{PLACEHOLDER}"', f'description = "{toml_description}"'),
            (
                f'{{ name="{PLACEHOLDER}", email="{PLACEHOLDER}@example.com" }}',
                f'{{ name="{toml_author}", email="{toml_email}" }}',
            ),
            (f'{PLACEHOLDER} = "{PLACEHOLDER}:cli"', f'{config.project_name} = "{config.package_module}:cli"'),
            (f'packages = ["src/{PLACEHOLDER}"]', f'packages = ["src/{config.package_module}"]'),
            (f"--cov={PLACEHOLDER}", f"--cov={config.package_module}"),
        ],
    )
    _replace(
        root / "README.md",
        [
            (f"{PLACEHOLDER}/{PLACEHOLDER}", f"{config.github_org}/{config.project_name}"),
            (PLACEHOLDER, config.project_name),
        ],
    )
    _remove_template_setup(root / "README.md")
    (root / "CHANGELOG.md").write_text(
        """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
"""
    )
    _replace(
        root / "development.md",
        [(f"{PLACEHOLDER}/{PLACEHOLDER}", f"{config.github_org}/{config.project_name}")],
    )
    _replace(
        root / "LICENSE",
        [(f"Copyright (c) 2026 {PLACEHOLDER}", f"Copyright (c) {config.copyright_year} {config.author_name}")],
    )
    _replace(
        root / "tests" / f"test_{PLACEHOLDER}.py",
        [
            (f"from {PLACEHOLDER}.{PLACEHOLDER} import", f"from {config.package_module}.cli import"),
            (f'patch("{PLACEHOLDER}.{PLACEHOLDER}.load_dotenv")', f'patch("{config.package_module}.cli.load_dotenv")'),
            (f'["{PLACEHOLDER}",', f'["{config.project_name}",'),
        ],
    )
    _replace(
        root / "src" / PLACEHOLDER / "__init__.py",
        [(f"from .{PLACEHOLDER} import", "from .cli import")],
    )
    _replace(
        root / ".github" / "workflows" / "publish.yml",
        [(f"https://pypi.org/p/{PLACEHOLDER}", f"https://pypi.org/p/{config.project_name}")],
    )
    _replace(
        root / ".github" / "workflows" / "ci.yml",
        [
            ("name: Quality and template smoke test", "name: Quality checks"),
            ("\n      - name: Smoke-test a configured project\n        run: make template-test\n", ""),
        ],
    )
    _replace(
        root / "Makefile",
        [
            (" test template-test upgrade", " test upgrade"),
            ("\ntemplate-test:\n\tuv run python devtools/template_smoke.py\n", ""),
        ],
    )

    source_package.rename(target_package)
    (target_package / f"{PLACEHOLDER}.py").rename(target_package / "cli.py")
    (root / "tests" / f"test_{PLACEHOLDER}.py").rename(root / "tests" / f"test_{config.package_module}.py")

    for template_file in (
        root / ".copier-answers.yml",
        root / "devtools" / "bootstrap.py",
        root / "devtools" / "template_smoke.py",
        root / "tests" / "test_bootstrap.py",
    ):
        template_file.unlink(missing_ok=True)

    if update_lock:
        subprocess.run(["uv", "lock"], cwd=root, check=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-name", required=True, help="Published project and CLI name, such as acme-tool")
    parser.add_argument("--package-module", help="Python import name; defaults to project name with hyphens replaced")
    parser.add_argument("--github-org", required=True, help="GitHub user or organization")
    parser.add_argument("--author-name", help="Package author; defaults to the GitHub owner")
    parser.add_argument("--author-email", required=True)
    parser.add_argument("--description", help="One-line package description; defaults to the project name")
    parser.add_argument("--copyright-year", type=int, default=datetime.now(UTC).year)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help=argparse.SUPPRESS)
    parser.add_argument("--no-lock", action="store_true", help=argparse.SUPPRESS)
    return parser


def main() -> None:
    args = _parser().parse_args()
    module = args.package_module or args.project_name.replace("-", "_").replace(".", "_")
    config = ProjectConfig(
        project_name=args.project_name,
        package_module=module,
        github_org=args.github_org,
        author_name=args.author_name or args.github_org,
        author_email=args.author_email,
        description=args.description or args.project_name,
        copyright_year=args.copyright_year,
    )
    configure_project(args.root, config, update_lock=not args.no_lock)
    print(f"Configured {config.project_name} with package {config.package_module}.")


if __name__ == "__main__":
    main()
