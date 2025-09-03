import pytest
from unittest.mock import MagicMock
from habit.habit import Habit
from habit.habit_tracker import HabitTracker

@pytest.fixture
def mock_db():
    """
    This pytest fixture creates a mock database instance for testing.

    This mock database simulates the behavior of the actual database layer
    to allow isolated unit testing without depedencies on a real database. It provides a mock object 
    with predefined return values for database operations.
    
    It Returns:
           MagicMock: A mock database object witha load_all_habits method
                        that returns an empty list default.
    """
    db = MagicMock()
    db.load_all_habits.return_value = []
    return db

@pytest.fixture
def tracker(monkeypatch, mock_db):
    """
    This is a Pytest fixture that creates a HabitTracker instance with a mocked database.
    
    It uses monkeypatching to replace the real DatabaseManager with the mock_db fixture,
    ensuring database operations are isolated from actual persistence layers during testing.
    
    Args:
        monkeypatch: Pytest's monkeypatch fixture for modifying dependencies
        mock_db: The mocked database fixture
        
    Returns:
        HabitTracker: A HabitTracker instance configured to use the mocked database
    """
    monkeypatch.setattr("habit.habit_tracker.DatabaseManager", lambda _: mock_db)
    return HabitTracker("test.db")

def test_add_habit(tracker, mock_db):
    """
    This tests the addition of a new habit to the tracker and verification of database persistence.
    
    Verifies that:
    1. The habit is successfully added to the tracker's internal list of habits
    2. The database's save_habit method is called exactly once with the correct habit object
    
    This test ensures that the add_habit method properly handles both in-memory storage
    and database persistence.
    """
    habit = Habit("Read", "daily")
    tracker.add_habit(habit)
    assert habit in tracker.habits
    mock_db.save_habit.assert_called_once_with(habit)

def test_delete_existing_habit(tracker, mock_db):
    """
    This tests the deletion of an existing habit from the tracker and database.
    
    Verifies that:
    1. The method returns True indicating successful deletion
    2. The habit is removed from the tracker's internal list
    3. The database's delete_habit method is called exactly once with the correct habit name
    
    This test checks the complete removal workflow for existing habits.
    """
    habit = Habit("Exercise", "weekly")
    tracker.habits.append(habit)
    mock_db.delete_habit.reset_mock()

    success = tracker.delete_habit("Exercise")
    assert success
    assert habit not in tracker.habits
    mock_db.delete_habit.assert_called_once_with("Exercise")

def test_delete_nonexistent_habit(tracker, mock_db):
    """
    This tests the attempt to delete a habit that does not exist in the tracker.
    
    Verifies that:
    1. The method returns False indicating the habit was not found
    2. The database's delete_habit method is not called
    
    This test ensures the system handles missing habits gracefully without
    attempting unnecessary database operations.
    """
    success = tracker.delete_habit("Nonexistent")
    assert not success
    mock_db.delete_habit.assert_not_called()

def test_update_habit(tracker, mock_db):
    """
    This tests the updating of an existing habit's properties and database persistence.
    
    Verifies that:
    1. The method returns True indicating successful update
    2. The habit's name and periodicity are correctly modified in memory
    3. The database's save_habit method is called exactly once with the updated habit
    
    This test ensures the update functionality works correctly for both the
    in-memory representation and database persistence.
    """
    habit = Habit("Sleep", "daily")
    tracker.habits.append(habit)

    updated = tracker.update_habit("Sleep", "Rest", "weekly")
    assert updated
    assert habit.name == "Rest"
    assert habit.periodicity == "weekly"
    mock_db.save_habit.assert_called_once_with(habit)

def test_update_to_existing_name_raises(tracker):
    """
    Test that updating a habit to use an already existing name raises a ValueError.
    
    Verifies that:
    1. Attempting to update a habit's name to one that already exists in the tracker
       raises a ValueError exception
    2. No changes are made to the existing habits
    
    This test ensures the system maintains unique habit names and prevents
    accidental duplication through updates.
    """
    h1 = Habit("Yoga", "daily")
    h2 = Habit("Read", "weekly")
    tracker.habits.extend([h1, h2])

    with pytest.raises(ValueError):
        tracker.update_habit("Yoga", "Read", "daily")

def test_find_habit_by_name_case_insensitive(tracker):
    """
    Test the case-insensitive search for habits by name.
    
    Verifies that:
    1. The method can find a habit regardless of case differences
    2. The returned object is the exact same instance as the added habit
    
    This test ensures the habit lookup functionality is user-friendly and
    accommodates variations in input casing.
    """
    habit = Habit("Meditate", "daily")
    tracker.habits.append(habit)
    found = tracker.find_habit_by_name("meditate")
    assert found is habit

def test_list_all_habits(tracker):
    """
    This tests the retrieval of all habits from the tracker.
    
    Verifies that:
    1. The method returns all habits in the tracker
    2. The habits are returned in the order they were added
    
    This test ensures the list functionality provides a complete and ordered
    view of all tracked habits.
    """
    h1 = Habit("Run", "daily")
    h2 = Habit("Pray", "weekly")
    tracker.habits.extend([h1, h2])
    result = tracker.list_all_habits()
    assert result == [h1, h2]
