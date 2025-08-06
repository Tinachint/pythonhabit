import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import tempfile
import pytest
from habit.habit import Habit
from habit.database import DatabaseManager

@pytest.fixture
def temp_db_path():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    try:
        yield path
    finally:
        os.remove(path)

@pytest.fixture
def db(temp_db_path):
    db = DatabaseManager(temp_db_path)
    db.initialize_schema()
    try:
        yield db
    finally:
        db.close()  # This will properly close the connection

def test_save_and_load_habit(db):
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
    habit = Habit("Read", "weekly")
    habit.complete_task()
    db.save_habit(habit)

    retrieved = db.get_habit_by_name("Read")
    assert retrieved is not None
    assert retrieved.name == "Read"
    assert retrieved.periodicity == "weekly"

def test_delete_habit(db):
    habit = Habit("Run", "monthly")
    db.save_habit(habit)

    assert db.get_habit_by_name("Run") is not None
    db.delete_habit("Run")
    assert db.get_habit_by_name("Run") is None
