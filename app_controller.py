# app_controller.py

from habit_tracker import HabitTracker
from habit import Habit


class AppController:
    """
    Coordinates user commands and routes them to HabitTracker and supporting modules.

    Responsibilities:
    
    - Initialize the HabitTracker and set up persistence
    - Handle CLI input for adding, completing, and listing habits
    - Acts as the central control layer of the app
    """

    def __init__(self, db_path: str = "habits.db"):
        """
        Initialize the controller and backend components.

        Parameters:
        db_path : str
            The path to the SQLite database for habit persistence.
        """
        self.tracker = HabitTracker(db_path)

    def start(self) -> None:
        """
        Begin the main CLI loop, prompting user actions.
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
            elif cmd == "list":
                self.handle_list()
            elif cmd == "exit":
                print("👋 Goodbye!")
                break
            else:
                print("❓ Unknown command. Type 'help' for options.")

    def _print_help(self) -> None:
        """
        Show available commands to the user.
        """
        print("""
Available commands:
• add       – Create a new habit
• complete  – Mark a habit as completed today
• list      – View all tracked habits
• exit      – Quit the app
""")

    def handle_add(self) -> None:
        """
        Collect user input and create a new Habit.
        """
        name = input("Habit name: ").strip()
        period = input("Periodicity (daily / weekly / monthly): ").strip().lower()
        try:
            habit = Habit(name, period)
            self.tracker.add_habit(habit)
            print(f"✅ Habit '{habit.name}' added.")
        except ValueError as e:
            print(f"⚠️  {e}")

    def handle_complete(self) -> None:
        """
        Mark a user-specified habit as completed today.
        """
        name = input("Which habit did you complete? ").strip()
        habit = self.tracker.find_habit_by_name(name)
        if habit:
            today = habit.complete_task()
            self.tracker.db.save_habit(habit)
            print(f"✔ '{habit.name}' completed for {today}. Streak: {habit.get_streak()}")
        else:
            print("🚫 Habit not found.")

    def handle_list(self) -> None:
        """
        Display all tracked habit names and their streaks.
        """
        if not self.tracker.habits:
            print("📭 No habits tracked yet.")
        else:
            print("📌 Current Habits:")
            for h in self.tracker.habits:
                print(f"– {h.name} ({h.periodicity}) ➝ Streak: {h.get_streak()}")
