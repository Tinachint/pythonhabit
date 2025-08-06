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
    habit = Habit("Exercise", "daily")
    today = date.today()
    habit._dates = {today - timedelta(days=i) for i in range(5)}  # 5-day streak
    return habit

@pytest.fixture
def weekly_habit_with_gap():
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
    habit = Habit("Budget", "monthly")
    today = date.today()
    habit._dates = {
        today - relativedelta(months=i) for i in range(4)  # 4-month streak
    }
    return habit

@pytest.fixture
def mixed_habits(daily_habit_with_streak, weekly_habit_with_gap, monthly_habit_full_streak):
    return [daily_habit_with_streak, weekly_habit_with_gap, monthly_habit_full_streak]

# Tests for filter_habits_by_periodicity
def test_filter_habits_by_periodicity(mixed_habits):
    daily_habits = filter_habits_by_periodicity(mixed_habits, "DAILY")
    assert len(daily_habits) == 1
    assert daily_habits[0].name == "Exercise"

# Tests for longest_streak_for
def test_longest_streak_daily(daily_habit_with_streak):
    assert longest_streak_for(daily_habit_with_streak) == 5

def test_longest_streak_with_gap(weekly_habit_with_gap):
    assert longest_streak_for(weekly_habit_with_gap) == 2  # last 2 weeks only

def test_longest_streak_monthly(monthly_habit_full_streak):
    assert longest_streak_for(monthly_habit_full_streak) == 4

def test_longest_streak_empty():
    habit = Habit("Nothing", "daily")
    assert longest_streak_for(habit) == 0

# Tests for get_all_streaks
def test_get_all_streaks(mixed_habits):
    streaks = get_all_streaks(mixed_habits)
    names = [s[0] for s in streaks]
    assert "Exercise" in names
    assert "Jog" in names
    assert "Budget" in names
    assert all(isinstance(s[1], int) for s in streaks)

# Tests for get_habit_with_longest_streak
def test_get_habit_with_longest_streak(mixed_habits):
    result = get_habit_with_longest_streak(mixed_habits)
    assert result == ("Exercise", 5)

def test_get_habit_with_longest_streak_none():
    assert get_habit_with_longest_streak([]) is None

def test_get_habit_with_longest_streak_zero_streaks():
    h1 = Habit("Empty", "daily")
    h2 = Habit("Also Empty", "weekly")
    assert get_habit_with_longest_streak([h1, h2]) is None
