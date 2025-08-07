from typing import Optional
from habit.habit_tracker import HabitTracker
from habit.habit import Habit

class AppController:
    """
    Coordinates user interaction and habit tracking operations.
    Acts as the main interface between CLI input and backend logic.
    """

    def __init__(self, db_path: str = "habits.db"):
        """
        Initialize the controller with a HabitTracker instance.

        Parameters:
        -----------
        db_path : str
            Path to the database file for storing habits.
        """
        self.tracker = HabitTracker(db_path)

    def start(self) -> None:
        """
        Launch the interactive CLI loop for user commands.
        """
        print("📊 Habit Tracker App (type 'help' for options)")
        while True:
            cmd = input(">> ").strip().lower()
            if cmd == "help":
                self._print_help()
            elif cmd == "add":
                self.handle_add()
            elif cmd == "complete":
                self.handle_complete()
            elif cmd == "update":
                self.handle_update()
            elif cmd == "delete":
                self.handle_delete()
            elif cmd == "list":
                self.handle_list()
            elif cmd == "exit":
                print("👋 Goodbye!")
                break
            else:
                print("❓ Unknown command. Type 'help' for options.")

    def _print_help(self) -> None:
        """
        Display available commands and their descriptions.
        """
        print("""
Available commands:
• add       – Create a new habit
• complete  – Mark a habit as completed today
• update    – Change periodicity of a habit
• delete    – Remove a habit
• list      – View all tracked habits
• help      – Show this help menu
• exit      – Quit the app
""")

    def handle_add(self, name: Optional[str] = None, periodicity: Optional[str] = None) -> None:
        """
        Add a new habit to the tracker.

        Parameters:
        -----------
        name : Optional[str]
            Name of the habit. If not provided, prompts the user.
        periodicity : Optional[str]
            Frequency of the habit (daily/weekly/monthly). If not provided, prompts the user.
        """
        name = name or input("Habit name: ").strip()
        periodicity = periodicity or input("Periodicity (daily/weekly/monthly): ").strip().lower()

        if not name or not periodicity:
            print("❗ Missing habit name or periodicity.")
            return

        try:
            habit = Habit(name, periodicity)
            self.tracker.add_habit(habit)
            print(f"✅ Habit '{habit.name}' added.")
        except ValueError as e:
            print(f"⚠️ {e}")

    def handle_complete(self, habit_name: Optional[str] = None) -> None:
        """
        Mark a habit as completed for today.

        Parameters:
        -----------
        habit_name : Optional[str]
            Name of the habit to complete. If not provided, prompts the user.
        """
        habit_name = habit_name or input("Which habit did you complete? ").strip()
        habit = self.tracker.find_habit_by_name(habit_name)
        if habit:
            today = habit.complete_task()
            self.tracker.db.save_habit(habit)
            print(f"✔ '{habit.name}' completed for {today}. Streak: {habit.get_streak()}")
        else:
            print("🚫 Habit not found.")

    def handle_update(self, name: Optional[str] = None, new_periodicity: Optional[str] = None) -> None:
        """
        Update the periodicity of an existing habit.

        Parameters:
        -----------
        name : Optional[str]
            Name of the habit to update. If not provided, prompts the user.
        new_periodicity : Optional[str]
            New frequency (daily/weekly/monthly). If not provided, prompts the user.
        """
        name = name or input("Habit to update: ").strip()
        new_periodicity = new_periodicity or input("New periodicity (daily/weekly/monthly): ").strip().lower()

        if not name or not new_periodicity:
            print("❗ Missing required fields.")
            return

        habit = self.tracker.find_habit_by_name(name)
        if not habit:
            print(f"🚫 Habit '{name}' not found.")
            return

        try:
            success = self.tracker.update_habit(name, name, new_periodicity)
            if success:
                print(f"🔄 Habit '{name}' updated to periodicity: {new_periodicity}")
        except ValueError as e:
            print(f"⚠️ {e}")

    def handle_delete(self, name: Optional[str] = None) -> None:
        """
        Delete a habit from the tracker.

        Parameters:
        -----------
        name : Optional[str]
            Name of the habit to delete. If not provided, prompts the user.
        """
        name = name or input("Habit to delete: ").strip()
        success = self.tracker.delete_habit(name)
        if success:
            print(f"🗑️ Habit '{name}' deleted.")
        else:
            print("🚫 Habit not found.")

    def handle_list(self, periodicity: Optional[str] = None) -> None:
        """
        List all tracked habits, optionally filtered by periodicity.

        Parameters:
        -----------
        periodicity : Optional[str]
            Filter habits by frequency (daily/weekly/monthly).
        """
        habits = self.tracker.habits
        if periodicity:
            habits = [h for h in habits if h.periodicity == periodicity]

        if not habits:
            print("📭 No habits found.")
            return

        print("📌 Current Habits:")
        for h in habits:
            print(f"– {h.name} ({h.periodicity}) ➝ Streak: {h.get_streak()}")

    def handle_command(self, cmd: str, habit_name: Optional[str] = None, periodicity: Optional[str] = None) -> None:
        """
        Dispatch a command to the appropriate handler.

        Parameters:
        -----------
        cmd : str
            The command to execute (e.g., 'add', 'list', 'complete').
        habit_name : Optional[str]
            Name of the habit (used by some commands).
        periodicity : Optional[str]
            Frequency of the habit (used by some commands).
        """
        if cmd == "add":
            self.handle_add(habit_name, periodicity)
        elif cmd == "complete":
            self.handle_complete(habit_name)
        elif cmd == "update":
            self.handle_update(habit_name, periodicity)
        elif cmd == "delete":
            self.handle_delete(habit_name)
        elif cmd == "list":
            self.handle_list(periodicity)
        elif cmd == "help":
            self._print_help()
        elif cmd == "exit":
            print("👋 Exiting.")
        else:
            print("❓ Unknown command. Type 'help' for options.")


    
