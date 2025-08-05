import pytest
from unittest.mock import MagicMock
from habit.habit import Habit
from habit.habit_tracker import HabitTracker

@pytest.fixture
def mock_db():
    """Mock the database layer used for habit persistence."""
    db = MagicMock()
    db.load_all_habits.return_value = []
    return db

@pytest.fixture
def tracker(monkeypatch, mock_db):
    """
    Create a HabitTracker instance using the mocked DatabaseManager.
    
    Monkeypatch replaces the real database with the mock for isolated testing.
    """
    monkeypatch.setattr("habit.habit_tracker.DatabaseManager", lambda _: mock_db)
    return HabitTracker("test.db")

def test_add_habit(tracker, mock_db):
    """Test that a new habit can be added and is persisted to the mock DB."""
    habit = Habit("Read", "daily")
    tracker.add_habit(habit)
    assert habit in tracker.habits
    mock_db.save_habit.assert_called_once_with(habit)

def test_delete_existing_habit(tracker, mock_db):
    """Test deleting an existing habit removes it and updates the mock DB."""
    habit = Habit("Exercise", "weekly")
    tracker.habits.append(habit)
    mock_db.delete_habit.reset_mock()

    success = tracker.delete_habit("Exercise")
    assert success
    assert habit not in tracker.habits
    mock_db.delete_habit.assert_called_once_with("Exercise")

def test_delete_nonexistent_habit(tracker, mock_db):
    """Test attempting to delete a habit that does not exist returns False."""
    success = tracker.delete_habit("Nonexistent")
    assert not success
    mock_db.delete_habit.assert_not_called()

def test_update_habit(tracker, mock_db):
    """Test updating a habit's name and periodicity reflects in tracker and DB."""
    habit = Habit("Sleep", "daily")
    tracker.habits.append(habit)

    updated = tracker.update_habit("Sleep", "Rest", "weekly")
    assert updated
    assert habit.name == "Rest"
    assert habit.periodicity == "weekly"
    mock_db.save_habit.assert_called_once_with(habit)

def test_update_to_existing_name_raises(tracker):
    """
    Test that updating a habit to a name that already exists raises a ValueError.
    
    This prevents duplicate habit names within the tracker.
    """
    h1 = Habit("Yoga", "daily")
    h2 = Habit("Read", "weekly")
    tracker.habits.extend([h1, h2])

    with pytest.raises(ValueError):
        tracker.update_habit("Yoga", "Read", "daily")

def test_find_habit_by_name_case_insensitive(tracker):
    """Test that habit lookup is case-insensitive and returns correct instance."""
    habit = Habit("Meditate", "daily")
    tracker.habits.append(habit)
    found = tracker.find_habit_by_name("meditate")
    assert found is habit

def test_list_all_habits(tracker):
    """Test that listing all habits returns the complete set in expected order."""
    h1 = Habit("Run", "daily")
    h2 = Habit("Pray", "weekly")
    tracker.habits.extend([h1, h2])
    result = tracker.list_all_habits()
    assert result == [h1, h2]
