 🧠 Habit Tracker (Python CLI)

This is a command-line habit tracking application built with Python using object-oriented and functional programming principles.  
It allows users to create, complete, and analyze daily and weekly habits.  

This project was developed as part of the IU course:  
**DLBDSOOFPP01 – Object-Oriented and Functional Programming with Python**.

🚀 Features

- Create and manage habits with defined periodicity (daily or weekly)
- Mark habits as completed
- Track habit completion streaks
- Analyze habits:
  - List all habits
  - Filter by periodicity
  - View longest streak for a single habit
  - View longest streak overall
- Persistent storage using SQLite
- Clean CLI interface

🛠️ Technology Stack

- Python 3.11
- SQLite3(built-in)
- Click (for CLI – optional)
- Pytest (for unit testing)

📁 Project Structure

plaintext
habit-tracker/
├── cli.py              Entry point for the app
├── habit.py            Habit class
├── tracker.py          HabitTracker class
├── analytics.py        Functional analytics
├── database.py         SQLite storage
├── tests/
│   └── test_habit.py   Unit tests
├── README.md           You're here!
├── requirements.txt    Dependencies
└── .gitignore          Files/folders to exclude from Git
