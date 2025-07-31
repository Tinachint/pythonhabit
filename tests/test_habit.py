import pytest
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from habit import Habit  # adjust if using subfolders
from unittest.mock import patch

#  Fixtures
@pytest.fixture
def daily_habit():
    """Create a daily habit fixture."""
    return Habit("Meditate", "daily")

@pytest.fixture
def habit_with_streak():
    """Create a weekly habit with a 3-week streak."""
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
    """Ensure Habit initializes with correct values."""
    assert daily_habit.name == "Meditate"
    assert daily_habit.periodicity == "daily"
    assert isinstance(daily_habit.creation_date, datetime)
    assert len(daily_habit.dates) == 0

#  Invalid Input
def test_invalid_periodicity():
    """Should raise error for unsupported periodicity."""
    with pytest.raises(ValueError):
        Habit("Invalid", "yearly")

#  Task Completion
def test_complete_task(daily_habit):
    """Test marking a habit as completed."""
    today = datetime.now().date()
    result = daily_habit.complete_task()
    assert result == today
    assert today in daily_habit.dates

#  Streak Logic
def test_daily_streak():
    """Test streak calculation for daily completions."""
    habit = Habit("Exercise", "daily")
    today = datetime.now().date()
    habit._dates = {today - timedelta(days=i) for i in range(3)}
    assert habit.get_streak() == 3

def test_broken_streak():
    """Should detect broken daily streak."""
    habit = Habit("Exercise", "daily")
    today = datetime.now().date()
    habit._dates = {today, today - timedelta(days=2)}
    assert habit.get_streak() == 1

def test_monthly_streak():
    """Test streak calculation for monthly completions."""
    habit = Habit("Pay Rent", "monthly")
    today = datetime.now().date()
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

#  Representation
def test_str_representation(daily_habit):
    """Test string representation of habit."""
    rep = str(daily_habit)
    assert "Meditate" in rep and "daily" in rep

#  Time Mocking
def test_complete_task_with_mock_time():
    """Test completion using a fixed mocked datetime."""
    fixed_time = datetime(2023, 1, 1, 12, 0)
    fixed_date = fixed_time.date()

    with patch("habit.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)  # fix constructor
        habit = Habit("Test", "daily")
        logged = habit.complete_task()
        assert logged == fixed_date
        assert fixed_date in habit.dates
