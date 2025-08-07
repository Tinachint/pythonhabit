import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from habit.cli import parse_args, main

# -------- Fixtures --------

@pytest.fixture(autouse=True)
def mock_app_controller():
    """
    Automatically patch AppController for all tests to isolate CLI logic
    from actual application behavior.
    """
    with patch("habit.cli.AppController") as MockController:
        yield MockController

# -------- Argument Parser Tests --------

def test_parse_args_with_all_options():
    """
    Test that all CLI arguments are parsed correctly when provided.
    """
    test_args = [
        "cli.py",
        "--command", "add",
        "--habit", "Read",
        "--periodicity", "daily",
        "--version",
        "--dry-run"
    ]
    with patch.object(sys, 'argv', test_args):
        args = parse_args()
        assert args.command == "add"
        assert args.habit == "Read"
        assert args.periodicity == "daily"
        assert args.version is True
        assert args.dry_run is True

def test_parse_args_defaults():
    """
    Test that default values are set when no arguments are provided.
    """
    with patch.object(sys, 'argv', ["cli.py"]):
        args = parse_args()
        assert args.command is None
        assert args.habit is None
        assert args.periodicity is None
        assert args.version is False
        assert args.dry_run is False

# -------- CLI Main Tests --------

def test_version_prints_version(mock_app_controller, capsys):
    """
    Test that the CLI prints the version when --version is passed.
    """
    with patch.object(sys, 'argv', ["cli.py", "--version"]):
        main()
        captured = capsys.readouterr()
        assert "Habit Tracker v" in captured.out

def test_dry_run_prints_command(mock_app_controller, capsys):
    """
    Test that dry-run mode prints the validated command without executing it.
    """
    with patch.object(sys, 'argv', ["cli.py", "--command", "add", "--dry-run"]):
        main()
        captured = capsys.readouterr()
        assert "Valid command: add" in captured.out

def test_invalid_command_prints_error(mock_app_controller, capsys):
    """
    Test that an unsupported command results in an error message.
    """
    with patch.object(sys, 'argv', ["cli.py", "--command", "explode"]):
        main()
        captured = capsys.readouterr()
        assert "Unsupported command" in captured.out

def test_add_command_missing_args(mock_app_controller, capsys):
    """
    Test that missing required arguments for 'add' command triggers usage hint.
    """
    with patch.object(sys, 'argv', ["cli.py", "--command", "add", "--habit", "Run"]):
        main()
        captured = capsys.readouterr()
        assert "Usage: --command add" in captured.out

def test_command_alias_translation(mock_app_controller):
    """
    Test that command aliases like 'done' are translated to their canonical form.
    """
    instance = MagicMock()
    mock_app_controller.return_value = instance
    with patch.object(sys, 'argv', ["cli.py", "--command", "done", "--habit", "run"]):
        main()
        instance.handle_command.assert_called_once_with("complete", habit_name="run", periodicity=None)

def test_no_command_shows_welcome(mock_app_controller, capsys):
    """
    Test that running the CLI with no arguments shows the welcome message.
    """
    instance = MagicMock()
    mock_app_controller.return_value = instance
    with patch.object(sys, 'argv', ["cli.py"]):
        main()
        captured = capsys.readouterr()
        assert "Welcome to Habit Tracker CLI" in captured.out
        instance.start.assert_called_once()

def test_main_handles_exception_gracefully(mock_app_controller, capsys):
    """
    Test that unexpected exceptions during command handling are caught and reported.
    """
    instance = MagicMock()
    instance.handle_command.side_effect = Exception("boom!")
    mock_app_controller.return_value = instance
    with patch.object(sys, 'argv', ["cli.py", "--command", "list"]):
        main()
        captured = capsys.readouterr()
        assert "Error: boom!" in captured.out
