import pytest
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from habit.analytics import (
    filter_habits_by_periodicity,
    longest_streak_for,
    get_all_streaks,
    get_habit_with_longest_streak
)
from habit.habit import Habit

# Fixtures
@pytest.fixture
def daily_habit_with_streak():
    """This fixture creates a daily habit with a 5-day streak.

     it Returns:
        Habit: A daily Habit instance with a 5-day streak."""
    habit = Habit("Exercise", "daily")
    today = date.today()
    habit._dates = {today - timedelta(days=i) for i in range(5)}  # 5-day streak
    return habit

@pytest.fixture
def weekly_habit_with_gap():
    """This fixture creates a weekly habit with a gap in completions.

     it Returns:
        Habit: A weekly Habit instance with a gap in the streak."""
    habit = Habit("Jog", "weekly")
    today = date.today()
    habit._dates = {
        today - timedelta(weeks=3),
        today - timedelta(weeks=1),
        today
    }  # gap between week 3 and 2
    return habit

@pytest.fixture
def monthly_habit_full_streak():
    """This fixture creates a monthly habit with a perfect 4-month streak.
     it Returns:
        Habit: A monthly Habit instance with a 4-month streak."""
    habit = Habit("Budget", "monthly")
    today = date.today()
    habit._dates = {
        today - relativedelta(months=i) for i in range(4)  # 4-month streak
    }
    return habit

@pytest.fixture
def mixed_habits(daily_habit_with_streak, weekly_habit_with_gap, monthly_habit_full_streak):
    """This fixture combines multiple habit types into a single list.

     it Returns:
        List[Habit]: A list containing various Habit instances with different periodicities and 
        streaks(one daily,weekly and monthly)."""
    return [daily_habit_with_streak, weekly_habit_with_gap, monthly_habit_full_streak]

# Tests for filter_habits_by_periodicity
def test_filter_habits_by_periodicity(mixed_habits):
    """This tests filtering habits by periodicity.
    It verifies that:

      - The function correctly filters habits by periodicity
      - Only daily habits are returned when filtering for "Daily"
      - The returned habits match the expected names and counts."""
    
    daily_habits = filter_habits_by_periodicity(mixed_habits, "DAILY")
    assert len(daily_habits) == 1
    assert daily_habits[0].name == "Exercise"

# Tests for longest_streak_for
def test_longest_streak_daily(daily_habit_with_streak):
    """This tests longest_streak_for function with a daily habit having a continuous streak.
    
    It Verifies that:
        - The function correctly calculates the longest streak for a daily habit
        - A habit with 5 consecutive daily completions returns a streak of 5
    """
    assert longest_streak_for(daily_habit_with_streak) == 5

def test_longest_streak_with_gap(weekly_habit_with_gap):
    """This tests longest_streak_for function with a weekly habit having a gap in completions.
    
    Verifies that:
        - The function correctly identifies the current streak after a gap
        - A habit with completions at week 0, 1, and 3 (missing week 2) 
          returns a streak of 2 (weeks 0 and 1)
    """
    assert longest_streak_for(weekly_habit_with_gap) == 2  # last 2 weeks only

def test_longest_streak_monthly(monthly_habit_full_streak):
    """This tests longest_streak_for function with a monthly habit having a perfect streak.
    
    Verifies that:
        - The function correctly calculates the longest streak for a monthly habit
        - A habit with 4 consecutive monthly completions returns a streak of 4
    """
    assert longest_streak_for(monthly_habit_full_streak) == 4

def test_longest_streak_empty():
    """This tests longest_streak_for function with a habit that has no completions.
    
    Verifies that:
        - The function returns 0 for a habit with no completion history
    """
    habit = Habit("Nothing", "daily")
    assert longest_streak_for(habit) == 0

# Tests for get_all_streaks
def test_get_all_streaks(mixed_habits):
    """This tests get_all_streaks function with a mixed list of habits.
    
    Verifies that:
        - The function returns streaks for all habits in the input list
        - All returned streak values are integers
        - The result includes all expected habit names
    """
    streaks = get_all_streaks(mixed_habits)
    names = [s[0] for s in streaks]
    assert "Exercise" in names
    assert "Jog" in names
    assert "Budget" in names
    assert all(isinstance(s[1], int) for s in streaks)

# Tests for get_habit_with_longest_streak
def test_get_habit_with_longest_streak(mixed_habits):
    """This tests get_habit_with_longest_streak function with habits of varying streak lengths.
    
    Verifies that:
        - The function correctly identifies the habit with the longest streak
        - From the mixed_habits fixture, the daily exercise habit with a 5-day streak
          is correctly identified as having the longest streak
    """
    result = get_habit_with_longest_streak(mixed_habits)
    assert result == ("Exercise", 5)

def test_get_habit_with_longest_streak_none():
    """This tests get_habit_with_longest_streak function with an empty list.
    
    Verifies that:
        - The function returns None when provided with an empty list of habits
    """
    assert get_habit_with_longest_streak([]) is None

def test_get_habit_with_longest_streak_zero_streaks():
    """This tests get_habit_with_longest_streak function with habits that have no streaks.
    
    Verifies that:
        - The function returns None when all habits in the list have no completions
          (and thus zero-length streaks)
    """
    h1 = Habit("Empty", "daily")
    h2 = Habit("Also Empty", "weekly")
    assert get_habit_with_longest_streak([h1, h2]) is None
