from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Set, Tuple


class Habit:
    """
    Tracks a habit's completions (no duplicates per period) and calculates streaks.
    """

    def __init__(self, name: str, periodicity: str):
        """
        Parameters:
        -----------
        name : str
            The habit’s description.
        periodicity : str
            One of "daily", "weekly", or "monthly".
        """
        valid = {"daily", "weekly", "monthly"}
        periodicity = periodicity.lower()
      
        if periodicity not in valid:
            raise ValueError(f"Periodicity must be one of {valid}")

        self.name: str = name
        self.periodicity: str = periodicity
        self.creation_date: datetime = datetime.now()
        # store unique dates only (no time component)
        self._dates: Set[date] = set()

    def complete_task(self) -> date:
        """
        Record today’s date for this habit—unless already recorded
        in the same period (day/week/month).

        Returns:
        --------
        date
            The date logged (today).
        """
        today = datetime.now().date()
        if not self._is_duplicate(today):
            self._dates.add(today)
        return today

    def _is_duplicate(self, d: date) -> bool:
        """
        Check whether 'd' falls in a period already logged.

        - Daily: same calendar date
        - Weekly: same ISO year & week
        - Monthly: same year & month
        """
        if self.periodicity == "daily":
            return d in self._dates

        if self.periodicity == "weekly":
            y, w, _ = d.isocalendar()
            return any((y, w) == dd.isocalendar()[:2] for dd in self._dates)

        # monthly
        return any((d.year, d.month) == (dd.year, dd.month) for dd in self._dates)

    def get_streak(self) -> int:
        """
        Compute the current streak of consecutive periods.

        Returns:
        int
            Number of back-to-back days/weeks/months completed.
        """
        if not self._dates:
            return 0

        # Sort dates newest → oldest
        sorted_dates = sorted(self._dates, reverse=True)
        streak = 1
        prev = sorted_dates[0]

        for current in sorted_dates[1:]:
            if self.periodicity == "daily":
                expected = prev - timedelta(days=1)

            elif self.periodicity == "weekly":
                expected = prev - timedelta(weeks=1)
                ey, ew, _ = expected.isocalendar()
                cy, cw, _ = current.isocalendar()
                if (cy, cw) != (ey, ew):
                    break

            else:  # monthly
                expected = prev - relativedelta(months=1)

            if current == expected:
                streak += 1
                prev = current
            else:
                break

        return streak

    @property
    def completions(self) -> List[date]:
        """
        Return all recorded completion dates in sorted order (oldest to newest).
        This makes completion data available for external inspection and testing,
        without allowing external modification.
        """
        return sorted(self._dates)

    def __str__(self) -> str:
        return (
            f"Habit(name='{self.name}', "
            f"periodicity='{self.periodicity}', "
            f"streak={self.get_streak()}, "
            f"logged_periods={len(self._dates)})"
        )

