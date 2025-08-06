import sqlite3
from typing import List, Optional
from habit.habit import Habit
import json
from datetime import datetime


class DatabaseManager:
    """
    Handles SQLite-based persistence for habits.
    """

    def __init__(self, db_name: str = "habits.db"):
        self.db_name = db_name
        self._conn = None  # Track the connection

    def _connect(self):
        """Get a connection, reusing if possible"""
        if self._conn is None:
            self._conn = sqlite3.connect(self.db_name)
        return self._conn

    def initialize_schema(self) -> None:
        """
        Creates the habits table if it doesn't exist.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    name TEXT PRIMARY KEY,
                    periodicity TEXT NOT NULL,
                    creation_date TEXT NOT NULL,
                    completions TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_habit(self, habit: Habit) -> None:
        """
        Insert or update a habit in the database.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO habits (name, periodicity, creation_date, completions)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    periodicity=excluded.periodicity,
                    creation_date=excluded.creation_date,
                    completions=excluded.completions
            """, (
                habit.name,
                habit.periodicity,
                habit.creation_date.isoformat(),
                json.dumps([d.isoformat() for d in habit._dates])
            ))
            conn.commit()

    def load_all_habits(self) -> List[Habit]:
        """
        Load all habits from the database.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, periodicity, creation_date, completions FROM habits")
            rows = cursor.fetchall()

        habits = []
        for name, periodicity, creation_date, completions_json in rows:
            habit = Habit(name, periodicity)
            habit.creation_date = datetime.fromisoformat(creation_date)
            habit._dates = set(datetime.fromisoformat(d).date() for d in json.loads(completions_json))
            habits.append(habit)
        return habits

    def get_habit_by_name(self, name: str) -> Optional[Habit]:
        """
        Retrieve a single habit by name from the database.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, periodicity, creation_date, completions
                FROM habits
                WHERE name = ?
            """, (name,))
            row = cursor.fetchone()

        if row:
            habit = Habit(row[0], row[1])
            habit.creation_date = datetime.fromisoformat(row[2])
            habit._dates = set(datetime.fromisoformat(d).date() for d in json.loads(row[3]))
            return habit
        return None

    def delete_habit(self, name: str) -> None:
        """
        Delete a habit by name.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM habits WHERE name = ?", (name,))
            conn.commit()

    def close(self):
        """
        Close the database connection.
        """
        if self._conn is not None:
            self._conn.close()
            self._conn = None
