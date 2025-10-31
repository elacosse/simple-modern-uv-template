import sys
from unittest.mock import patch

from changeme.changeme import main


def test_main_with_name(capsys):
    with patch.object(sys, "argv", ["changeme", "--name", "Alice"]):
        main()
        captured = capsys.readouterr()
        assert "Hello, Alice!" in captured.out


def test_main_without_name(capsys):
    with patch.object(sys, "argv", ["changeme"]):
        main()
        captured = capsys.readouterr()
        assert "Hello, World!" in captured.out
