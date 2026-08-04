"""Render and verify a disposable project made from this template."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_NAMES = {
    ".claude",
    ".coverage",
    ".DS_Store",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "coverage.xml",
    "dist",
    "__pycache__",
}


def _ignore(_directory: str, names: list[str]) -> set[str]:
    return IGNORED_NAMES.intersection(names)


def _run(command: list[str], cwd: Path) -> None:
    environment = os.environ.copy()
    environment.pop("VIRTUAL_ENV", None)
    subprocess.run(command, cwd=cwd, check=True, env=environment)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="modern-uv-template-") as temporary_directory:
        project = Path(temporary_directory) / "sample-project"
        shutil.copytree(ROOT, project, ignore=_ignore)
        _run(
            [
                sys.executable,
                "devtools/bootstrap.py",
                "--project-name",
                "sample-project",
                "--github-org",
                "sample-org",
                "--author-name",
                "Sample Author",
                "--author-email",
                "author@example.com",
                "--description",
                "Generated project smoke test",
            ],
            project,
        )
        _run(["uv", "sync", "--locked"], project)
        _run(["make", "lint"], project)
        _run(["uv", "run", "pytest"], project)
        _run(["uv", "run", "sample-project", "--name", "Template"], project)

        output = project / "build-output"
        _run(["uv", "build", "--out-dir", str(output)], project)
        source_distribution = next(output.glob("*.tar.gz"))
        with tarfile.open(source_distribution, "r:gz") as archive:
            members = archive.getnames()
        forbidden = ("/.claude/", "/.github/", "/devtools/")
        unexpected = [member for member in members if any(part in member for part in forbidden)]
        if unexpected:
            raise RuntimeError(f"Unexpected files in source distribution: {unexpected}")

        if (project / "src" / "changeme").exists():
            raise RuntimeError("Placeholder package was not renamed")
        if not (project / "src" / "sample_project").is_dir():
            raise RuntimeError("Configured package is missing")
        if (project / ".copier-answers.yml").exists():
            raise RuntimeError("Upstream template state was retained")
        if (project / "devtools" / "bootstrap.py").exists():
            raise RuntimeError("Template configurator was retained")

    print("Template smoke test passed.")


if __name__ == "__main__":
    main()
