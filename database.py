# database.py

import sqlite3
import os

# Database file name
DB_NAME = "todo.db"

# ----------------------------
# Return a connection to the database
# ----------------------------
def get_connection():
    """Return a SQLite database connection."""
    return sqlite3.connect(DB_NAME)

# ----------------------------
# Create tasks table if it doesn't exist
# ----------------------------
def create_table():
    """Initialize the database and create the tasks table if it doesn't exist."""
    # Ensure the database file exists in the current folder
    if not os.path.exists(DB_NAME):
        open(DB_NAME, 'w').close()
        
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ----------------------------
# Optional: Initialize the database when this file is run directly
# ----------------------------
if __name__ == "__main__":
    create_table()
    print("Database initialized and tasks table ready.")
