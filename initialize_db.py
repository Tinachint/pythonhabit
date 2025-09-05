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
    """Create sample habits with 4 weeks of completion data."""
    print("Initializing database with sample data...")
    
    # Initialize database
    db = DatabaseManager("habits.db")
    db.initialize_schema()
    
    # Clear any existing data
    db.close()
    os.remove("habits.db") if os.path.exists("habits.db") else None
    db = DatabaseManager("habits.db")
    db.initialize_schema()
    
    habits = []
    
    # Create the 5 predefined habits
    exercise = Habit("Exercise", "daily")
    read = Habit("Read", "daily")
    meditate = Habit("Meditate", "weekly")
    journal = Habit("Journal", "weekly")
    budget = Habit("Budget", "monthly")
    
    habits = [exercise, read, meditate, journal, budget]
    
    # Add completion data for the last 4 weeks
    today = date.today()
    
    for habit in habits:
        if habit.periodicity == "daily":
            # Add completions for the last 28 days (with some realistic gaps)
            for i in range(28):
                # Skip some days to make it realistic (not every single day)
                if i % 7 != 0:  # Skip one day per week
                    completion_date = today - timedelta(days=i)
                    habit._dates.add(completion_date)
        
        elif habit.periodicity == "weekly":
            # Add completions for the last 4 weeks
            for i in range(4):
                completion_date = today - timedelta(weeks=i)
                # Add some variation (not exactly every 7 days)
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
    create_sample_data()