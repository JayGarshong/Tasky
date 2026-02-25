import sys
from database import create_table
from tasks import add_task, list_tasks
from backup import create_backup  # ← NEW: Import backup function

def main():
    # ===== NEW: Create backup when app starts =====
    print("Tasky starting...")
    create_backup()
    # ==============================================
    
    create_table()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py add \"Task title\" [Description]")
        print("  python main.py list")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Please provide a task title.")
            return
        title = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        add_task(title, description)
        print(f"Task '{title}' added successfully.")

    elif command == "list":
        tasks = list_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            print("Here are your tasks:")
            for task in tasks:
                print(f"ID: {task[0]} | Title: {task[1]} | Description: {task[2]} | Status: {task[3]}")

    else:
        print(f"Unknown command '{command}'")

if __name__ == "__main__":
    main()