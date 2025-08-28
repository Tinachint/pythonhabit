🧠 Python Habit Tracker (CLI)

This is a command-line application for tracking habits which was built in Python using object-oriented and functional programming principles. It allows users to create, complete, and analyze daily and weekly habits directly from the terminal.

This project was developed as part of the IU course: DLBDSOOFPP01 – Object-Oriented and Functional Programming with Python.

🚀 Features

Create and manage habits with defined periodicity (daily or weekly)

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
├── cli.py # Entry point for the app
├── habit.py # Habit class (OOP)
├── tracker.py # HabitTracker class (OOP)
├── analytics.py # Functional analytics
├── database.py # SQLite storage
├── tests/  
│ └── test_habit.py # Unit tests
├── requirements.txt # Dependencies
└── README.md # You're here!

📦 Installation

Clone the repository

git clone https://github.com/Tinachint/pythonhabit.git
cd pythonhabit

Create a virtual environment

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

▶️ Running the App

Start the interactive habit tracker with the following command:

python cli.py

Example Commands

# Add a new daily habit

python cli.py add --habit "Read" --periodicity daily

# List all habits

python cli.py list

# Mark a habit as complete

python cli.py complete --habit "Read"

# View analytics

python cli.py analytics

🔍 Analytics Module

Implemented using functional programming, this module provides:

Current streak 🔥

Longest streak 🏆

Habit comparisons 📊

These insights are calculated with pure functions for reliability and clarity.

🧪 Testing

Run unit tests with:

pytest

Run the full test suite with:

pytest -v

Test Coverage Includes:

Unit Tests: Core logic for the Habit class (creation, completion, streak calculation).

Functional Tests: The pure functions in the analytics module.

Integration Tests: Data persistence and retrieval from the SQLite database.

🗃️ Predefined Habits

The app includes 5 predefined habits (daily and weekly) with 4 weeks of example tracking data. You can easily add new habits via the CLI.

🔐 Data Storage

Habit data is stored securely using SQLite, ensuring persistence across sessions.

📚 Documentation

All modules include docstrings for clarity.

Code is cleanly structured and commented for maintainability.

This README serves as the primary project documentation.

📎 License

This project is for educational purposes under IU’s portfolio guidelines.
Not intended for production use.

🔗 GitHub Repository

https://github.com/Tinachint/pythonhabit
