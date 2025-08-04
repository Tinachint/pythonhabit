# tracker.py

from typing import List, Optional
from habit import Habit
from habit.database import DatabaseManager


class HabitTracker:
    """
    Manages a collection of habits and provides methods to manipulate them.
    
    Responsibilitiees
    - Add, find, update, and delete habits
    - Persist habits using a database
    """

    def __init__(self, db_path: str = "habits.db"):
        """
        Initialize the tracker and load habits from the database.

        Parameters:
        
        db_path : str
            Path to the SQLite database file.
        """
        self.db = DatabaseManager(db_path)
        self.db.initialize_schema()
        self.habits: List[Habit] = self.db.load_all_habits()

    def add_habit(self, habit: Habit) -> None:
        """
        Add a new habit to the list and save it.

        Parameters:
        
        habit : Habit
            The habit to be added.
        """
        self.habits.append(habit)
        self.db.save_habit(habit)

    def delete_habit(self, name: str) -> bool:
        """
        Delete a habit by name.

        Parameters:
        
        name : str
            Name of the habit to delete.

        Returns:
        -
        bool
            True if deletion was successful, False if habit not found.
        """
        habit = self.find_habit_by_name(name)
        if habit:
            self.habits.remove(habit)
            self.db.delete_habit(name)
            return True
        return False

    def update_habit(self, old_name: str, new_name: str, new_periodicity: str) -> bool:
        """
        Update an existing habit's name and/or periodicity.

        Parameters:
        
        old_name : str
            The current name of the habit.
        new_name : str
            The new name to assign.
        new_periodicity : str
            The updated periodicity ("daily", "weekly", "monthly").

        Returns:
        
        bool
            True if update was successful, False otherwise.
        """
        habit = self.find_habit_by_name(old_name)
        if habit is None:
            return False  # Habit not found

        if new_name.lower() != old_name.lower() and self.find_habit_by_name(new_name):
            raise ValueError(f"A habit named '{new_name}' already exists.")

        habit.name = new_name
        habit.periodicity = new_periodicity.lower()
        self.db.save_habit(habit)
        return True

    def find_habit_by_name(self, name: str) -> Optional[Habit]:
        """
        Look up a habit by name.

        Parameters:
        
        name : str
            Name of the habit to look for.

        Returns:
        
        Optional[Habit]
            The matching habit, or None if not found.
        """
        return next((h for h in self.habits if h.name.lower() == name.lower()), None)

    def list_all_habits(self) -> List[Habit]:
        """
        Return all currently tracked habits.

        Returns:
        
        List[Habit]
            The list of habits.
        """
        return self.habits
