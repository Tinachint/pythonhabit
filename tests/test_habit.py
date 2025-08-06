import pytest
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from habit.habit import Habit  
from unittest.mock import patch
from unittest.mock import Mock

# Fixtures
@pytest.fixture
def daily_habit():
    """Create a daily habit fixture."""
    return Habit("Meditate", "daily")

@pytest.fixture
def habit_with_streak():
    """Create a weekly habit with a 3-week streak."""
    habit = Habit("Read", "weekly")
    today = date.today()
    habit._dates = {
        today - timedelta(weeks=2),
        today - timedelta(weeks=1),
        today
    }
    return habit

# Habit Creation
def test_create_habit(daily_habit):
    """Ensure Habit initializes with correct values."""
    assert daily_habit.name == "Meditate"
    assert daily_habit.periodicity == "daily"
    assert isinstance(daily_habit.creation_date, datetime)
    assert len(daily_habit.completions) == 0

# Invalid Input
def test_invalid_periodicity():
    """Should raise error for unsupported periodicity."""
    with pytest.raises(ValueError):
        Habit("Invalid", "yearly")

# Task Completion
def test_complete_task(daily_habit):
    """Test marking a habit as completed."""
    today = date.today()
    result = daily_habit.complete_task()
    assert result == today
    assert today in daily_habit.completions

# Streak Logic
def test_daily_streak():
    """Test streak calculation for daily completions."""
    habit = Habit("Exercise", "daily")
    today = date.today()
    habit._dates = {today - timedelta(days=i) for i in range(3)}
    assert habit.get_streak() == 3

def test_broken_streak():
    """Should detect broken daily streak."""
    habit = Habit("Exercise", "daily")
    today = date.today()
    habit._dates = {today, today - timedelta(days=2)}
    assert habit.get_streak() == 1

def test_monthly_streak():
    """Test streak calculation for monthly completions."""
    habit = Habit("Pay Rent", "monthly")
    today = date.today()
    habit._dates = {
        today,
        (today - relativedelta(months=1)),
        (today - relativedelta(months=2))
    }
    assert habit.get_streak() == 3

def test_streak_with_no_completions():
    """Should return 0 streak for empty completions list."""
    habit = Habit("Yoga", "weekly")
    assert habit.get_streak() == 0

# Representation
def test_str_representation(daily_habit):
    """Test string representation of habit."""
    rep = str(daily_habit)
    assert "Meditate" in rep and "daily" in rep

# Time Mocking
def test_complete_task_with_mock_time():
    """Test completion using a fixed mocked datetime."""
    fixed_datetime = datetime(2023, 1, 1, 12, 0, 0)

    # Patch 'habit.habit.datetime' where it's used
    with patch('habit.habit.datetime') as mock_datetime:
        # Mock datetime.now() to return the fixed datetime
        mock_now = Mock()
        mock_now.date.return_value = fixed_datetime.date()
        mock_datetime.now.return_value = mock_now

        habit = Habit("Test", "daily")
        logged = habit.complete_task()

        assert logged == fixed_datetime.date()
        assert logged in habit.completions
        assert len(habit.completions) == 1