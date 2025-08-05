from typing import List, Optional, Tuple
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from habit.habit import Habit

def filter_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """Return habits matching the given periodicity (case-insensitive)."""
    return [h for h in habits if h.periodicity == periodicity.lower()]

def longest_streak_for(habit: Habit) -> int:
    """Calculate the longest historical streak for a habit."""
    if not habit.completions:
        return 0

    sorted_dates = sorted([c.date() for c in habit.completions])
    max_streak = streak = 1
    previous = sorted_dates[0]

    for current in sorted_dates[1:]:
        if habit.periodicity == "daily":
            expected = previous + timedelta(days=1)
        elif habit.periodicity == "weekly":
            expected = previous + timedelta(weeks=1)
        else:  # monthly
            expected = previous + relativedelta(months=1)

        if current == expected:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1
        previous = current

    return max_streak

def get_all_streaks(habits: List[Habit]) -> List[Tuple[str, int]]:
    """Return (habit_name, current_streak) pairs for all habits."""
    return [(h.name, h.get_streak()) for h in habits]

def get_habit_with_longest_streak(habits: List[Habit]) -> Optional[Tuple[str, int]]:
    """Return the habit with the longest historical streak (ignoring 0-streaks)."""
    if not habits:
        return None
    streaks = [(h.name, longest_streak_for(h)) for h in habits]
    max_streak = max(streaks, key=lambda pair: pair[1])
    return max_streak if max_streak[1] > 0 else None