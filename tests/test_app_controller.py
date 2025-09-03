import pytest
from unittest.mock import MagicMock, patch
from habit.app_controller import AppController

@pytest.fixture
def controller():
    """Fixture to create an AppController instance with a mocked HabitTracker.

    This fixture patches the HabitTracker class within the AppController module,
    replacing it with a MagicMock. This allows tests to run without invoking actual
    application logic, enabling isolated unit testing of the AppController methods.
    Yields:
        AppController: An instance of AppController with a mocked HabitTracker.
    
    """
    with patch("habit.app_controller.HabitTracker") as MockTracker:
        instance = AppController()
        instance.tracker = MockTracker.return_value
        return instance

def test_handle_add_valid(controller):
    """Test adding a habit with valid name and periodicity. 

       Verifies that:
       1. The handle_add method correctly processes valid name and periodicity parameters
       2. The tracker's add_habit method is called exactly once
       3. No errors are raised when valid parameters are provided
    
       This test ensures the core habit creation functionality works as expected
        with proper input validation and delegation to the tracker.
    """
    controller.handle_add(name="Read", periodicity="daily")
    controller.tracker.add_habit.assert_called_once()

def test_handle_add_missing_fields(controller, capsys):
    """Test add command with missing name and periodicity.
    
       Verifies that:
       1. The handle_add method detects missing name and periodicity inputs
       2. An appropriate error message is printed to the console
       3. The tracker's add_habit method is not called when inputs are missing
       
       This test ensures input validation works correctly for the add command,
       preventing incomplete habit creation attempts.
    """
    with patch("builtins.input", side_effect=["", ""]):
        controller.handle_add()
        captured = capsys.readouterr()
        assert "❗ Missing habit name or periodicity." in captured.out

def test_handle_add_invalid_periodicity(controller, capsys):
    """Test add command with invalid periodicity.
    
       Verifies that:
       1. The handle_add method detects an invalid periodicity input
       2. An appropriate error message is printed to the console
       3. The tracker's add_habit method is not called when periodicity is invalid
       
       This test ensures input validation works correctly for the add command,
       preventing habit creation with unsupported periodicity values."""
    with patch("builtins.input", side_effect=["Run", "yearly"]):
        controller.handle_add()
        captured = capsys.readouterr()
        assert "⚠️" in captured.out

def test_handle_complete_success(controller, capsys):
    """Test completing a habit successfully.
       Verifies that:

       1. The handle_complete method processes a valid habit name
       2. The habit's complete_task method is called and returns a completion date
       3. The habit is saved to the database via the tracker's db.save_habit method
       4. A success message with the completion date is printed to the console
    
       This test ensures the complete command functions correctly for existing habits,
       providing user feedback and persisting changes.
    """
    mock_habit = MagicMock()
    mock_habit.name = "Read"
    mock_habit.complete_task.return_value = "2025-08-07"
    mock_habit.get_streak.return_value = 3
    controller.tracker.find_habit_by_name.return_value = mock_habit

    controller.handle_complete("Read")
    controller.tracker.db.save_habit.assert_called_once_with(mock_habit)
    captured = capsys.readouterr()
    assert "✔ 'Read' completed for 2025-08-07" in captured.out

def test_handle_complete_not_found(controller, capsys):
    """Test completing a habit that doesn't exist.

       Verifies that:
       1. The handle_complete method handles a non-existent habit name gracefully
       2. An appropriate error message is printed to the console
       3. No attempt is made to call complete_task or save_habit on a non-existent habit

         This test ensures the complete command provides clear feedback when users
            attempt to complete habits that are not found in the tracker.
       """
    controller.tracker.find_habit_by_name.return_value = None
    controller.handle_complete("Unknown")
    captured = capsys.readouterr()
    assert "🚫 Habit not found." in captured.out

def test_handle_update_success(controller, capsys):
    """Test updating a habit's periodicity.

       Verifies that:
       1. The handle_update method processes valid name and new periodicity parameters
       2. The tracker's update_habit method is called and returns True indicating success
       3. A success message is printed to the console confirming the update
    
      This test ensures the update command functions correctly for existing habits,
      allowing users to modify habit properties with appropriate feedback.
    """
    controller.tracker.find_habit_by_name.return_value = MagicMock()
    controller.tracker.update_habit.return_value = True
    controller.handle_update(name="Read", new_periodicity="weekly")
    captured = capsys.readouterr()
    assert "🔄 Habit 'Read' updated to periodicity: weekly" in captured.out

def test_handle_update_missing_fields(controller, capsys):
    """Test update command with missing inputs.

       Verifies that:
       1. The handle_update method detects missing name and new periodicity inputs
       2. An appropriate error message is printed to the console
       3. The tracker's update_habit method is not called when inputs are missing

       This test ensures input validation works correctly for the update command,
       preventing incomplete update attempts.
"""
    with patch("builtins.input", side_effect=["", ""]):
        controller.handle_update()
        captured = capsys.readouterr()
        assert "❗ Missing required fields." in captured.out

def test_handle_delete_success(controller, capsys):
    """Test deleting a habit successfully.

       Verifies that:
       1. The handle_delete method processes a valid habit name
       2. The tracker's delete_habit method is called and returns True indicating success
       3. A success message is printed to the console confirming the deletion

        This test ensures the delete command functions correctly for existing habits,
         providing user feedback upon successful removal.

"""
    controller.tracker.delete_habit.return_value = True
    controller.handle_delete("Read")
    captured = capsys.readouterr()
    assert "🗑️ Habit 'Read' deleted." in captured.out

def test_handle_delete_not_found(controller, capsys):
    """Test deleting a habit that doesn't exist.
       Verifies that:
       1. The handle_delete method handles a non-existent habit name gracefully
       2. An appropriate error message is printed to the console
       3. No attempt is made to delete a non-existent habit

        This test ensures the delete command provides clear feedback when users
        attempt to remove habits that are not found in the tracker.
    """
    controller.tracker.delete_habit.return_value = False
    controller.handle_delete("Unknown")
    captured = capsys.readouterr()
    assert "🚫 Habit not found." in captured.out

def test_handle_list_with_habits(controller, capsys):
    """Test listing habits with streaks.
       Verifies that:
       1. The handle_list method retrieves and displays existing habits
       2. The output includes habit names and their current streaks
       3. A header message is printed when habits are present
       
       This test ensures the list command provides users with a clear overview
       of their tracked habits and progress.
    """
    mock_habit = MagicMock()
    mock_habit.name = "Read"
    mock_habit.periodicity = "daily"
    mock_habit.get_streak.return_value = 2
    controller.tracker.habits = [mock_habit]

    controller.handle_list()
    captured = capsys.readouterr()
    assert "📌 Current Habits:" in captured.out
    assert "Read" in captured.out

def test_handle_list_empty(controller, capsys):
    """Test listing when no habits are present.
       Verifies that:
       1. The handle_list method handles an empty habit list gracefully
       2. An appropriate message is printed indicating no habits are found
       3. No errors occur when the habit list is empty

        This test ensures the list command provides clear feedback when users
        have not yet added any habits to their tracker.
    """
    controller.tracker.habits = []
    controller.handle_list()
    captured = capsys.readouterr()
    assert "📭 No habits found." in captured.out

def test_handle_command_dispatch(controller):
    """Test command dispatching via handle_command.
       Verifies that:
       1. The handle_command method correctly routes commands to their respective handlers
       2. The appropriate handler methods are called based on the command input
       3. No errors occur during command dispatching

        This test ensures the central command handling mechanism functions correctly,
        enabling users to interact with the application via various commands.
    """
    controller.handle_command("add", habit_name="Run", periodicity="daily")
    controller.tracker.add_habit.assert_called_once()

def test_handle_command_unknown(controller, capsys):
    """Test unknown command handling.
       Verifies that:
       1. The handle_command method detects unsupported commands
       2. An appropriate error message is printed to the console
       3. No application logic is executed for unknown commands

        This test ensures users receive clear feedback when attempting to use
        commands that are not recognized by the system.
    """
    controller.handle_command("explode")
    captured = capsys.readouterr()
    assert "❓ Unknown command" in captured.out
