# planner_db.py - Database operations for plans
import sqlite3
from datetime import datetime

DB_FILE = "tasks.db"  # Same database, new table

def init_planner_table():
    """Create plans table if it doesn't exist"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            heading TEXT NOT NULL,
            description TEXT,
            focus_area TEXT DEFAULT 'General',
            priority TEXT DEFAULT 'Medium',
            time_frame TEXT NOT NULL,  -- 'Week' or 'Month'
            created_at TEXT,
            updated_at TEXT,
            status TEXT DEFAULT 'Active'
        )
    ''')
    conn.commit()
    conn.close()

def add_plan(heading, description, focus_area, priority, time_frame):
    """Add a new plan"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    c.execute('''
        INSERT INTO plans 
        (heading, description, focus_area, priority, time_frame, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (heading, description, focus_area, priority, time_frame, now, now))
    
    plan_id = c.lastrowid
    conn.commit()
    conn.close()
    return plan_id

def list_plans(time_frame=None):
    """Get all plans, optionally filtered by Week/Month"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    if time_frame:
        c.execute('SELECT * FROM plans WHERE time_frame = ? ORDER BY id DESC', (time_frame,))
    else:
        c.execute('SELECT * FROM plans ORDER BY id DESC')
    
    plans = c.fetchall()
    conn.close()
    return plans

def update_plan(plan_id, heading, description, focus_area, priority, time_frame):
    """Update an existing plan"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    c.execute('''
        UPDATE plans 
        SET heading = ?, description = ?, focus_area = ?, 
            priority = ?, time_frame = ?, updated_at = ?
        WHERE id = ?
    ''', (heading, description, focus_area, priority, time_frame, now, plan_id))
    
    conn.commit()
    conn.close()
    return True

def delete_plan(plan_id):
    """Delete a plan"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM plans WHERE id = ?', (plan_id,))
    conn.commit()
    conn.close()
    return True

# ============================================================================
# INITIALIZE ON IMPORT
# ============================================================================

init_planner_table()