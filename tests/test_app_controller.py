import pytest
from unittest.mock import MagicMock, patch
from habit.app_controller import AppController

@pytest.fixture
def controller():
    """Create an AppController instance with mocked HabitTracker."""
    with patch("habit.app_controller.HabitTracker") as MockTracker:
        instance = AppController()
        instance.tracker = MockTracker.return_value
        return instance

def test_handle_add_valid(controller):
    """Test adding a habit with valid name and periodicity."""
    controller.handle_add(name="Read", periodicity="daily")
    controller.tracker.add_habit.assert_called_once()

def test_handle_add_missing_fields(controller, capsys):
    """Test add command with missing name and periodicity."""
    with patch("builtins.input", side_effect=["", ""]):
        controller.handle_add()
        captured = capsys.readouterr()
        assert "❗ Missing habit name or periodicity." in captured.out

def test_handle_add_invalid_periodicity(controller, capsys):
    """Test add command with invalid periodicity."""
    with patch("builtins.input", side_effect=["Run", "yearly"]):
        controller.handle_add()
        captured = capsys.readouterr()
        assert "⚠️" in captured.out

def test_handle_complete_success(controller, capsys):
    """Test completing a habit successfully."""
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
    """Test completing a habit that doesn't exist."""
    controller.tracker.find_habit_by_name.return_value = None
    controller.handle_complete("Unknown")
    captured = capsys.readouterr()
    assert "🚫 Habit not found." in captured.out

def test_handle_update_success(controller, capsys):
    """Test updating a habit's periodicity."""
    controller.tracker.find_habit_by_name.return_value = MagicMock()
    controller.tracker.update_habit.return_value = True
    controller.handle_update(name="Read", new_periodicity="weekly")
    captured = capsys.readouterr()
    assert "🔄 Habit 'Read' updated to periodicity: weekly" in captured.out

def test_handle_update_missing_fields(controller, capsys):
    """Test update command with missing inputs."""
    with patch("builtins.input", side_effect=["", ""]):
        controller.handle_update()
        captured = capsys.readouterr()
        assert "❗ Missing required fields." in captured.out

def test_handle_delete_success(controller, capsys):
    """Test deleting a habit successfully."""
    controller.tracker.delete_habit.return_value = True
    controller.handle_delete("Read")
    captured = capsys.readouterr()
    assert "🗑️ Habit 'Read' deleted." in captured.out

def test_handle_delete_not_found(controller, capsys):
    """Test deleting a habit that doesn't exist."""
    controller.tracker.delete_habit.return_value = False
    controller.handle_delete("Unknown")
    captured = capsys.readouterr()
    assert "🚫 Habit not found." in captured.out

def test_handle_list_with_habits(controller, capsys):
    """Test listing habits with streaks."""
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
    """Test listing when no habits are present."""
    controller.tracker.habits = []
    controller.handle_list()
    captured = capsys.readouterr()
    assert "📭 No habits found." in captured.out

def test_handle_command_dispatch(controller):
    """Test command dispatching via handle_command."""
    controller.handle_command("add", habit_name="Run", periodicity="daily")
    controller.tracker.add_habit.assert_called_once()

def test_handle_command_unknown(controller, capsys):
    """Test unknown command handling."""
    controller.handle_command("explode")
    captured = capsys.readouterr()
    assert "❓ Unknown command" in captured.out
