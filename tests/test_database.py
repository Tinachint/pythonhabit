import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tempfile
import pytest
from habit.habit import Habit
from habit.database import DatabaseManager

@pytest.fixture
def temp_db_path():
    """
    This is a Pytest fixture that creates a temporary database file path for testing.
    
    This fixture generates a unique temporary file path with a .db extension
    that will be automatically cleaned up after test execution. This ensures
    database tests run in isolation without affecting production data.
    
    Yields:
        str: A filesystem path to a temporary database file
        
    Note:
        The temporary file is automatically removed after the test completes,
        regardless of test success or failure.
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        yield path
    finally:
        os.remove(path)

@pytest.fixture
def db(temp_db_path):
    """
    This Pytest fixture creates a DatabaseManager instance with a temporary database.
    
    Initializes a fresh database schema in the temporary database file before each test
    and ensures proper connection cleanup after test completion.
    
    Args:
        temp_db_path: The temporary database path fixture
        
    Yields:
        DatabaseManager: A fully initialized DatabaseManager instance connected to
                         a temporary database with the proper schema
    """
    db = DatabaseManager(temp_db_path)
    db.initialize_schema()
    try:
        yield db
    finally:
        db.close()  # This will properly close the connection

def test_save_and_load_habit(db):
    """
    This tests the complete round-trip persistence workflow for habit objects.
    
    Verifies that:
    1. A habit object can be successfully serialized and saved to the database
    2. The saved habit can be accurately retrieved and deserialized from the database
    3. All habit properties (name, periodicity, completion dates) are preserved
    4. Streak calculations remain consistent after the save/load cycle
    
    This test validates the core data persistence functionality of the application.
    """
    habit = Habit("Test", "daily")
    habit.complete_task()
    db.save_habit(habit)

    habits = db.load_all_habits()
    assert len(habits) == 1
    loaded = habits[0]
    assert loaded.name == "Test"
    assert loaded.periodicity == "daily"
    assert loaded.get_streak() == 1

def test_get_habit_by_name(db):
    """
    This tests the retrieval of a specific habit by its name identifier.
    
    Verifies that:
    1. A habit can be successfully saved to the database
    2. The same habit can be accurately retrieved using its name as a key
    3. All retrieved habit properties match the originally saved values
    
    This test validates the database indexing and query functionality for habit retrieval.
    """
    habit = Habit("Read", "weekly")
    habit.complete_task()
    db.save_habit(habit)

    retrieved = db.get_habit_by_name("Read")
    assert retrieved is not None
    assert retrieved.name == "Read"
    assert retrieved.periodicity == "weekly"

def test_delete_habit(db):
    """
    This tests the complete deletion workflow for habit objects from the database.
    
    Verifies that:
    1. A habit can be successfully saved to the database and subsequently retrieved
    2. The delete operation successfully removes the habit from the database
    3. Attempts to retrieve a deleted habit return None, confirming complete removal
    
    This test validates the database cleanup and data integrity maintenance functionality.
    """
    habit = Habit("Run", "monthly")
    db.save_habit(habit)

    assert db.get_habit_by_name("Run") is not None
    db.delete_habit("Run")
    assert db.get_habit_by_name("Run") is None
