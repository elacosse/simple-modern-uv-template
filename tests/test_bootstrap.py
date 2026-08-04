from pathlib import Path

import pytest

from devtools.bootstrap import ProjectConfig, configure_project


def _write_template(root: Path) -> None:
    placeholder = "changeme"
    files = {
        "pyproject.toml": f'''Repository = "https://github.com/{placeholder}/{placeholder}"
name = "{placeholder}"
description = "{placeholder}"
authors = [{{ name="{placeholder}", email="{placeholder}@example.com" }}]
{placeholder} = "{placeholder}:cli"
packages = ["src/{placeholder}"]
addopts = "--cov={placeholder}"
''',
        "README.md": f"""# {placeholder}
<!-- template-setup:start -->
setup instructions
<!-- template-setup:end -->
https://github.com/{placeholder}/{placeholder}
pip install {placeholder}
""",
        "development.md": f"https://github.com/{placeholder}/{placeholder}",
        "CHANGELOG.md": "template history",
        "LICENSE": f"Copyright (c) 2026 {placeholder}",
        ".copier-answers.yml": f"""package_author_email: {placeholder}@example.com
package_author_name: {placeholder}
package_description: {placeholder}
package_github_org: {placeholder}
package_module: {placeholder}
package_name: {placeholder}
""",
        f"tests/test_{placeholder}.py": f'''from {placeholder}.{placeholder} import cli
patch("{placeholder}.{placeholder}.load_dotenv")
argv = ["{placeholder}", "--help"]
''',
        ".github/workflows/publish.yml": f"https://pypi.org/p/{placeholder}",
        ".github/workflows/ci.yml": """name: Quality and template smoke test

      - name: Smoke-test a configured project
        run: make template-test
""",
        "Makefile": """.PHONY: default setup install check lint format test template-test upgrade build clean

template-test:
	uv run python devtools/template_smoke.py
""",
        f"src/{placeholder}/__init__.py": f"from .{placeholder} import cli, main",
        f"src/{placeholder}/{placeholder}.py": "def cli(): pass\n",
        "devtools/bootstrap.py": "template utility",
        "devtools/template_smoke.py": "template smoke test",
    }
    for relative_path, content in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def test_configure_project(tmp_path: Path) -> None:
    _write_template(tmp_path)
    config = ProjectConfig(
        project_name="acme-tool",
        package_module="acme_tool",
        github_org="acme",
        author_name="Ada Example",
        author_email="ada@example.com",
        description="An example tool",
        copyright_year=2030,
    )

    configure_project(tmp_path, config, update_lock=False)

    assert (tmp_path / "src/acme_tool").is_dir()
    assert (tmp_path / "src/acme_tool/cli.py").is_file()
    assert not (tmp_path / "src/changeme").exists()
    assert (tmp_path / "tests/test_acme_tool.py").is_file()
    assert 'name = "acme-tool"' in (tmp_path / "pyproject.toml").read_text()
    assert "--cov=acme_tool" in (tmp_path / "pyproject.toml").read_text()
    assert "template-setup" not in (tmp_path / "README.md").read_text()
    assert "template history" not in (tmp_path / "CHANGELOG.md").read_text()
    assert not (tmp_path / ".copier-answers.yml").exists()
    assert not (tmp_path / "devtools/bootstrap.py").exists()
    assert "template-test" not in (tmp_path / "Makefile").read_text()


def test_configure_project_rejects_invalid_module(tmp_path: Path) -> None:
    _write_template(tmp_path)
    config = ProjectConfig(
        project_name="acme-tool",
        package_module="not-valid",
        github_org="acme",
        author_name="Ada Example",
        author_email="ada@example.com",
        description="An example tool",
        copyright_year=2030,
    )

    with pytest.raises(ValueError, match="Python identifier"):
        configure_project(tmp_path, config, update_lock=False)


def test_configure_project_preflights_before_writing(tmp_path: Path) -> None:
    _write_template(tmp_path)
    (tmp_path / "Makefile").write_text(".PHONY: default\n")
    config = ProjectConfig(
        project_name="acme-tool",
        package_module="acme_tool",
        github_org="acme",
        author_name="Ada Example",
        author_email="ada@example.com",
        description="An example tool",
        copyright_year=2030,
    )

    with pytest.raises(ValueError, match="template marker"):
        configure_project(tmp_path, config, update_lock=False)

    assert (tmp_path / "src/changeme").is_dir()
    assert 'name = "changeme"' in (tmp_path / "pyproject.toml").read_text()
