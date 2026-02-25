# tasks.py - Database operations for Tasky
# UPDATED: Added hidden column for permanent task hiding
# FIXED: Removed duplicate datetime import inside get_weekly_performance()

import sqlite3
from datetime import datetime, timedelta

DB_FILE = "tasks.db"

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def add_hidden_column_if_not_exists():
    """Add hidden column to existing tables (for upgrading old databases)"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Check if column exists
    c.execute("PRAGMA table_info(tasks)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'hidden' not in columns:
        print("[Database] Adding 'hidden' column to tasks table...")
        c.execute("ALTER TABLE tasks ADD COLUMN hidden INTEGER DEFAULT 0")
        conn.commit()
        print("[Database] Schema updated successfully")
    else:
        print("[Database] 'hidden' column already exists")
    
    conn.close()

def create_table():
    """Create tasks table with hidden column"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create table with hidden column (if not exists)
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Pending',
            category TEXT DEFAULT 'General',
            priority TEXT DEFAULT 'Medium',
            created_at TEXT,
            started_at TEXT,
            completed_at TEXT,
            hidden INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # For existing databases, add the hidden column if needed
    add_hidden_column_if_not_exists()

# ============================================================================
# CORE TASK OPERATIONS
# ============================================================================

def add_task(title, description="", category="General", priority="Medium"):
    """Add a new task (visible by default)"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    c.execute('''
        INSERT INTO tasks 
        (title, description, category, priority, status, created_at, hidden)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, category, priority, "Pending", now, 0))
    
    task_id = c.lastrowid
    conn.commit()
    conn.close()
    return task_id

def list_tasks(include_hidden=False):
    """Get tasks - by default, only visible ones (hidden=0)
    
    Args:
        include_hidden (bool): If True, returns ALL incomplete tasks including hidden ones
                              If False, returns only visible incomplete tasks (for main view)
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    if include_hidden:
        # For Unfinished tab - get ALL incomplete tasks regardless of hidden status
        c.execute('SELECT * FROM tasks WHERE status != "Done" ORDER BY id DESC')
    else:
        # For main view - only visible incomplete tasks
        c.execute('SELECT * FROM tasks WHERE status != "Done" AND hidden = 0 ORDER BY id DESC')
    
    tasks = c.fetchall()
    conn.close()
    return tasks

def list_all_tasks():
    """Get ALL tasks (including completed, including hidden) - for debugging"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM tasks ORDER BY id DESC')
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_unfinished_tasks():
    """Get ALL incomplete tasks (including hidden ones) for Unfinished tab"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM tasks WHERE status != "Done" ORDER BY id DESC')
    tasks = c.fetchall()
    conn.close()
    return tasks

def mark_done(task_id):
    """Mark task as completed and unhide it"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    # When marking done, also set hidden=0 so completed tasks reappear in main view
    c.execute('''
        UPDATE tasks 
        SET status = 'Done', completed_at = ?, hidden = 0
        WHERE id = ?
    ''', (now, task_id))
    
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Permanently delete a task"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def start_task(task_id):
    """Record when a task was started"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    c.execute('''
        UPDATE tasks 
        SET started_at = ? 
        WHERE id = ? AND started_at IS NULL
    ''', (now, task_id))
    
    conn.commit()
    conn.close()

# ============================================================================
# HIDDEN TASKS FUNCTIONS
# ============================================================================

def hide_incomplete_tasks():
    """PERMANENTLY hide all incomplete tasks from main view
    Called by refresh button
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('''
        UPDATE tasks 
        SET hidden = 1 
        WHERE status != 'Done' AND hidden = 0
    ''')
    
    affected = c.rowcount
    conn.commit()
    conn.close()
    
    print(f"[Database] Permanently hidden {affected} tasks")
    return affected

def unhide_all_tasks():
    """Show ALL tasks again (set hidden=0 for all)
    Called by "Show All Tasks" button
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute('UPDATE tasks SET hidden = 0')
    affected = c.rowcount
    
    conn.commit()
    conn.close()
    
    print(f"[Database] Unhidden {affected} tasks")
    return affected

def get_hidden_count():
    """Get number of hidden incomplete tasks"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM tasks WHERE hidden = 1 AND status != "Done"')
    count = c.fetchone()[0]
    conn.close()
    return count

def is_task_hidden(task_id):
    """Check if a specific task is hidden"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT hidden FROM tasks WHERE id = ?', (task_id,))
    result = c.fetchone()
    conn.close()
    return result and result[0] == 1

# ============================================================================
# TIME TRACKING FUNCTIONS
# ============================================================================

def get_task_duration(task):
    """Calculate duration for a task
    Task format: (id, title, description, status, category, priority, created_at, started_at, completed_at, hidden)
    """
    if task[3] != "Done" or not task[6] or not task[8]:
        return None
    
    try:
        created = datetime.fromisoformat(task[6])
        completed = datetime.fromisoformat(task[8])
        duration = (completed - created).total_seconds() / 60  # in minutes
        return duration
    except:
        return None

def format_duration(minutes):
    """Format minutes into readable string"""
    if minutes < 60:
        return f"{int(minutes)} min"
    elif minutes < 1440:  # 24 hours
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return f"{hours}h {mins}m"
    else:
        days = int(minutes // 1440)
        hours = int((minutes % 1440) // 60)
        return f"{days}d {hours}h"

# ============================================================================
# STATISTICS FUNCTIONS
# ============================================================================

def get_task_statistics():
    """Get overall task statistics"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Total tasks
    c.execute('SELECT COUNT(*) FROM tasks')
    total = c.fetchone()[0]
    
    # Completed tasks
    c.execute('SELECT COUNT(*) FROM tasks WHERE status = "Done"')
    completed = c.fetchone()[0]
    
    # Pending tasks (visible + hidden)
    c.execute('SELECT COUNT(*) FROM tasks WHERE status != "Done"')
    pending = c.fetchone()[0]
    
    # Tasks with duration data
    c.execute('SELECT COUNT(*) FROM tasks WHERE status = "Done" AND completed_at IS NOT NULL AND created_at IS NOT NULL')
    tasks_with_duration = c.fetchone()[0]
    
    # Average completion time
    if tasks_with_duration > 0:
        c.execute('''
            SELECT AVG(
                (julianday(completed_at) - julianday(created_at)) * 24 * 60
            ) FROM tasks 
            WHERE status = "Done" AND completed_at IS NOT NULL AND created_at IS NOT NULL
        ''')
        avg_time = c.fetchone()[0] or 0
    else:
        avg_time = 0
    
    conn.close()
    
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'completion_rate': completion_rate,
        'tasks_with_duration': tasks_with_duration,
        'avg_completion_time': avg_time
    }

def get_daily_performance():
    """Get today's performance stats"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    today = datetime.now().date().isoformat()
    
    # Tasks created today
    c.execute('SELECT COUNT(*) FROM tasks WHERE date(created_at) = ?', (today,))
    created = c.fetchone()[0]
    
    # Tasks completed today
    c.execute('SELECT COUNT(*) FROM tasks WHERE date(completed_at) = ?', (today,))
    completed = c.fetchone()[0]
    
    # Total time spent today
    c.execute('''
        SELECT SUM(
            (julianday(completed_at) - julianday(created_at)) * 24 * 60
        ) FROM tasks 
        WHERE date(completed_at) = ? AND completed_at IS NOT NULL AND created_at IS NOT NULL
    ''', (today,))
    total_time = c.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'total_created': created,
        'total_completed': completed,
        'total_time_minutes': total_time
    }

def get_weekly_performance():
    """Get this week's performance stats"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Get start of week (Monday)
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    start_str = start_of_week.isoformat()
    end_str = end_of_week.isoformat()
    
    # Tasks created this week
    c.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE date(created_at) BETWEEN ? AND ?
    ''', (start_str, end_str))
    created = c.fetchone()[0]
    
    # Tasks completed this week
    c.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE date(completed_at) BETWEEN ? AND ?
    ''', (start_str, end_str))
    completed = c.fetchone()[0]
    
    # Total time spent this week
    c.execute('''
        SELECT SUM(
            (julianday(completed_at) - julianday(created_at)) * 24 * 60
        ) FROM tasks 
        WHERE date(completed_at) BETWEEN ? AND ?
        AND completed_at IS NOT NULL AND created_at IS NOT NULL
    ''', (start_str, end_str))
    total_time = c.fetchone()[0] or 0
    
    # Most productive day
    c.execute('''
        SELECT date(completed_at), COUNT(*) 
        FROM tasks 
        WHERE date(completed_at) BETWEEN ? AND ?
        GROUP BY date(completed_at)
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ''', (start_str, end_str))
    result = c.fetchone()
    
    most_productive = result[0] if result else None
    if most_productive:
        # Convert to day name - FIXED: removed duplicate import
        most_productive = datetime.fromisoformat(most_productive).strftime("%A")
    
    conn.close()
    
    return {
        'total_created': created,
        'total_completed': completed,
        'total_time_minutes': total_time,
        'most_productive_day': most_productive,
        'week_start': start_of_week.strftime("%b %d"),
        'week_end': end_of_week.strftime("%b %d")
    }

def get_monthly_performance():
    """Get this month's performance stats"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    
    # Get last day of month
    if today.month == 12:
        end_of_month = today.replace(year=today.year+1, month=1, day=1) - timedelta(days=1)
    else:
        end_of_month = today.replace(month=today.month+1, day=1) - timedelta(days=1)
    
    start_str = start_of_month.isoformat()
    end_str = end_of_month.isoformat()
    
    # Tasks created this month
    c.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE date(created_at) BETWEEN ? AND ?
    ''', (start_str, end_str))
    created = c.fetchone()[0]
    
    # Tasks completed this month
    c.execute('''
        SELECT COUNT(*) FROM tasks 
        WHERE date(completed_at) BETWEEN ? AND ?
    ''', (start_str, end_str))
    completed = c.fetchone()[0]
    
    # Best week (simplified - week with most completions)
    c.execute('''
        SELECT strftime('%W', completed_at) as week_num, COUNT(*) 
        FROM tasks 
        WHERE date(completed_at) BETWEEN ? AND ?
        GROUP BY week_num
        ORDER BY COUNT(*) DESC
        LIMIT 1
    ''', (start_str, end_str))
    result = c.fetchone()
    
    best_week = f"Week {result[0]}" if result else None
    
    conn.close()
    
    completion_rate = (completed / created * 100) if created > 0 else 0
    
    return {
        'total_created': created,
        'total_completed': completed,
        'completion_rate': completion_rate,
        'best_week': best_week
    }

def get_completion_streak():
    """Get current streak of days with at least one completion"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    streak = 0
    check_date = datetime.now().date()
    
    while True:
        date_str = check_date.isoformat()
        c.execute('SELECT COUNT(*) FROM tasks WHERE date(completed_at) = ?', (date_str,))
        count = c.fetchone()[0]
        
        if count > 0:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break
    
    conn.close()
    return streak

# ============================================================================
# INITIALIZE DATABASE ON IMPORT
# ============================================================================

create_table()