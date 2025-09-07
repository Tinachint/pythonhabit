#!/usr/bin/env python3
"""
Database initialization script for habit tracker.
Creates 5 predefined habits with 4 weeks of sample data.
This script should be run once to initialize the database with sample data.
"""

import sys
import os
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

# Add the habit package to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from habit.database import DatabaseManager
from habit.habit import Habit


def create_sample_data():
    """
    Create sample habits with 4 weeks of completion data.
    
    This function:
    1. Creates a fresh SQLite database
    2. Defines 5 habits with different periodicities
    3. Adds realistic completion data for the past 4 weeks
    4. Saves all habits to the database
    5. Provides feedback on the created data
    
    Returns:
        None
    """
    print("Initializing database with sample data...")
    
    # Remove existing database to start fresh
    if os.path.exists("habits.db"):
        os.remove("habits.db")
        print("Removed existing database file.")
    
    # Initialize database
    db = DatabaseManager("habits.db")
    db.initialize_schema()
    
    # Create the 5 predefined habits with different periodicities
    habits = [
        Habit("Exercise", "daily"),
        Habit("Read", "daily"),
        Habit("Meditate", "weekly"),
        Habit("Journal", "weekly"),
        Habit("Budget", "monthly")
    ]
    
    # Add completion data for the last 4 weeks
    today = date.today()
    
    for habit in habits:
        if habit.periodicity == "daily":
            # Add completions for the last 28 days (with realistic gaps)
            for i in range(28):
                # Skip one day per week to make it realistic
                if i % 7 != 0:
                    completion_date = today - timedelta(days=i)
                    habit._dates.add(completion_date)
        
        elif habit.periodicity == "weekly":
            # Add completions for the last 4 weeks
            for i in range(4):
                completion_date = today - timedelta(weeks=i)
                # Add slight variation to weekly dates
                if i > 0:
                    completion_date = completion_date - timedelta(days=1 if i % 2 == 0 else 0)
                habit._dates.add(completion_date)
                
        elif habit.periodicity == "monthly":
            # Add completions for the last 4 months
            for i in range(4):
                completion_date = today - relativedelta(months=i)
                habit._dates.add(completion_date)
        
        # Save to database
        db.save_habit(habit)
        print(f"✓ Added {habit.name} ({habit.periodicity}) with {len(habit._dates)} completions")
    
    db.close()
    print("\n✅ Database initialized with sample data!")
    print("Sample habits created:")
    for habit in habits:
        print(f"  - {habit.name} ({habit.periodicity}): {len(habit._dates)} completions")
    print("\nYou can now run the application with: python -m habit.cli")


if __name__ == "__main__":
    """
    Main execution point for the initialization script.
    
    When run directly, this script will:
    1. Create a new SQLite database file (habits.db)
    2. Populate it with 5 predefined habits
    3. Add 4 weeks of sample completion data
    4. Print a summary of the created data
    """
    create_sample_data()