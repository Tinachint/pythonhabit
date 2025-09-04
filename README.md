🧠 Python Habit Tracker (CLI)

This is a command-line application for tracking habits which was built in Python using object-oriented and functional programming principles. It allows users to create, complete, and analyze daily and weekly habits directly from the terminal.

This project was developed as part of the IU course: DLBDSOOFPP01 – Object-Oriented and Functional Programming with Python.

🚀 Features

Create and manage habits with defined periodicity (daily,weekly or monthly)

Mark habits as completed

Track habit completion streaks

Analyze habits:

List all habits

Filter by periodicity

View longest streak for a single habit

View longest streak overall

Persistent storage using SQLite

Clean CLI interface

🛠️ Technology Stack
Component Description
Python 3.11 Core programming language
SQLite3 Built-in database for persistent storage
argparse CLI command parsing
Functional Programming Used in analytics module for streak calculations
Object-Oriented Design Habit and HabitTracker classes
Pytest Unit testing framework

📁 Project Structure
habit-tracker/
├── habit/
│ ├── **init**.py
│ ├── habit.py # Habit class (OOP)
│ ├── analytics.py # Functional analytics
│ ├── database.py # SQLite storage
│ ├── habit_tracker.py # HabitTracker class
│ ├── app_controller.py # CLI controller
│ └── cli.py # Entry point
├── tests/
│ ├── test_habit.py
│ ├── test_analytics.py
│ ├── test_habit_tracker.py
│ ├── test_database.py
│ ├── test_app_controller.py
│ └── test_cli.py
├── requirements.txt
└── README.md

🗃️ Predefined Habits

The app includes 5 predefined habits with 4 weeks of example tracking data:

1. **Exercise** (daily) - 30 minutes of physical activity
2. **Read** (daily) - Read 10 pages
3. **Meditate** (weekly) - 15 minutes of meditation
4. **Journal** (weekly) - Write journal entry
5. **Budget** (monthly) - Review monthly expenses

To initialize the database with these habits and sample data, run:

bash

python initialize_db.py
📦 Installation

1. Clone the repository

   bash

   git clone https://github.com/Tinachint/pythonhabit.git
   cd pythonhabit

2. Create a virtual environment

   bash

   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate

3. Install dependencies

   bash
   pip install pytest python-dateutil

▶️ Running the App

    Start the interactive habit tracker with the following command:

    bash
    python -m habit.cli

Example Commands

bash

# Add a new daily habit

python -m habit.cli --command add --habit "Read" --periodicity daily

# List all habits

python -m habit.cli --command list

# Mark a habit as complete

python -m habit.cli --command complete --habit "Read"

# View analytics

python -m habit.cli --command analytics

🔍 Analytics Module

Implemented using functional programming, this module provides:

Current streak 🔥

Longest streak 🏆

Habit comparisons 📊

These insights are calculated with pure functions for reliability and clarity.

🧪 Testing

bash

pytest

Run the full test suite with:

pytest -v

Test Coverage Includes:

Unit Tests: Core logic for the Habit class (creation, completion, streak calculation).

Functional Tests: The pure functions in the analytics module.

Integration Tests: Data persistence and retrieval from the SQLite database.

CLI interface tests

🔐 Data Storage

Habit data is stored securely using SQLite, ensuring persistence across sessions.

🔌 API Interface

The application provides a clean CLI API:

- add: Create a new habit
- complete: Mark a habit as completed
- update: Modify habit properties
- delete`: Remove a habit
- list: View all habits
- analytics: Show habit insights

All commands support both interactive and direct invocation.

📚 Documentation

All modules include docstrings for clarity.

Code is cleanly structured and commented for maintainability.

This README serves as the primary project documentation.

📎 License

This project is for educational purposes under IU’s portfolio guidelines.
Not intended for production use.

🔗 GitHub Repository

https://github.com/Tinachint/pythonhabit
