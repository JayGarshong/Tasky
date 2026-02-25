# Tasky - Main GUI Interface
# Professional Task Manager with Clean UI
# CLEANED VERSION - Unfinished tab removed

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tasks import add_task, list_tasks, mark_done, delete_task, start_task, get_task_duration, format_duration, get_task_statistics, get_daily_performance, get_weekly_performance, get_monthly_performance, get_completion_streak, get_hidden_count
import tkinter.font as tkFont
from datetime import datetime, date
from app_state import AppState, set_control_functions
from planner_window import PlannerWindow

# ============================================================================
# MAIN WINDOW SETUP - Professional clean layout
# ============================================================================

root = tk.Tk()
root.title("Tasky")
root.geometry("900x600")
root.minsize(800, 520)

# Remove ALL internal padding from root window
root.grid_rowconfigure(0, weight=0)  # Header row
root.grid_rowconfigure(1, weight=1)  # Content row
root.grid_columnconfigure(0, weight=1)

# Clean background with no borders
BG_COLOR = "#f0f2f5"  # Softer, more professional background
root.configure(bg=BG_COLOR, bd=0, highlightthickness=0)

# ============================================================================
# PROFESSIONAL COLOR PALETTE
# ============================================================================

HEADER_BG = "#1e2b3a"      # Dark slate blue - professional and calm
HEADER_FG = "#ffffff"      # White text
TASK_BG = "#ffffff"        # White cards
TASK_DONE_CHECK = "#27ae60"  # Green checkmark

# Button colors - refined palette
BTN_DONE = "#3498db"       # Blue
BTN_DELETE = "#e74c3c"     # Red
BTN_START = "#2c3e50"      # Dark slate

# Text colors - better contrast
TEXT_PRIMARY = "#2c3e50"    # Dark slate for main text
TEXT_SECONDARY = "#5d6d7e"  # Softer for secondary text
TEXT_LIGHT = "#7f8c8d"      # Light for hints
TEXT_WHITE = "#ffffff"      # White text

# Accent colors
ACCENT_BLUE = "#3498db"
ACCENT_GREEN = "#27ae60"
ACCENT_ORANGE = "#f39c12"
ACCENT_RED = "#e74c3c"
ACCENT_PURPLE = "#9b59b6"

# Font definitions - clean and modern
header_font = tkFont.Font(family="Segoe UI", size=24, weight="bold")
myday_font = tkFont.Font(family="Segoe UI", size=20, weight="normal")
title_font = tkFont.Font(family="Segoe UI", size=14, weight="bold")
desc_font = tkFont.Font(family="Segoe UI", size=12)
button_font = tkFont.Font(family="Segoe UI", size=11, weight="bold")
small_font = tkFont.Font(family="Segoe UI", size=10)
calendar_font = tkFont.Font(family="Segoe UI", size=10)
calendar_header_font = tkFont.Font(family="Segoe UI", size=11, weight="bold")

# ============================================================================
# LAYOUT CONSTANTS
# ============================================================================

SIDEBAR_WIDTH = 320
CONTENT_SHIFT = SIDEBAR_WIDTH + 10

# ============================================================================
# TASK MANAGEMENT FUNCTIONS
# ============================================================================

def mark_done_gui(task_id):
    mark_done(task_id)
    refresh_tasks()

def delete_task_gui(task_id):
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
        delete_task(task_id)
        refresh_tasks()

def start_task_gui(task_id):
    start_task(task_id)
    refresh_tasks()
    messagebox.showinfo("Task Started", "Timer started for this task!")

def add_task_gui():
    """Professional add task dialog"""
    dialog = tk.Toplevel(root)
    dialog.title("Add New Task")
    dialog.geometry("450x380")
    dialog.configure(bg=TASK_BG)
    dialog.transient(root)
    dialog.grab_set()
    
    # Center on parent
    dialog.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() // 2) - (450 // 2)
    y = root.winfo_y() + (root.winfo_height() // 2) - (380 // 2)
    dialog.geometry(f"+{x}+{y}")
    
    # Header
    header_frame = tk.Frame(dialog, bg=HEADER_BG, height=50)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    tk.Label(
        header_frame,
        text="✨ Create New Task",
        font=("Segoe UI", 14, "bold"),
        bg=HEADER_BG,
        fg=TEXT_WHITE
    ).pack(pady=12)
    
    # Content
    content = tk.Frame(dialog, bg=TASK_BG, padx=25, pady=20)
    content.pack(fill="both", expand=True)
    
    # Title field
    tk.Label(
        content,
        text="Task Title",
        font=("Segoe UI", 11, "bold"),
        bg=TASK_BG,
        fg=TEXT_PRIMARY,
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    title_entry = tk.Entry(
        content,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid",
        highlightthickness=1,
        highlightcolor="#bdc3c7"
    )
    title_entry.pack(fill="x", pady=(0, 15))
    title_entry.focus_set()
    
    # Description field
    tk.Label(
        content,
        text="Description (optional)",
        font=("Segoe UI", 11),
        bg=TASK_BG,
        fg=TEXT_PRIMARY,
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    desc_entry = tk.Entry(
        content,
        font=("Segoe UI", 11),
        bd=1,
        relief="solid"
    )
    desc_entry.pack(fill="x", pady=(0, 15))
    
    # Category and Priority row
    row_frame = tk.Frame(content, bg=TASK_BG)
    row_frame.pack(fill="x", pady=(0, 20))
    
    # Category
    left_col = tk.Frame(row_frame, bg=TASK_BG)
    left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    tk.Label(
        left_col,
        text="Category",
        font=("Segoe UI", 11),
        bg=TASK_BG,
        fg=TEXT_PRIMARY,
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    category_var = tk.StringVar(value="General")
    categories = ["General", "Work", "Personal", "Health", "Study", "Home", "Finance"]
    
    category_combo = ttk.Combobox(
        left_col,
        textvariable=category_var,
        values=categories,
        font=("Segoe UI", 10),
        state="readonly"
    )
    category_combo.pack(fill="x")
    
    # Priority
    right_col = tk.Frame(row_frame, bg=TASK_BG)
    right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    tk.Label(
        right_col,
        text="Priority",
        font=("Segoe UI", 11),
        bg=TASK_BG,
        fg=TEXT_PRIMARY,
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    priority_var = tk.StringVar(value="Medium")
    priority_combo = ttk.Combobox(
        right_col,
        textvariable=priority_var,
        values=["High", "Medium", "Low"],
        font=("Segoe UI", 10),
        state="readonly"
    )
    priority_combo.pack(fill="x")
    
    # Buttons
    button_frame = tk.Frame(content, bg=TASK_BG)
    button_frame.pack(fill="x", pady=(10, 0))
    
    def submit():
        title = title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Task title is required!", parent=dialog)
            return
        
        description = desc_entry.get().strip()
        add_task(title, description, category_var.get(), priority_var.get())
        refresh_tasks()
        dialog.destroy()
    
    def cancel():
        dialog.destroy()
    
    tk.Button(
        button_frame,
        text="Create Task",
        font=button_font,
        bg=ACCENT_GREEN,
        fg=TEXT_WHITE,
        bd=0,
        padx=20,
        pady=8,
        activebackground="#229954",
        cursor="hand2",
        command=submit
    ).pack(side="left", padx=(0, 10))
    
    tk.Button(
        button_frame,
        text="Cancel",
        font=button_font,
        bg="#ecf0f1",
        fg=TEXT_SECONDARY,
        bd=0,
        padx=20,
        pady=8,
        activebackground="#d5dbdb",
        cursor="hand2",
        command=cancel
    ).pack(side="left")
    
    dialog.bind('<Return>', lambda e: submit())
    dialog.bind('<Escape>', lambda e: cancel())
    root.wait_window(dialog)

# ===== MANUAL REFRESH  =====
def manual_refresh():
    """Permanently hide incomplete tasks from main view"""
    print("[Manual Refresh] Hiding incomplete tasks permanently...")
    
    # Hide tasks in database
    from tasks import hide_incomplete_tasks
    hidden_count = hide_incomplete_tasks()
    
    # Clear main view
    for widget in task_container.winfo_children():
        widget.destroy()
    AppState.active_buttons = None
    
    # Show empty state message
    if hidden_count > 0:
        show_empty_main_message(
            "✨ Tasks hidden", 
            f"{hidden_count} tasks hidden - use 'Show All' to restore"
        )
    else:
        show_empty_main_message(
            "✨ All caught up!", 
            "No incomplete tasks to hide"
        )
    
    # Show visual feedback
    show_refresh_feedback()

def unhide_all_tasks():
    """Show all tasks again (reset hidden status)"""
    from tasks import unhide_all_tasks, get_hidden_count
    
    hidden_count = get_hidden_count()
    
    if hidden_count == 0:
        messagebox.showinfo("No Hidden Tasks", "There are no hidden tasks to show.")
        return
    
    if messagebox.askyesno(
        "Show All Tasks",
        f"This will show {hidden_count} hidden tasks on the main page. Continue?"
    ):
        unhide_all_tasks()
        refresh_tasks()
        
        # Show feedback
        feedback = tk.Toplevel(root)
        feedback.overrideredirect(True)
        feedback.configure(bg=ACCENT_BLUE)
        
        x = root.winfo_rootx() + root.winfo_width() - 200
        y = root.winfo_rooty() + 80
        feedback.geometry(f"150x30+{x}+{y}")
        
        label = tk.Label(
            feedback,
            text=f"✓ {hidden_count} tasks restored",
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT_BLUE,
            fg="white"
        )
        label.pack(expand=True, fill="both")
        
        feedback.after(1500, feedback.destroy)

def show_empty_main_message(title="✨ All tasks hidden", subtitle="Click 'Show All Tasks' to restore"):
    """Show a message when main page is empty
    Args:
        title: Main message to display
        subtitle: Secondary instruction message
    """
    from tasks import get_hidden_count
    
    empty_frame = tk.Frame(task_container, bg=BG_COLOR)
    empty_frame.pack(fill="both", expand=True, pady=100)
    
    # Icon (different based on context)
    if "hidden" in title.lower():
        icon = "🗂️"
    elif "no tasks" in title.lower():
        icon = "📝"
    else:
        icon = "✨"
    
    tk.Label(
        empty_frame,
        text=icon,
        font=("Segoe UI", 48),
        bg=BG_COLOR,
        fg=TEXT_LIGHT
    ).pack()
    
    # Title
    tk.Label(
        empty_frame,
        text=title,
        font=("Segoe UI", 16, "bold"),
        bg=BG_COLOR,
        fg=TEXT_PRIMARY
    ).pack(pady=(10, 5))
    
    # Subtitle
    tk.Label(
        empty_frame,
        text=subtitle,
        font=("Segoe UI", 12),
        bg=BG_COLOR,
        fg=TEXT_SECONDARY
    ).pack()
    
    # Optional: Add "Show All Tasks" button if there are hidden tasks
    if get_hidden_count() > 0:
        show_btn = tk.Button(
            empty_frame,
            text="Show All Tasks",
            font=button_font,
            bg=ACCENT_BLUE,
            fg=TEXT_WHITE,
            bd=0,
            padx=20,
            pady=8,
            activebackground="#2980b9",
            cursor="hand2",
            command=unhide_all_tasks
        )
        show_btn.pack(pady=(20, 0))

def show_refresh_feedback():
    """Show a quick feedback that refresh happened"""
    # Create a small popup near the refresh button
    feedback = tk.Toplevel(root)
    feedback.overrideredirect(True)  # Remove window decorations
    feedback.configure(bg="#27ae60")
    
    # Position near the refresh button
    x = root.winfo_rootx() + root.winfo_width() - 150
    y = root.winfo_rooty() + 80
    feedback.geometry(f"120x30+{x}+{y}")
    
    # Add message
    label = tk.Label(
        feedback,
        text="✓ Page Cleared!",
        font=("Segoe UI", 10, "bold"),
        bg="#27ae60",
        fg="white"
    )
    label.pack(expand=True, fill="both")
    
    # Auto-close after 1.5 seconds
    feedback.after(1500, feedback.destroy)
# ======================================
   
# ============================================================================
# MAIN INTERFACE HEADER - Now touches top edge
# ============================================================================

# Header frame with zero top margin
header = tk.Frame(root, bg=HEADER_BG, height=70)
header.grid(row=0, column=0, sticky="ew", pady=0)
header.grid_propagate(False)

main_container = tk.Frame(root, bg=BG_COLOR)
main_container.grid(row=1, column=0, sticky="nsew", pady=0)

# ============================================================================
# SIDEBAR TOGGLE
# ============================================================================

def toggle_mini_window():
    """Open or close sidebar with professional animation feel"""
    if AppState.planner_window_active or AppState.progress_window_active:
        return
    
    if mini_frame.winfo_ismapped():
        mini_frame.place_forget()
        if not AppState.progress_window_active:
            shift_main_content(False)
        AppState.mini_window_active = False
    else:
        mini_frame.place(
            x=0,
            y=70,
            width=SIDEBAR_WIDTH,
            height=root.winfo_height() - 70
        )
        mini_frame.lift()
        if not AppState.progress_window_active:
            shift_main_content(True)
        AppState.mini_window_active = True

# Toggle button with hover effect
toggle_btn = tk.Button(
    header,
    text="☰",
    font=("Segoe UI", 18),
    bg=HEADER_BG,
    fg=TEXT_WHITE,
    bd=0,
    activebackground="#34495e",
    activeforeground=TEXT_WHITE,
    cursor="hand2",
    command=toggle_mini_window
)
toggle_btn.pack(side="left", padx=(15, 10), pady=20)

# App title with subtle shadow effect
title_label = tk.Label(
    header,
    text="Tasky",
    font=header_font,
    bg=HEADER_BG,
    fg=TEXT_WHITE
)
title_label.pack(side="left", padx=5)

# Version/subtitle
tk.Label(
    header,
    text="· organize your day",
    font=("Segoe UI", 14),
    bg=HEADER_BG,
    fg="#a0b3c9"
).pack(side="left", padx=(5, 0))

# ===== NEW: Add Refresh Button =====
# Create a frame for right-side buttons
right_buttons = tk.Frame(header, bg=HEADER_BG)
right_buttons.pack(side="right", padx=20)

# Refresh button
refresh_btn = tk.Button(
    right_buttons,
    text="🔄 Refresh",
    font=("Segoe UI", 11, "bold"),
    bg="#2c3e50",  # Slightly lighter than header
    fg=TEXT_WHITE,
    bd=0,
    padx=15,
    pady=5,
    activebackground="#34495e",
    activeforeground=TEXT_WHITE,
    cursor="hand2",
    command=manual_refresh
)
refresh_btn.pack(side="left", padx=5)

# Add hover effect
refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg="#34495e"))
refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg="#2c3e50"))

# ============================================================================
# MAIN PAGE CONTENT - Clean and professional
# ============================================================================

# "My Day" section with zero top padding
myday_label = tk.Label(
    main_container,
    text="My Day",
    font=myday_font,
    bg=BG_COLOR,
    fg=TEXT_PRIMARY
)
myday_label.pack(anchor="w", padx=40, pady=(0, 5))

# Date display with nice formatting
today = datetime.today()
day_name = today.strftime("%A")
day_number = today.strftime("%d")
month_year = today.strftime("%B %Y")

date_frame = tk.Frame(main_container, bg=BG_COLOR)
date_frame.pack(anchor="w", padx=40, pady=(0, 15))

day_label = tk.Label(
    date_frame,
    text=day_name,
    font=("Segoe UI", 14, "bold"),
    bg=BG_COLOR,
    fg=ACCENT_BLUE
)
day_label.pack(side="left")

date_label = tk.Label(
    date_frame,
    text=f", {day_number} {month_year}",
    font=desc_font,
    bg=BG_COLOR,
    fg=TEXT_SECONDARY
)
date_label.pack(side="left")

# Store references for shifting
calendar_ref = date_frame  # Use date_frame for shifting

def shift_main_content(active):
    """Smooth content shift when sidebar opens"""
    AppState.mini_window_active = active
    pad = CONTENT_SHIFT if active else 40
    
    myday_label.pack_configure(anchor="w", padx=(pad, 40))
    date_frame.pack_configure(anchor="w", padx=(pad, 40))
    canvas_frame.pack_configure(padx=(pad-10 if active else 30, 30))

# ============================================================================
# PROGRESS WINDOW CONTROLS
# ============================================================================

def hide_main_content():
    myday_label.pack_forget()
    date_frame.pack_forget()
    canvas_frame.pack_forget()
    
def show_main_content():
    try:
        myday_label.pack(anchor="w", padx=40, pady=(0, 5))
        date_frame.pack(anchor="w", padx=40, pady=(0, 15))
        canvas_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))
    except:
        pass

def toggle_progress_window():
    """Open/close analytics window"""
    # Close sidebar if open
    if AppState.mini_window_active:
        mini_frame.place_forget()
        shift_main_content(False)
        AppState.mini_window_active = False
    
    if AppState.progress_window_active:
        # Close progress window
        if AppState.progress_frame:
            AppState.progress_frame.pack_forget()
        AppState.progress_window_active = False
        show_main_content()
        root.unbind("<Escape>")
        
        # Re-enable scrolling
        if AppState.rebind_scrolling_func:
            AppState.rebind_scrolling_func()
    else:
        # Open progress window
        hide_main_content()
        create_progress_window()
        AppState.progress_window_active = True

# Register control functions
set_control_functions(hide_main_content, show_main_content, toggle_mini_window)
print("[GUI] Control functions registered")

# ============================================================================
# INITIALIZE PLANNER
# ============================================================================

planner = PlannerWindow(root, main_container)

# ============================================================================
# SIDEBAR CONSTRUCTION - Modern, clean design
# ============================================================================

mini_frame = tk.Frame(root, bg=TASK_BG, bd=0, relief="flat")
mini_frame.pack_propagate(False)

# Sidebar header with gradient-like effect
mini_header = tk.Frame(mini_frame, bg="#f8f9fa", height=50)
mini_header.pack(fill="x")
mini_header.pack_propagate(False)

tk.Label(
    mini_header,
    text="Quick Actions",
    font=("Segoe UI", 14, "bold"),
    bg="#f8f9fa",
    fg=HEADER_BG
).pack(pady=15, padx=20, anchor="w")

# Sidebar content area
mini_content = tk.Frame(mini_frame, bg=TASK_BG)
mini_content.pack(fill="both", expand=True, padx=20, pady=15)

# ============================================================================
# CUSTOM ROUNDED BUTTON
# ============================================================================

def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
        x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
        x1, y2, x1, y2-r, x1, y1+r, x1, y1
    ]
    return self.create_polygon(points, **kwargs, smooth=True)

tk.Canvas.create_rounded_rect = create_rounded_rect

class RoundedButton:
    def __init__(self, parent, text, command, width=220, height=45, corner_radius=22):
        self.parent = parent
        self.text = text
        self.command = command
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.normal_color = ACCENT_BLUE
        self.hover_color = "#2980b9"
        self.current_color = self.normal_color
        
        self.container = tk.Frame(parent, bg=TASK_BG, width=width, height=height)
        self.container.pack_propagate(False)
        self.container.pack(pady=(0, 12))
        
        self.canvas = tk.Canvas(
            self.container, 
            width=width, 
            height=height, 
            bg=TASK_BG,
            highlightthickness=0
        )
        self.canvas.pack()
        
        self.button_bg = self.canvas.create_rounded_rect(
            0, 0, width, height, corner_radius, 
            fill=self.normal_color, outline=""
        )
        
        self.text_id = self.canvas.create_text(
            width//2, height//2,
            text=text,
            font=button_font,
            fill=TEXT_WHITE
        )
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)
        self.canvas.config(cursor="hand2")
    
    def on_click(self, event):
        self.command()
        self.canvas.itemconfig(self.button_bg, fill=self.hover_color)
        self.container.after(100, lambda: self.canvas.itemconfig(self.button_bg, fill=self.current_color))
    
    def on_enter(self, event):
        self.current_color = self.hover_color
        self.canvas.itemconfig(self.button_bg, fill=self.hover_color)
    
    def on_leave(self, event):
        self.current_color = self.normal_color
        self.canvas.itemconfig(self.button_bg, fill=self.normal_color)

# Add task button
add_button = RoundedButton(mini_content, "＋ Add New Task", add_task_gui)

# Separator
separator1 = tk.Frame(mini_content, height=1, bg="#ecf0f1")
separator1.pack(fill="x", pady=10)

# ============================================================================
# CALENDAR SECTION
# ============================================================================

calendar_container = tk.Frame(mini_content, bg=TASK_BG)
calendar_container.pack(fill="x", pady=(5, 0))

calendar_header_frame = tk.Frame(calendar_container, bg=TASK_BG, cursor="hand2")
calendar_header_frame.pack(fill="x", pady=(0, 10))

calendar_arrow = tk.Label(
    calendar_header_frame,
    text="▶",
    font=("Segoe UI", 10),
    bg=TASK_BG,
    fg=TEXT_LIGHT
)
calendar_arrow.pack(side="left", padx=(0, 8))

tk.Label(
    calendar_header_frame,
    text="📅",
    font=("Segoe UI", 14),
    bg=TASK_BG,
    fg=ACCENT_BLUE
).pack(side="left", padx=(0, 8))

calendar_title = tk.Label(
    calendar_header_frame,
    text="Calendar",
    font=("Segoe UI", 13, "bold"),
    bg=TASK_BG,
    fg=HEADER_BG
)
calendar_title.pack(side="left")

def toggle_calendar():
    AppState.calendar_expanded = not AppState.calendar_expanded
    
    if AppState.calendar_expanded:
        calendar_content.pack(fill="x", pady=(5, 0))
        calendar_arrow.config(text="▼")
        create_calendar()
    else:
        for widget in calendar_content.winfo_children():
            widget.destroy()
        calendar_content.pack_forget()
        calendar_arrow.config(text="▶")

calendar_header_frame.bind("<Button-1>", lambda e: toggle_calendar())
calendar_arrow.bind("<Button-1>", lambda e: toggle_calendar())
calendar_title.bind("<Button-1>", lambda e: toggle_calendar())

calendar_content = tk.Frame(calendar_container, bg=TASK_BG)

def create_calendar(selected_year=None, selected_month=None):
    for widget in calendar_content.winfo_children():
        widget.destroy()
    
    today = date.today()
    year = selected_year if selected_year else today.year
    month = selected_month if selected_month else today.month
    
    # Month/Year selector
    selector = tk.Frame(calendar_content, bg=TASK_BG)
    selector.pack(fill="x", pady=(0, 10))
    
    tk.Label(selector, text="Month:", font=small_font, bg=TASK_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 5))
    
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    
    month_combo = ttk.Combobox(
        selector,
        values=months,
        font=small_font,
        state="readonly",
        width=10
    )
    month_combo.set(datetime(year, month, 1).strftime("%B"))
    month_combo.pack(side="left", padx=(0, 10))
    
    tk.Label(selector, text="Year:", font=small_font, bg=TASK_BG, fg=TEXT_PRIMARY).pack(side="left", padx=(0, 5))
    
    years = [str(y) for y in range(2020, 2031)]
    year_combo = ttk.Combobox(
        selector,
        values=years,
        font=small_font,
        state="readonly",
        width=6
    )
    year_combo.set(str(year))
    year_combo.pack(side="left")
    
    def update_calendar():
        month_name = month_combo.get()
        year_str = year_combo.get()
        if month_name and year_str:
            month_dict = {m: i+1 for i, m in enumerate(months)}
            create_calendar(int(year_str), month_dict[month_name])
    
    month_combo.bind("<<ComboboxSelected>>", lambda e: update_calendar())
    year_combo.bind("<<ComboboxSelected>>", lambda e: update_calendar())
    
    # Month header
    month_header = tk.Label(
        calendar_content,
        text=datetime(year, month, 1).strftime("%B %Y"),
        font=calendar_header_font,
        bg=TASK_BG,
        fg=HEADER_BG
    )
    month_header.pack(pady=(5, 10))
    
    # Day headers
    days_frame = tk.Frame(calendar_content, bg=TASK_BG)
    days_frame.pack(fill="x", pady=(0, 5))
    
    days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for day in days:
        tk.Label(
            days_frame,
            text=day,
            font=small_font,
            bg=TASK_BG,
            fg=TEXT_SECONDARY,
            width=3
        ).pack(side="left", padx=1)
    
    # Calendar grid
    grid = tk.Frame(calendar_content, bg=TASK_BG)
    grid.pack(fill="x")
    
    first_day = date(year, month, 1)
    start_col = first_day.weekday()
    
    if month == 12:
        num_days = (date(year+1, 1, 1) - first_day).days
    else:
        num_days = (date(year, month+1, 1) - first_day).days
    
    # Empty cells
    for col in range(start_col):
        tk.Label(grid, text="", width=3, bg=TASK_BG).grid(row=0, column=col, padx=1, pady=1)
    
    # Day cells
    row = 0
    col = start_col
    for day in range(1, num_days + 1):
        if col == 7:
            col = 0
            row += 1
        
        bg = ACCENT_BLUE if (day == today.day and month == today.month and year == today.year) else TASK_BG
        fg = TEXT_WHITE if bg == ACCENT_BLUE else TEXT_PRIMARY
        
        tk.Label(
            grid,
            text=str(day),
            font=small_font,
            bg=bg,
            fg=fg,
            width=3,
            relief="flat"
        ).grid(row=row, column=col, padx=1, pady=1)
        
        col += 1

separator2 = tk.Frame(mini_content, height=1, bg="#ecf0f1")
separator2.pack(fill="x", pady=10)

# ============================================================================
# STATISTICS SECTION
# ============================================================================

stats_container = tk.Frame(mini_content, bg=TASK_BG)
stats_container.pack(fill="x", pady=(5, 0))

stats_header_frame = tk.Frame(stats_container, bg=TASK_BG, cursor="hand2")
stats_header_frame.pack(fill="x", pady=(0, 10))

stats_arrow = tk.Label(
    stats_header_frame,
    text="▶",
    font=("Segoe UI", 10),
    bg=TASK_BG,
    fg=TEXT_LIGHT
)
stats_arrow.pack(side="left", padx=(0, 8))

tk.Label(
    stats_header_frame,
    text="📊",
    font=("Segoe UI", 14),
    bg=TASK_BG,
    fg=ACCENT_GREEN
).pack(side="left", padx=(0, 8))

stats_title = tk.Label(
    stats_header_frame,
    text="Statistics",
    font=("Segoe UI", 13, "bold"),
    bg=TASK_BG,
    fg=HEADER_BG
)
stats_title.pack(side="left")

def toggle_stats():
    AppState.stats_expanded = not AppState.stats_expanded
    
    if AppState.stats_expanded:
        stats_content.pack(fill="x", pady=(5, 0))
        stats_arrow.config(text="▼")
        update_stats()
    else:
        stats_content.pack_forget()
        stats_arrow.config(text="▶")

stats_header_frame.bind("<Button-1>", lambda e: toggle_stats())
stats_arrow.bind("<Button-1>", lambda e: toggle_stats())
stats_title.bind("<Button-1>", lambda e: toggle_stats())

stats_content = tk.Frame(stats_container, bg=TASK_BG)

def update_stats():
    if not AppState.stats_expanded:
        return
        
    stats = get_task_statistics()
    
    total_label.config(text=f"Total: {stats['total']}")
    completed_label.config(text=f"Done: {stats['completed']}")
    pending_label.config(text=f"Pending: {stats['pending']}")
    rate_label.config(text=f"Rate: {stats['completion_rate']:.0f}%")
    
    if stats['tasks_with_duration'] > 0:
        avg_time_label.config(
            text=f"Avg: {format_duration(stats['avg_completion_time'])}",
            fg=TEXT_PRIMARY
        )
    else:
        avg_time_label.config(text="Avg: No data", fg=TEXT_LIGHT)

# Stats display
total_label = tk.Label(stats_content, font=small_font, bg=TASK_BG, fg=TEXT_PRIMARY, anchor="w")
total_label.pack(fill="x", pady=3)

completed_label = tk.Label(stats_content, font=small_font, bg=TASK_BG, fg=TEXT_PRIMARY, anchor="w")
completed_label.pack(fill="x", pady=3)

pending_label = tk.Label(stats_content, font=small_font, bg=TASK_BG, fg=TEXT_PRIMARY, anchor="w")
pending_label.pack(fill="x", pady=3)

rate_label = tk.Label(stats_content, font=small_font, bg=TASK_BG, fg=TEXT_PRIMARY, anchor="w")
rate_label.pack(fill="x", pady=3)

avg_time_label = tk.Label(stats_content, font=small_font, bg=TASK_BG, fg=TEXT_LIGHT, anchor="w")
avg_time_label.pack(fill="x", pady=3)

separator3 = tk.Frame(mini_content, height=1, bg="#ecf0f1")
separator3.pack(fill="x", pady=10)

# ============================================================================
# SIDEBAR BUTTONS
# ============================================================================

progress_btn = RoundedButton(mini_content, "📈 Analytics", toggle_progress_window)
planner_btn = RoundedButton(mini_content, "📋 Planner", planner.open)

# ============================================================================
# SCROLLING SYSTEM
# ============================================================================

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    return "break"

def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(canvas_window, width=canvas.winfo_width())

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=canvas.winfo_width())
    update_scroll_region()

def reset_scroll_position():
    canvas.yview_moveto(0)
    canvas.update_idletasks()

def setup_scrolling():
    def on_mousewheel(event):
        if not AppState.progress_window_active and not AppState.planner_window_active:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"
    
    def bind_to_mousewheel(widget):
        widget.bind("<MouseWheel>", on_mousewheel)
        widget.bind("<Button-4>", on_mousewheel)
        widget.bind("<Button-5>", on_mousewheel)
        
        for child in widget.winfo_children():
            try:
                bind_to_mousewheel(child)
            except:
                pass
    
    def rebind_scrolling():
        canvas.unbind("<MouseWheel>")
        task_container.unbind("<MouseWheel>")
        main_container.unbind("<MouseWheel>")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        bind_to_mousewheel(main_container)
        bind_to_mousewheel(task_container)
        bind_to_mousewheel(canvas_frame)
    
    rebind_scrolling()
    AppState.rebind_scrolling_func = rebind_scrolling

# ============================================================================
# TASK DISPLAY AREA
# ============================================================================

canvas_frame = tk.Frame(main_container, bg=BG_COLOR)
canvas_frame.pack(fill="both", expand=True, padx=30, pady=(0, 10))

canvas = tk.Canvas(canvas_frame, bg=BG_COLOR, highlightthickness=0)
scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

canvas.configure(yscrollcommand=scrollbar.set)

task_container = tk.Frame(canvas, bg=BG_COLOR)
canvas_window = canvas.create_window((0, 0), window=task_container, anchor="nw")

canvas.bind("<Configure>", on_canvas_configure)
task_container.bind("<Configure>", update_scroll_region)

# ============================================================================
# TASK CARD - Clean, modern design
# ============================================================================

class TaskCard:
    def __init__(self, parent, idx, task_id, title, status, description, category="General", priority="Medium"):
        self.parent = parent
        self.task_id = task_id
        self.buttons_visible = False
        
        # Card with subtle shadow effect
        self.card = tk.Frame(
            parent, 
            bg=TASK_BG, 
            bd=0,
            relief="flat",
            highlightbackground="#e0e0e0",
            highlightthickness=1
        )
        self.card.pack(fill="x", padx=5, pady=6)
        
        # Content
        content = tk.Frame(self.card, bg=TASK_BG)
        content.pack(fill="x", padx=15, pady=12)
        
        # Left section
        left = tk.Frame(content, bg=TASK_BG)
        left.pack(side="left", fill="both", expand=True)
        
        # Title row
        title_row = tk.Frame(left, bg=TASK_BG)
        title_row.pack(anchor="w", pady=(0, 5))
        
        # Number
        self.num = tk.Label(
            title_row,
            text=f"{idx + 1}.",
            font=("Segoe UI", 12, "bold"),
            bg=TASK_BG,
            fg=TEXT_LIGHT
        )
        self.num.pack(side="left", padx=(0, 8))
        
        # Checkmark for done tasks
        if status == "Done":
            self.check = tk.Label(
                title_row,
                text="✓",
                font=("Segoe UI", 14, "bold"),
                bg=TASK_BG,
                fg=TASK_DONE_CHECK
            )
            self.check.pack(side="left", padx=(0, 6))
        
        # Title
        self.title = tk.Label(
            title_row,
            text=title,
            font=("Segoe UI", 13, "bold"),
            bg=TASK_BG,
            fg=TASK_DONE_CHECK if status == "Done" else TEXT_PRIMARY
        )
        self.title.pack(side="left")

        # Badges
        badges = tk.Frame(title_row, bg=TASK_BG)
        badges.pack(side="left", padx=(10, 0))
        
        # Category badge
        self.category = tk.Label(
            badges,
            text=category,
            font=("Segoe UI", 9),
            bg="#e8f0fe",
            fg=HEADER_BG,
            padx=8,
            pady=2
        )
        self.category.pack(side="left", padx=(0, 5))
        
        # Priority badge with color
        priority_colors = {
            "High": {"bg": "#fee9e7", "fg": "#c0392b"},
            "Medium": {"bg": "#fef6e3", "fg": "#e67e22"},
            "Low": {"bg": "#e8f5e9", "fg": "#27ae60"}
        }
        pc = priority_colors.get(priority, {"bg": "#f0f0f0", "fg": TEXT_SECONDARY})
        
        self.priority = tk.Label(
            badges,
            text=priority,
            font=("Segoe UI", 9, "bold"),
            bg=pc["bg"],
            fg=pc["fg"],
            padx=8,
            pady=2
        )
        self.priority.pack(side="left")

        # Description
        if description:
            self.desc = tk.Label(
                left,
                text=description,
                font=("Segoe UI", 11),
                bg=TASK_BG,
                fg=TEXT_SECONDARY,
                wraplength=500,
                anchor="w"
            )
            self.desc.pack(anchor="w", pady=(5, 0))

        # Duration for completed tasks
        if status == "Done":
            for task in list_tasks():
                if task[0] == task_id:
                    duration = get_task_duration(task)
                    if duration:
                        self.duration = tk.Label(
                            left,
                            text=f"Completed in {format_duration(duration)}",
                            font=("Segoe UI", 10),
                            bg=TASK_BG,
                            fg=ACCENT_GREEN,
                            anchor="w"
                        )
                        self.duration.pack(anchor="w", pady=(5, 0))
                    break

        # Buttons
        self.btn_frame = tk.Frame(content, bg=TASK_BG)
        self.btn_frame.pack(side="right", padx=(10, 0))
        
        self.btns = tk.Frame(self.btn_frame, bg=TASK_BG)
        self.btns.pack()

        # Action buttons
        self.start = tk.Button(
            self.btns,
            text="▶",
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_WHITE,
            bg=BTN_START,
            width=3,
            bd=0,
            cursor="hand2",
            command=lambda: start_task_gui(task_id)
        )
        
        self.done = tk.Button(
            self.btns,
            text="✓",
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_WHITE,
            bg=BTN_DONE,
            width=3,
            bd=0,
            cursor="hand2",
            command=lambda: mark_done_gui(task_id)
        )

        self.delete = tk.Button(
            self.btns,
            text="✗",
            font=("Segoe UI", 10, "bold"),
            fg=TEXT_WHITE,
            bg=BTN_DELETE,
            width=3,
            bd=0,
            cursor="hand2",
            command=lambda: delete_task_gui(task_id)
        )
        
        self.bind_all()
    
    def toggle_buttons(self):
        if AppState.active_buttons and AppState.active_buttons != self:
            AppState.active_buttons.hide_buttons()
            AppState.active_buttons = None
        
        if self.buttons_visible:
            self.hide_buttons()
            AppState.active_buttons = None
        else:
            self.show_buttons()
            AppState.active_buttons = self
    
    def show_buttons(self):
        self.start.pack(side="left", padx=2)
        self.done.pack(side="left", padx=2)
        self.delete.pack(side="left", padx=2)
        self.buttons_visible = True
    
    def hide_buttons(self):
        self.start.pack_forget()
        self.done.pack_forget()
        self.delete.pack_forget()
        self.buttons_visible = False
    
    def bind_all(self):
        self.card.bind("<Button-1>", lambda e: self.toggle_buttons())
        self.num.bind("<Button-1>", lambda e: self.toggle_buttons())
        if hasattr(self, 'check'):
            self.check.bind("<Button-1>", lambda e: self.toggle_buttons())
        self.title.bind("<Button-1>", lambda e: self.toggle_buttons())
        self.category.bind("<Button-1>", lambda e: self.toggle_buttons())
        self.priority.bind("<Button-1>", lambda e: self.toggle_buttons())
        if hasattr(self, 'desc'):
            self.desc.bind("<Button-1>", lambda e: self.toggle_buttons())
        if hasattr(self, 'duration'):
            self.duration.bind("<Button-1>", lambda e: self.toggle_buttons())

# ============================================================================
# TASK REFRESH
# ============================================================================

def refresh_tasks():
    """Refresh tasks display - only shows visible (hidden=0) tasks"""
    for widget in task_container.winfo_children():
        widget.destroy()
    AppState.active_buttons = None

    # Use list_tasks() which now defaults to hidden=0
    from tasks import list_tasks, get_hidden_count
    visible_tasks = list_tasks(include_hidden=False)
    hidden_count = get_hidden_count()
    
    # Debug output
    if hidden_count > 0:
        print(f"[Display] Showing {len(visible_tasks)} tasks, {hidden_count} tasks hidden in DB")
    
    # If no visible tasks, show empty state
    if not visible_tasks:
        if hidden_count > 0:
            show_empty_main_message(
                "✨ Tasks hidden", 
                f"{hidden_count} tasks hidden - use 'Show All' to restore"
            )
        else:
            show_empty_main_message(
                "📋 No tasks yet", 
                "Click '+ Add New Task' to get started"
            )
        return
    
    # Display visible tasks
    for idx, task in enumerate(visible_tasks):
        task_id = task[0]
        title = task[1]
        description = task[2] if task[2] else ""
        status = task[3]
        category = task[4] if task[4] else "General"
        priority = task[5] if task[5] else "Medium"
        
        TaskCard(
            task_container, 
            idx, 
            task_id, 
            title, 
            status, 
            description,
            category,
            priority
        )
    
    update_scroll_region()
    reset_scroll_position()
    
    if AppState.rebind_scrolling_func:
        AppState.rebind_scrolling_func()
    
    if AppState.mini_window_active and AppState.stats_expanded:
        update_stats()

# ============================================================================
# PROGRESS ANALYTICS WINDOW - Clean version (Unfinished tab removed)
# ============================================================================

def create_progress_window():
    if AppState.progress_frame:
        try:
            if AppState.progress_frame.winfo_exists():
                AppState.progress_frame.destroy()
        except:
            pass
    
    BG_LIGHT = "#f8fafc"
    HEADER_BG_DARK = "#1e2b3a"
    
    AppState.progress_frame = tk.Frame(main_container, bg=BG_LIGHT, relief="flat")
    AppState.progress_frame.pack(fill="both", expand=True, padx=0, pady=0)
    
    # Header
    header = tk.Frame(AppState.progress_frame, bg=HEADER_BG_DARK, height=80)
    header.pack(fill="x", pady=(0, 0))
    header.pack_propagate(False)
    
    header_content = tk.Frame(header, bg=HEADER_BG_DARK)
    header_content.pack(fill="both", expand=True, padx=30, pady=20)
    
    title_row = tk.Frame(header_content, bg=HEADER_BG_DARK)
    title_row.pack(fill="x")
    
    tk.Label(
        title_row,
        text="📊 Analytics Dashboard",
        font=("Segoe UI", 20, "bold"),
        bg=HEADER_BG_DARK,
        fg=TEXT_WHITE
    ).pack(side="left")
    
    tk.Button(
        title_row,
        text="✕ Close",
        font=button_font,
        bg="#34495e",
        fg=TEXT_WHITE,
        bd=0,
        padx=15,
        pady=5,
        activebackground="#3d566e",
        cursor="hand2",
        command=toggle_progress_window
    ).pack(side="right", padx=(0, 20))
    
    # Subtitle
    tk.Label(
        header_content,
        text=f"{datetime.now().strftime('%A, %B %d, %Y')}",
        font=("Segoe UI", 11),
        bg=HEADER_BG_DARK,
        fg="#a0b3c9"
    ).pack(anchor="w")

    # Scrollable content
    scroll = tk.Frame(AppState.progress_frame, bg=BG_LIGHT)
    scroll.pack(fill="both", expand=True)
    
    canvas = tk.Canvas(scroll, bg=BG_LIGHT, highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg=BG_LIGHT)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    
    def config_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    scroll_frame.bind("<Configure>", config_scroll)
    
    # Tabs - with proper spacing
    tab_frame = tk.Frame(scroll_frame, bg=BG_LIGHT)
    tab_frame.pack(fill="x", pady=(20, 20), padx=30)
    
    # Tab buttons
    tab_btns = {}
    tab_contents = {}
    current_tab = "Daily"
    
    def switch_tab(name):
        nonlocal current_tab
        for n, btn in tab_btns.items():
            if n == name:
                btn.config(bg=ACCENT_BLUE, fg=TEXT_WHITE)
            else:
                btn.config(bg="#ecf0f1", fg=TEXT_SECONDARY)
        
        for n, content in tab_contents.items():
            content.pack_forget()
        tab_contents[name].pack(fill="both", expand=True, padx=0, pady=(10, 0))
        current_tab = name
    
    # Create tabs - 3 tabs only (Unfinished removed)
    tabs = [("Daily", "📅"), ("Weekly", "📈"), ("Monthly", "📊")]
    
    btn_frame = tk.Frame(tab_frame, bg=BG_LIGHT)
    btn_frame.pack()
    
    for name, icon in tabs:
        btn_bg = ACCENT_BLUE if name == "Daily" else "#ecf0f1"
        btn_fg = TEXT_WHITE if name == "Daily" else TEXT_SECONDARY
            
        btn = tk.Button(
            btn_frame,
            text=f"{icon} {name}",
            font=button_font,
            bg=btn_bg,
            fg=btn_fg,
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=lambda n=name: switch_tab(n)
        )
        btn.pack(side="left", padx=5)
        tab_btns[name] = btn
    
    # ============================================
    # DAILY TAB
    # ============================================
    daily = tk.Frame(tab_frame, bg=BG_LIGHT)
    tab_contents["Daily"] = daily
    
    daily_data = get_daily_performance()
    streak = get_completion_streak()
    
    # Stats cards row
    card_row = tk.Frame(daily, bg=BG_LIGHT)
    card_row.pack(fill="x", pady=10)
    
    # Configure grid for 3 cards
    for i in range(3):
        card_row.grid_columnconfigure(i, weight=1, pad=5)
    
    # Completed card
    comp_card = tk.Frame(card_row, bg=TASK_BG, bd=0, highlightbackground="#e0e0e0", highlightthickness=1)
    comp_card.grid(row=0, column=0, sticky="ew", padx=5)
    
    tk.Label(comp_card, text="✅ Completed", font=("Segoe UI", 12), bg=TASK_BG, fg=TEXT_SECONDARY).pack(pady=(15, 5))
    tk.Label(comp_card, text=str(daily_data['total_completed']), font=("Segoe UI", 32, "bold"), bg=TASK_BG, fg=ACCENT_GREEN).pack()
    tk.Label(comp_card, text=f"of {daily_data['total_created']} tasks", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_LIGHT).pack(pady=(5, 15))
    
    # Time card
    time_card = tk.Frame(card_row, bg=TASK_BG, bd=0, highlightbackground="#e0e0e0", highlightthickness=1)
    time_card.grid(row=0, column=1, sticky="ew", padx=5)
    
    tk.Label(time_card, text="⏱️ Time Spent", font=("Segoe UI", 12), bg=TASK_BG, fg=TEXT_SECONDARY).pack(pady=(15, 5))
    time_text = f"{daily_data['total_time_minutes']:.0f} min" if daily_data['total_time_minutes'] > 0 else "0 min"
    tk.Label(time_card, text=time_text, font=("Segoe UI", 24, "bold"), bg=TASK_BG, fg=ACCENT_BLUE).pack()
    tk.Label(time_card, text="today", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_LIGHT).pack(pady=(5, 15))
    
    # Streak card
    streak_card = tk.Frame(card_row, bg=TASK_BG, bd=0, highlightbackground="#e0e0e0", highlightthickness=1)
    streak_card.grid(row=0, column=2, sticky="ew", padx=5)
    
    tk.Label(streak_card, text="🔥 Streak", font=("Segoe UI", 12), bg=TASK_BG, fg=TEXT_SECONDARY).pack(pady=(15, 5))
    streak_icon = "🔥" if streak > 0 else "📅"
    tk.Label(streak_card, text=f"{streak_icon} {streak}", font=("Segoe UI", 24, "bold"), bg=TASK_BG, fg=ACCENT_ORANGE).pack()
    tk.Label(streak_card, text="days", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_LIGHT).pack(pady=(5, 15))
    
    # Progress bar
    if daily_data['total_created'] > 0:
        progress = (daily_data['total_completed'] / daily_data['total_created']) * 100
    else:
        progress = 0
    
    prog_frame = tk.Frame(daily, bg=TASK_BG, bd=0, highlightbackground="#e0e0e0", highlightthickness=1)
    prog_frame.pack(fill="x", pady=20)
    
    tk.Label(prog_frame, text="📊 Daily Progress", font=("Segoe UI", 12, "bold"), bg=TASK_BG, fg=TEXT_PRIMARY).pack(anchor="w", padx=20, pady=(15, 10))
    
    bar_frame = tk.Frame(prog_frame, bg=TASK_BG)
    bar_frame.pack(fill="x", padx=20, pady=(0, 15))
    
    bar_bg = tk.Frame(bar_frame, bg="#ecf0f1", height=20)
    bar_bg.pack(fill="x")
    
    bar = tk.Frame(bar_bg, bg=ACCENT_GREEN, height=20)
    bar.place(x=0, y=0, width=int(progress * 5), height=20)
    
    tk.Label(bar_frame, text=f"{progress:.0f}%", font=button_font, bg=TASK_BG, fg=ACCENT_GREEN).pack(pady=(5, 0))
    
    # ============================================
    # WEEKLY TAB
    # ============================================
    weekly = tk.Frame(tab_frame, bg=BG_LIGHT)
    tab_contents["Weekly"] = weekly
    
    weekly_data = get_weekly_performance()
    
    w_frame = tk.Frame(weekly, bg=TASK_BG, bd=0, highlightbackground="#e0e0e0", highlightthickness=1)
    w_frame.pack(fill="x", pady=10)
    
    # Weekly header
    header_row = tk.Frame(w_frame, bg=TASK_BG)
    header_row.pack(fill="x", padx=20, pady=(15, 5))
    
    tk.Label(
        header_row,
        text="📈 This Week",
        font=("Segoe UI", 14, "bold"),
        bg=TASK_BG,
        fg=TEXT_PRIMARY
    ).pack(side="left")
    
    # Date range
    week_range = f"{weekly_data['week_start']} to {weekly_data['week_end']}"
    tk.Label(
        header_row,
        text=week_range,
        font=("Segoe UI", 10),
        bg=TASK_BG,
        fg=TEXT_LIGHT
    ).pack(side="right")
    
    # Stats row
    stats_row = tk.Frame(w_frame, bg=TASK_BG)
    stats_row.pack(fill="x", padx=20, pady=(10, 15))
    
    # Completed
    comp_col = tk.Frame(stats_row, bg=TASK_BG)
    comp_col.pack(side="left", expand=True, fill="both")
    
    tk.Label(comp_col, text="Completed", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_SECONDARY).pack()
    tk.Label(comp_col, text=str(weekly_data['total_completed']), font=("Segoe UI", 24, "bold"), bg=TASK_BG, fg=ACCENT_BLUE).pack()
    
    # Created
    created_col = tk.Frame(stats_row, bg=TASK_BG)
    created_col.pack(side="left", expand=True, fill="both")
    
    tk.Label(created_col, text="Created", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_SECONDARY).pack()
    tk.Label(created_col, text=str(weekly_data['total_created']), font=("Segoe UI", 24, "bold"), bg=TASK_BG, fg=TEXT_PRIMARY).pack()
    
    # Time
    time_col = tk.Frame(stats_row, bg=TASK_BG)
    time_col.pack(side="left", expand=True, fill="both")
    
    tk.Label(time_col, text="Time Spent", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_SECONDARY).pack()
    time_text = f"{weekly_data['total_time_minutes']:.0f} min" if weekly_data['total_time_minutes'] > 0 else "0 min"
    tk.Label(time_col, text=time_text, font=("Segoe UI", 20, "bold"), bg=TASK_BG, fg=ACCENT_GREEN).pack()
    
    # Most productive day
    if weekly_data['most_productive_day']:
        peak_frame = tk.Frame(w_frame, bg="#f0f9ff", bd=0, highlightbackground="#bae6fd", highlightthickness=1)
        peak_frame.pack(fill="x", pady=10, padx=20)
        
        tk.Label(
            peak_frame,
            text=f"🏆 Most Productive: {weekly_data['most_productive_day']}",
            font=("Segoe UI", 12, "bold"),
            bg="#f0f9ff",
            fg=ACCENT_BLUE
        ).pack(pady=10)
    
    # ============================================
    # MONTHLY TAB
    # ============================================
    monthly = tk.Frame(tab_frame, bg=BG_LIGHT)
    tab_contents["Monthly"] = monthly
    
    monthly_data = get_monthly_performance()
    
    m_frame = tk.Frame(monthly, bg=TASK_BG, bd=0, highlightbackground="#e0e0e0", highlightthickness=1)
    m_frame.pack(fill="x", pady=10)
    
    # Monthly header
    m_header = tk.Frame(m_frame, bg=TASK_BG)
    m_header.pack(fill="x", padx=20, pady=(15, 5))
    
    tk.Label(
        m_header,
        text="📊 This Month",
        font=("Segoe UI", 14, "bold"),
        bg=TASK_BG,
        fg=TEXT_PRIMARY
    ).pack(side="left")
    
    # Month name
    month_name = datetime.now().strftime("%B %Y")
    tk.Label(
        m_header,
        text=month_name,
        font=("Segoe UI", 10),
        bg=TASK_BG,
        fg=TEXT_LIGHT
    ).pack(side="right")
    
    # Stats row
    m_stats = tk.Frame(m_frame, bg=TASK_BG)
    m_stats.pack(fill="x", padx=20, pady=(10, 15))
    
    # Completed
    m_comp = tk.Frame(m_stats, bg=TASK_BG)
    m_comp.pack(side="left", expand=True, fill="both")
    
    tk.Label(m_comp, text="Completed", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_SECONDARY).pack()
    tk.Label(m_comp, text=str(monthly_data['total_completed']), font=("Segoe UI", 24, "bold"), bg=TASK_BG, fg=ACCENT_PURPLE).pack()
    
    # Created
    m_created = tk.Frame(m_stats, bg=TASK_BG)
    m_created.pack(side="left", expand=True, fill="both")
    
    tk.Label(m_created, text="Created", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_SECONDARY).pack()
    tk.Label(m_created, text=str(monthly_data['total_created']), font=("Segoe UI", 24, "bold"), bg=TASK_BG, fg=TEXT_PRIMARY).pack()
    
    # Rate
    m_rate = tk.Frame(m_stats, bg=TASK_BG)
    m_rate.pack(side="left", expand=True, fill="both")
    
    tk.Label(m_rate, text="Rate", font=("Segoe UI", 11), bg=TASK_BG, fg=TEXT_SECONDARY).pack()
    tk.Label(m_rate, text=f"{monthly_data['completion_rate']:.0f}%", font=("Segoe UI", 20, "bold"), bg=TASK_BG, fg=ACCENT_GREEN).pack()
    
    # Best week
    if monthly_data['best_week']:
        best_frame = tk.Frame(m_frame, bg="#f3e8ff", bd=0, highlightbackground="#e9d5ff", highlightthickness=1)
        best_frame.pack(fill="x", pady=10, padx=20)
        
        tk.Label(
            best_frame,
            text=f"🌟 Best Week: {monthly_data['best_week']}",
            font=("Segoe UI", 12, "bold"),
            bg="#f3e8ff",
            fg=ACCENT_PURPLE
        ).pack(pady=10)
    
    # Start with Daily tab
    switch_tab("Daily")
    
    # ESC to close
    def close_with_esc(event=None):
        toggle_progress_window()
    
    root.bind("<Escape>", close_with_esc)

# ============================================================================
# KEYBOARD SHORTCUTS
# ============================================================================

root.bind("<Control-n>", lambda e: add_task_gui())
root.bind("<Control-h>", lambda e: toggle_mini_window())

# ============================================================================
# INITIAL LOAD
# ============================================================================

refresh_tasks()
setup_scrolling()

# ============================================================================
# START THE APP
# ============================================================================

root.mainloop()