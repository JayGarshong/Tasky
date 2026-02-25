# app_state.py - Single source of truth for all app state
# UPDATED: Added auto-refresh tracking for main window + hidden tasks for refresh button

from datetime import datetime

class AppState:
    """Central store for all application state"""
    
    # Window states
    mini_window_active = False      # Is sidebar visible?
    stats_expanded = False          # Is statistics sidebar expanded?
    calendar_expanded = False       # Is calendar expanded?
    progress_window_active = False  # Is progress window active?
    planner_window_active = False   # Is planner window active?
    
    # Window references
    progress_frame = None           # Reference to progress window
    planner_frame = None           # Reference to planner window
    
    # Date tracking
    last_refresh_date = None       # Track last analytics refresh
    last_main_refresh_date = None  # Track last main window refresh
    
    # Task display state
    active_buttons = None          # Which task card has buttons visible
    
    # Scrolling system
    rebind_scrolling_func = None   # Reference to scroll rebind function
    
    # ===== NEW: Hidden Tasks Tracking =====
    hidden_tasks = []               # List of task IDs hidden from main view
    
    @classmethod
    def init(cls):
        """Initialize date-related state"""
        today = datetime.now().date()
        cls.last_refresh_date = today
        cls.last_main_refresh_date = today
        cls.hidden_tasks = []       # Initialize empty hidden tasks list
    
    @classmethod
    def check_main_refresh(cls):
        """Check if main window needs refresh (daily)
        
        Returns:
            bool: True if we've crossed into a new day since last check
        """
        today = datetime.now().date()
        if cls.last_main_refresh_date != today:
            cls.last_main_refresh_date = today
            return True
        return False
    
    @classmethod
    def check_analytics_refresh(cls):
        """Check if analytics need refresh (daily)
        
        Returns:
            bool: True if we've crossed into a new day since last analytics refresh
        """
        today = datetime.now().date()
        if cls.last_refresh_date != today:
            cls.last_refresh_date = today
            return True
        return False
    
    # ===== NEW: Hidden Tasks Methods =====
    @classmethod
    def hide_task(cls, task_id):
        """Add a task to hidden list"""
        if task_id not in cls.hidden_tasks:
            cls.hidden_tasks.append(task_id)
            return True
        return False
    
    @classmethod
    def unhide_task(cls, task_id):
        """Remove a task from hidden list"""
        if task_id in cls.hidden_tasks:
            cls.hidden_tasks.remove(task_id)
            return True
        return False
    
    @classmethod
    def is_task_hidden(cls, task_id):
        """Check if a task is hidden"""
        return task_id in cls.hidden_tasks
    
    @classmethod
    def hide_all_incomplete_tasks(cls, tasks):
        """Hide all incomplete tasks from a list of tasks
        Args:
            tasks: List of tasks from list_tasks() where each task has structure:
                   (id, title, description, status, category, priority, created_at, started_at, completed_at)
        """
        hidden_count = 0
        for task in tasks:
            # task[3] is status, task[0] is id
            if task[3] != "Done":  # If task is not completed
                if task[0] not in cls.hidden_tasks:
                    cls.hidden_tasks.append(task[0])
                    hidden_count += 1
        return hidden_count
    
    @classmethod
    def clear_hidden_tasks(cls):
        """Unhide all tasks"""
        count = len(cls.hidden_tasks)
        cls.hidden_tasks = []
        return count
    
    @classmethod
    def get_hidden_count(cls):
        """Get number of hidden tasks"""
        return len(cls.hidden_tasks)
    
    @classmethod
    def reset(cls):
        """Reset all state (useful for testing)"""
        cls.mini_window_active = False
        cls.stats_expanded = False
        cls.calendar_expanded = False
        cls.progress_window_active = False
        cls.planner_window_active = False
        cls.progress_frame = None
        cls.planner_frame = None
        cls.active_buttons = None
        cls.rebind_scrolling_func = None
        cls.hidden_tasks = []  # Reset hidden tasks
        cls.init()
    
    @classmethod
    def get_status(cls):
        """Get current status of all state variables (for debugging)"""
        return {
            'mini_window': cls.mini_window_active,
            'stats_expanded': cls.stats_expanded,
            'calendar_expanded': cls.calendar_expanded,
            'progress_window': cls.progress_window_active,
            'planner_window': cls.planner_window_active,
            'last_refresh': cls.last_refresh_date,
            'last_main_refresh': cls.last_main_refresh_date,
            'has_active_buttons': cls.active_buttons is not None,
            'hidden_tasks_count': len(cls.hidden_tasks),  # NEW: Show hidden count
            'hidden_tasks': cls.hidden_tasks.copy()  # NEW: Show hidden list (copy to prevent modification)
        }

# Auto-initialize when imported
AppState.init()

# ============================================================================
# GLOBAL APP CONTROL FUNCTIONS (SET BY GUI)
# ============================================================================

# These will be set by gui.py when it starts
_hide_main_content_func = None
_show_main_content_func = None
_toggle_sidebar_func = None

def set_control_functions(hide_func, show_func, toggle_func):
    """Set the control functions from gui.py
    
    Args:
        hide_func: Function to hide main content
        show_func: Function to show main content
        toggle_func: Function to toggle sidebar
    """
    global _hide_main_content_func, _show_main_content_func, _toggle_sidebar_func
    _hide_main_content_func = hide_func
    _show_main_content_func = show_func
    _toggle_sidebar_func = toggle_func
    print("[AppState] Control functions registered")

def hide_main_view():
    """Hide main task view - callable from anywhere"""
    if _hide_main_content_func:
        _hide_main_content_func()
    else:
        print("[AppState] Warning: hide_main_content function not registered")

def show_main_view():
    """Show main task view - callable from anywhere"""
    if _show_main_content_func:
        _show_main_content_func()
    else:
        print("[AppState] Warning: show_main_content function not registered")

def close_sidebar():
    """Close sidebar if open - callable from anywhere"""
    if _toggle_sidebar_func and AppState.mini_window_active:
        _toggle_sidebar_func()

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== AppState Test ===")
    print(f"Last analytics refresh: {AppState.last_refresh_date}")
    print(f"Last main refresh: {AppState.last_main_refresh_date}")
    print(f"Need main refresh? {AppState.check_main_refresh()}")
    print(f"Hidden tasks count: {AppState.get_hidden_count()}")
    print(f"Status: {AppState.get_status()}")
    print("✓ AppState ready with auto-refresh tracking and hidden tasks")