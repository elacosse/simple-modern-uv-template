import sys
from unittest.mock import patch

import pytest

from changeme.changeme import cli, main


def test_main_with_name(capsys: pytest.CaptureFixture[str]) -> None:
    main(name="Alice")
    captured = capsys.readouterr()
    assert "Hello, Alice!" in captured.out


def test_main_without_name(capsys: pytest.CaptureFixture[str]) -> None:
    main()
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out


def test_cli_with_name(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(sys, "argv", ["changeme", "--name", "Alice"]):
        with pytest.raises(SystemExit) as exc_info:
            cli()
    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert "Hello, Alice!" in captured.out
