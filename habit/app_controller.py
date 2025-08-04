# app_controller.py

from typing import Optional
from habit.habit_tracker import HabitTracker
from habit import Habit


class AppController:
    def __init__(self, db_path: str = "habits.db"):
        self.tracker = HabitTracker(db_path)

    def start(self) -> None:
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
        habit_name = habit_name or input("Which habit did you complete? ").strip()
        habit = self.tracker.find_habit_by_name(habit_name)
        if habit:
            today = habit.complete_task()
            self.tracker.db.save_habit(habit)
            print(f"✔ '{habit.name}' completed for {today}. Streak: {habit.get_streak()}")
        else:
            print("🚫 Habit not found.")

    def handle_update(self, name: Optional[str] = None, new_periodicity: Optional[str] = None) -> None:
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
        name = name or input("Habit to delete: ").strip()
        success = self.tracker.delete_habit(name)
        if success:
            print(f"🗑️ Habit '{name}' deleted.")
        else:
            print("🚫 Habit not found.")

    def handle_list(self, periodicity: Optional[str] = None) -> None:
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


    
