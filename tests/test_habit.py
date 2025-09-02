import pytest
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from habit.habit import Habit
from unittest.mock import patch

#  Fixtures
@pytest.fixture
def daily_habit():
    """Pytest fixture to create a daily habit fixture.
    it Returns:
        Habit: A daily Habit instance.
    """
    return Habit("Meditate", "daily")

@pytest.fixture
def habit_with_streak():
    """This fixture creates a weekly habit with a 3-week streak
     it Returns:
        Habit: A weekly Habit instance with a 3-week streak."""
    habit = Habit("Read", "weekly")
    today = datetime.now().date()
    habit._dates = {
        today - timedelta(weeks=2),
        today - timedelta(weeks=1),
        today
    }
    return habit

#  Habit Creation
def test_create_habit(daily_habit):
    """Test that a Hsbit initializes with correct attributes.
    
    Verifies:
     -The habit's name is set correctly.
     -The periodicity is set correctly.
     -The creation date is a datetime instance.
    
    """
    assert daily_habit.name == "Meditate"
    assert daily_habit.periodicity == "daily"
    assert isinstance(daily_habit.creation_date, datetime)
    assert len(daily_habit._dates) == 0

#  Invalid Input
def test_invalid_periodicity():
    """This tests that iniatilizing a Habit with an invalid periodicity raises ValueError.
    This ensures the Habit class validates periodicity inputs during installation.
    """
    with pytest.raises(ValueError):
        Habit("Invalid", "yearly")

#  Task Completion
def test_complete_task(daily_habit):
    """Test the complete_task method of the habit
    This verifies that:
        - Completing a task returns the current date.
        - The date is added to the habit's _dates set."""
    today = datetime.now().date()
    result = daily_habit.complete_task()
    assert result == today
    assert today in daily_habit._dates

#  Streak Logic
def test_daily_streak():
    """Test streak calculation for a habit with consecutive daily completions.
      This stimulates a habit completed for the last 3 consecutive days and
        checks if the streak is calculated correctly.
    """
    habit = Habit("Exercise", "daily")
    today = datetime.now().date()
    habit._dates = {today - timedelta(days=i) for i in range(3)}
    assert habit.get_streak() == 3

def test_broken_streak():
    """This tests the streak calculation for a habit with a broken completions sequance.
    It stimulates a habit with completions on two non-consecutive days and checks 
    if the streak is calculated as 1."""
    habit = Habit("Exercise", "daily")
    today = datetime.now().date()
    habit._dates = {today, today - timedelta(days=2)}
    assert habit.get_streak() == 1

def test_monthly_streak():
    """Test streak calculation for monthly completions.
    This simulates a habit completed on the same day for the last 3 months and
    checks if the streak is calculated correctly."""

    habit = Habit("Pay Rent", "monthly")
    today = datetime.now().date()
    habit._dates = {
        today,
        (today - relativedelta(months=1)),
        (today - relativedelta(months=2))
    }
    assert habit.get_streak() == 3

def test_streak_with_no_completions():
    """This calculates streaks for habits with no cpmpletions.
    Should return 0 streak for empty completions list.
    """
    habit = Habit("Yoga", "weekly")
    assert habit.get_streak() == 0

#  Representation
def test_str_representation(daily_habit):
    """Test string representation of a Habit object.
    This verifies that the habit's name and periodicity are included in the string."""
    rep = str(daily_habit)
    assert "Meditate" in rep and "daily" in rep

#  Time Mocking
def test_complete_task_with_mock_time():
    """This tests the complete_task method using a mocked datetime.
    It uses unittest.mock to fix the current time and verities that the completion is 
    logged with the expected date.
    """
    fixed_time = datetime(2023, 1, 1, 12, 0)
    fixed_date = fixed_time.date()

    with patch("habit.habit.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        habit = Habit("Test", "daily")
        logged = habit.complete_task()
        assert logged == fixed_date
        assert fixed_date in habit._dates

