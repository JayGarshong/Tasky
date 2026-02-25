# backup.py - Automatic database backup system with CLI tools
# Place this file in the same folder as tasks.db

import shutil
import os
from datetime import datetime, timedelta
import sqlite3

# ============================================================================
# CONFIGURATION
# ============================================================================

BACKUP_DIR = "backups"
DB_FILE = "tasks.db"
MAX_BACKUP_DAYS = 7

# ============================================================================
# CORE BACKUP FUNCTIONS
# ============================================================================

def ensure_backup_dir():
    """Create backup directory if it doesn't exist"""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"[Backup] Created directory: {BACKUP_DIR}")

def get_backup_filename():
    """Generate backup filename with current date"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    return f"tasks_backup_{date_str}.db"

def create_backup():
    """Copy current database to backup folder"""
    ensure_backup_dir()
    
    # Check if database exists
    if not os.path.exists(DB_FILE):
        print(f"[Backup] No database file found at {DB_FILE}")
        return False
    
    backup_path = os.path.join(BACKUP_DIR, get_backup_filename())
    
    # Don't overwrite today's backup if it already exists
    if os.path.exists(backup_path):
        print(f"[Backup] Today's backup already exists: {backup_path}")
        return True
    
    try:
        # Quick verification that database is not corrupted
        conn = sqlite3.connect(DB_FILE)
        conn.execute("SELECT COUNT(*) FROM tasks")
        conn.close()
        
        # Copy the file
        shutil.copy2(DB_FILE, backup_path)
        print(f"[Backup] Created: {backup_path}")
        
        # Clean old backups
        clean_old_backups()
        
        return True
    except Exception as e:
        print(f"[Backup] Failed: {e}")
        return False

def clean_old_backups():
    """Remove backups older than MAX_BACKUP_DAYS"""
    ensure_backup_dir()
    
    cutoff_date = datetime.now() - timedelta(days=MAX_BACKUP_DAYS)
    removed_count = 0
    
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith("tasks_backup_") and filename.endswith(".db"):
            filepath = os.path.join(BACKUP_DIR, filename)
            
            try:
                # Extract date from filename (tasks_backup_2026-02-12.db)
                date_str = filename.replace("tasks_backup_", "").replace(".db", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                
                if file_date < cutoff_date:
                    os.remove(filepath)
                    removed_count += 1
                    print(f"[Backup] Removed old: {filename}")
            except Exception as e:
                # If filename doesn't match pattern, leave it alone
                pass
    
    if removed_count > 0:
        print(f"[Backup] Cleaned {removed_count} old backup(s)")

def list_backups():
    """Return list of available backups with dates"""
    ensure_backup_dir()
    
    backups = []
    for filename in os.listdir(BACKUP_DIR):
        if filename.startswith("tasks_backup_") and filename.endswith(".db"):
            filepath = os.path.join(BACKUP_DIR, filename)
            
            # Extract date from filename
            date_str = filename.replace("tasks_backup_", "").replace(".db", "")
            
            backups.append({
                'filename': filename,
                'path': filepath,
                'date': date_str
            })
    
    # Sort by date, newest first
    backups.sort(key=lambda x: x['date'], reverse=True)
    return backups

def get_latest_backup_date():
    """Return the date of the most recent backup as string"""
    backups = list_backups()
    if backups:
        return backups[0]['date']
    return None

def restore_backup(backup_filename):
    """Restore database from a backup file"""
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    if not os.path.exists(backup_path):
        print(f"[Restore] Backup file not found: {backup_path}")
        return False
    
    try:
        # Create backup of current db before restoring (just in case)
        if os.path.exists(DB_FILE):
            emergency_backup = f"{DB_FILE}.before_restore"
            shutil.copy2(DB_FILE, emergency_backup)
            print(f"[Restore] Current database backed up to: {emergency_backup}")
        
        # Restore from backup
        shutil.copy2(backup_path, DB_FILE)
        print(f"[Restore] Successfully restored from: {backup_filename}")
        return True
    except Exception as e:
        print(f"[Restore] Failed: {e}")
        return False

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("\n=== 📀 BACKUP SYSTEM ===")
        print("Commands:")
        print("  python backup.py list        - Show all backups")
        print("  python backup.py backup      - Create manual backup")
        print("  python backup.py restore     - Restore from latest backup")
        print("  python backup.py restore YYYY-MM-DD - Restore specific date")
        print("\nExamples:")
        print("  python backup.py list")
        print("  python backup.py restore 2026-02-11")
        print("=" * 50)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "list":
        backups = list_backups()
        if not backups:
            print("\n❌ No backups found.")
        else:
            print(f"\n📀 Available backups ({len(backups)}):")
            print("=" * 50)
            for b in backups:
                print(f"  {b['date']}  -  {b['filename']}")
            print("=" * 50)
    
    elif command == "backup":
        print("\n📀 Creating manual backup...")
        create_backup()
    
    elif command == "restore":
        if len(sys.argv) > 2:
            # Restore specific date
            date_str = sys.argv[2]
            filename = f"tasks_backup_{date_str}.db"
            print(f"\n⚠️  Attempting to restore from: {date_str}")
        else:
            # Restore latest
            backups = list_backups()
            if backups:
                filename = backups[0]['filename']
                date_str = backups[0]['date']
                print(f"\n⚠️  Attempting to restore from latest: {date_str}")
            else:
                print("\n❌ No backups to restore.")
                sys.exit(1)
        
        confirm = input(f"\n⚠️  Restore database from {date_str}? (yes/no): ")
        if confirm.lower() == "yes":
            restore_backup(filename)
        else:
            print("❌ Restore cancelled.")
    
    else:
        print(f"\n❌ Unknown command: {command}")
        print("Run 'python backup.py' for help.")