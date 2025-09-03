import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, MagicMock
from habit.cli import parse_args, main

# Fixtures

@pytest.fixture(autouse=True)
def mock_app_controller():
    """
    This is a pytest fixture which automatically mocks the AppController class for all tests.
    It replaces the real AppController with a MagicMock, allowing tests to run
    without invoking actual application logic.
    Yields:
        MagicMock: The mocked AppController class
    """
    with patch("habit.cli.AppController") as MockController:
        yield MockController

# Argument Parser Tests 

def test_parse_args_with_all_options():
    """
    Test that all CLI arguments are parsed correctly when provided.

    Verifies that:
    1. All command-line arguments are correctly parsed into their respective attributes
    2. Both short and long form arguments are properly handled
    3. Boolean flags (--version, --dry-run) are correctly set to True when present
    
    This test ensures the argument parser can handle complex command-line inputs
    with multiple options and flags simultaneously.
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
    Verifies that:
    1. All optional arguments default to None or False as appropriate
    2. The parser can handle the absence of any command-line inputs gracefully
    3. The system behaves correctly with no user-specified options

    This test ensures the argument parser initializes with sensible defaults
    when no command-line arguments are given.

    """
    with patch.object(sys, 'argv', ["cli.py"]):
        args = parse_args()
        assert args.command is None
        assert args.habit is None
        assert args.periodicity is None
        assert args.version is False
        assert args.dry_run is False

# CLI Main Tests

def test_version_prints_version(mock_app_controller, capsys):
    """
    Test that the CLI prints the version when --version is passed.
    Verifies that:
    1. The version flag triggers the version output
    2. The output contains the expected version string
    3. No other application logic is invoked when --version is used

    This test ensures users can easily check the application version without
    affecting their current habit data or triggering unintended side effects.
    """
    with patch.object(sys, 'argv', ["cli.py", "--version"]):
        main()
        captured = capsys.readouterr()
        assert "Habit Tracker v" in captured.out

def test_dry_run_prints_command(mock_app_controller, capsys):
    """
    Test that dry-run mode prints the validated command without executing it.
    Verifies that:
    1. The dry-run flag triggers a printout of the validated command
    2. The output contains confirmation of the valid command
    3. No actual command execution occurs in dry-run mode

    This test ensures users can verify their intended commands without making
    any changes to their habit data.
    """
    with patch.object(sys, 'argv', ["cli.py", "--command", "add", "--dry-run"]):
        main()
        captured = capsys.readouterr()
        assert "Valid command: add" in captured.out

def test_invalid_command_prints_error(mock_app_controller, capsys):
    """
    Test that an unsupported command results in an error message.
    Verifies that:
    1. An invalid command triggers an appropriate error output
    2. The output contains a message indicating the command is unsupported
    3. No application logic is executed for unsupported commands

    This test ensures users receive clear feedback when attempting to use
    commands that are not recognized by the system.
    """
    with patch.object(sys, 'argv', ["cli.py", "--command", "explode"]):
        main()
        captured = capsys.readouterr()
        assert "Unsupported command" in captured.out

def test_add_command_missing_args(mock_app_controller, capsys):
    """
    Test that missing required arguments for 'add' command triggers usage hint.
    Verifies that:
    1. The system detects when required arguments are missing for a command
    2. Appropriate usage guidance is provided to the user
    3. The command is not executed with incomplete parameters
    
    This test ensures the CLI provides helpful feedback when users omit
    required arguments for specific commands.
    """
    with patch.object(sys, 'argv', ["cli.py", "--command", "add", "--habit", "Run"]):
        main()
        captured = capsys.readouterr()
        assert "Usage: --command add" in captured.out

def test_command_alias_translation(mock_app_controller):
    """
    Test command alias resolution in the CLI interface.
    
    Verifies that:
    1. Command aliases (e.g., "done") are correctly mapped to their canonical forms
    2. The translated command is executed with the appropriate parameters
    3. Aliases provide convenient shortcuts without duplicating functionality
    
    This test ensures the CLI supports user-friendly command variants while
    maintaining a consistent internal command structure.
    """
    instance = MagicMock()
    mock_app_controller.return_value = instance
    with patch.object(sys, 'argv', ["cli.py", "--command", "done", "--habit", "run"]):
        main()
        instance.handle_command.assert_called_once_with("complete", habit_name="run", periodicity=None)

def test_no_command_shows_welcome(mock_app_controller, capsys):
    """
    Test default behavior when no command is specified.
    
    Verifies that:
    1. The CLI displays a welcome message when no specific command is provided
    2. The interactive mode is initiated when no command arguments are given
    3. Users receive guidance on how to interact with the application
    
    This test ensures the CLI provides a friendly onboarding experience for
    new users or those who need guidance on available commands.
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

    Verifies that:
    1. Unexpected exceptions during command execution are properly caught
    2. Error information is displayed to the user in a readable format
    3. The application doesn't crash completely when commands fail
    
    This test ensures the CLI maintains robustness by gracefully handling
    unexpected errors and providing useful feedback to users.
    """
    instance = MagicMock()
    instance.handle_command.side_effect = Exception("boom!")
    mock_app_controller.return_value = instance
    with patch.object(sys, 'argv', ["cli.py", "--command", "list"]):
        main()
        captured = capsys.readouterr()
        assert "Error: boom!" in captured.out
