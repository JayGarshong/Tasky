# planner_window.py - Planner UI (imported by gui.py)
# FIXED: Header gap (lines 97 and 130) - Quick Add bar now touches header

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from planner_db import list_plans, add_plan, update_plan, delete_plan
from app_state import AppState, hide_main_view, show_main_view, close_sidebar

class PlannerWindow:
    def __init__(self, parent, main_container):
        self.parent = parent
        self.main_container = main_container
        self.window = None
        self.notebook = None
        self.week_frame = None
        self.month_frame = None
        self.week_content = None
        self.month_content = None
        
        # Colors - Match Analytics dashboard exactly
        self.BG_LIGHT = "#f8fafc"
        self.HEADER_BG = "#7e3af2"  # Purple instead of blue - distinguishes from Analytics
        self.HEADER_FG = "#ffffff"
        self.CARD_BG = "#ffffff"
        self.TEXT_PRIMARY = "#0f172a"
        self.TEXT_SECONDARY = "#475569"
        self.TEXT_LIGHT = "#64748b"
        self.ACCENT_PURPLE = "#8b5cf6"
        self.ACCENT_GREEN = "#10b981"
        self.ACCENT_ORANGE = "#f59e0b"
        self.ACCENT_RED = "#ef4444"
        self.ACCENT_BLUE = "#3b82f6"
        
        # Priority colors (match tasks)
        self.PRIORITY_COLORS = {
            "High": {"bg": "#ffebee", "fg": "#c62828"},
            "Medium": {"bg": "#fff3e0", "fg": "#ef6c00"},
            "Low": {"bg": "#e8f5e9", "fg": "#2e7d32"}
        }
        
        # Focus area colors
        self.FOCUS_COLORS = {
            "Career": {"bg": "#e3f2fd", "fg": "#0d47a1"},
            "Health": {"bg": "#e8f5e9", "fg": "#1b5e20"},
            "Learning": {"bg": "#fff3e0", "fg": "#e65100"},
            "Personal": {"bg": "#f3e5f5", "fg": "#4a148c"},
            "Finance": {"bg": "#e8eaf6", "fg": "#1a237e"},
            "Family": {"bg": "#ffebee", "fg": "#b71c1c"},
            "Social": {"bg": "#e0f2f1", "fg": "#004d40"},
            "General": {"bg": "#fafafa", "fg": "#37474f"}
        }
        
    def open(self):
        """Open planner as full-screen takeover (like Analytics)"""
        
        # ===== CRITICAL FIX: Close sidebar and hide main content =====
        close_sidebar()
        hide_main_view()
        # ============================================================
        
        # Create main planner frame that fills the main_container
        self.window = tk.Frame(
            self.main_container, 
            bg=self.BG_LIGHT,
            relief="flat"
        )
        self.window.pack(fill="both", expand=True, padx=0, pady=0)
        
        # ============================================
        # FIXED HEADER (OUTSIDE SCROLLABLE AREA)
        # ============================================
        
        # Header container - FIXED at top
        header_container = tk.Frame(self.window, bg=self.HEADER_BG, height=100)
        header_container.pack(fill="x", pady=(0, 0))
        header_container.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_container, bg=self.HEADER_BG)
        header_content.pack(fill="both", expand=True, padx=40, pady=25)
        
        # Title and return button row
        title_button_row = tk.Frame(header_content, bg=self.HEADER_BG)
        title_button_row.pack(fill="x", pady=(0, 8))
        
        # Title on left
        title_container = tk.Frame(title_button_row, bg=self.HEADER_BG)
        title_container.pack(side="left", fill="x", expand=True)
        
        tk.Label(
            title_container,
            text="📋 TASK PLANNER",
            font=("Segoe UI", 24, "bold"),
            bg=self.HEADER_BG,
            fg="#ffffff",
            anchor="w"
        ).pack(side="left")
        
        # Return button on right (matches Analytics close button)
        return_btn = tk.Button(
            title_button_row,
            text="← Return to Tasks",
            font=("Segoe UI", 11, "bold"),
            bg="#5e2ecc",  # Slightly darker purple
            fg="#ffffff",
            bd=0,
            padx=20,
            pady=8,
            activebackground="#6b3ad6",
            activeforeground="#ffffff",
            command=self.close,
            cursor="hand2",
            relief="flat",
            highlightthickness=0
        )
        return_btn.pack(side="right")
        
        # Subtitle
        subtitle_frame = tk.Frame(header_content, bg=self.HEADER_BG)
        subtitle_frame.pack(fill="x")
        
        tk.Label(
            subtitle_frame,
            text="Set weekly and monthly goals • Track what matters",
            font=("Segoe UI", 11),
            bg=self.HEADER_BG,
            fg="#e0d4ff",  # Light purple
            anchor="w"
        ).pack(fill="x")
        
        # ============================================
        # QUICK ADD BAR (BELOW HEADER)
        # ===== FIX #1B: Header Gap (Planner Window) =====
        # Changed pady=(20,0) to pady=(0,0) to eliminate gap
        # ============================================
        
        quick_add_frame = tk.Frame(self.window, bg=self.BG_LIGHT)
        quick_add_frame.pack(fill="x", pady=(0, 0), padx=40)  # ← FIXED: Removed top padding
        
        # Quick Add label
        tk.Label(
            quick_add_frame,
            text="Quick Add:",
            font=("Segoe UI", 12, "bold"),
            bg=self.BG_LIGHT,
            fg=self.TEXT_PRIMARY
        ).pack(side="left", padx=(0, 15))
        
        # Week plan quick button
        week_quick_btn = tk.Button(
            quick_add_frame,
            text="+ Week Plan",
            font=("Segoe UI", 10, "bold"),
            bg=self.ACCENT_GREEN,
            fg="white",
            bd=0,
            padx=15,
            pady=6,
            activebackground="#0ca678",
            activeforeground="white",
            cursor="hand2",
            command=lambda: self.show_add_dialog("Week")
        )
        week_quick_btn.pack(side="left", padx=5)
        
        # Month plan quick button
        month_quick_btn = tk.Button(
            quick_add_frame,
            text="+ Month Plan",
            font=("Segoe UI", 10, "bold"),
            bg=self.ACCENT_BLUE,
            fg="white",
            bd=0,
            padx=15,
            pady=6,
            activebackground="#2563eb",
            activeforeground="white",
            cursor="hand2",
            command=lambda: self.show_add_dialog("Month")
        )
        month_quick_btn.pack(side="left", padx=5)
        
        # Separator
        # ===== FIX #1B (continued): Adjusted top padding from 20 to 15 for cleaner spacing =====
        separator = tk.Frame(self.window, bg="#e2e8f0", height=1)
        separator.pack(fill="x", padx=40, pady=(15, 0))  # ← FIXED: Reduced from 20 to 15
        # ===== END FIX #1B =====
        
        # ============================================
        # SCROLLABLE CONTENT AREA WITH TABS
        # ============================================
        
        # Container for notebook
        notebook_container = tk.Frame(self.window, bg=self.BG_LIGHT)
        notebook_container.pack(fill="both", expand=True, padx=40, pady=(5, 20))
        
        # Create styled notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Planner.TNotebook', background=self.BG_LIGHT, borderwidth=0)
        style.configure('Planner.TNotebook.Tab', 
                       padding=[15, 8],
                       font=('Segoe UI', 11, 'bold'))
        style.map('Planner.TNotebook.Tab',
                 background=[('selected', self.HEADER_BG), ('active', '#e2e8f0')],
                 foreground=[('selected', 'white'), ('active', self.TEXT_PRIMARY)])
        
        self.notebook = ttk.Notebook(notebook_container, style='Planner.TNotebook')
        self.notebook.pack(fill="both", expand=True)
        
        # Week tab
        self.week_frame = tk.Frame(self.notebook, bg=self.BG_LIGHT)
        self.notebook.add(self.week_frame, text="📆 WEEK PLANS")
        
        # Month tab
        self.month_frame = tk.Frame(self.notebook, bg=self.BG_LIGHT)
        self.notebook.add(self.month_frame, text="📅 MONTH PLANS")
        
        # Create scrollable frames for each tab
        self.setup_scrollable_tab("week")
        self.setup_scrollable_tab("month")
        
        # Load plans
        self.refresh_plans()
        
        # Store reference in AppState
        AppState.planner_window_active = True
        AppState.planner_frame = self.window
    
    def setup_scrollable_tab(self, tab_name):
        """Setup scrollable area for a tab"""
        if tab_name == "week":
            parent = self.week_frame
        else:
            parent = self.month_frame
        
        # Canvas for scrolling
        canvas = tk.Canvas(parent, bg=self.BG_LIGHT, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        
        # Content frame
        content_frame = tk.Frame(canvas, bg=self.BG_LIGHT)
        
        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Add content frame to canvas
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        # Store references
        if tab_name == "week":
            self.week_canvas = canvas
            self.week_scrollbar = scrollbar
            self.week_content = content_frame
        else:
            self.month_canvas = canvas
            self.month_scrollbar = scrollbar
            self.month_content = content_frame
        
        # Configure scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        content_frame.bind("<Configure>", configure_scroll_region)
        
        # Configure canvas resize
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        
        canvas.bind("<Configure>", on_canvas_configure)
        
        # Mouse wheel binding
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)
        content_frame.bind("<MouseWheel>", on_mousewheel)
    
    def close(self):
        """Close planner and return to main view"""
        if self.window and self.window.winfo_exists():
            self.window.destroy()
            self.window = None
        
        AppState.planner_window_active = False
        AppState.planner_frame = None
        
        # ===== SHOW MAIN CONTENT - FIXED =====
        show_main_view()
    
    def show_add_dialog(self, time_frame="Week"):
        """Show dialog to add a new plan"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(f"Add {time_frame} Plan")
        dialog.geometry("500x480")
        dialog.configure(bg=self.BG_LIGHT)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center on parent
        dialog.update_idletasks()
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - (500 // 2)
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - (480 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Dialog header
        header_frame = tk.Frame(dialog, bg=self.HEADER_BG, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"✨ Create New {time_frame} Plan",
            font=("Segoe UI", 14, "bold"),
            bg=self.HEADER_BG,
            fg="white"
        ).pack(pady=12)
        
        # Content frame
        content = tk.Frame(dialog, bg=self.BG_LIGHT, padx=30, pady=25)
        content.pack(fill="both", expand=True)
        
        # Heading field
        tk.Label(
            content, 
            text="Plan Heading", 
            font=("Segoe UI", 11, "bold"),
            bg=self.BG_LIGHT, 
            fg=self.TEXT_PRIMARY,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        heading_entry = tk.Entry(
            content, 
            font=("Calibri", 12), 
            width=45,
            relief="solid",
            bd=1
        )
        heading_entry.pack(fill="x", pady=(0, 15))
        heading_entry.focus_set()
        
        # Description field
        tk.Label(
            content, 
            text="Description (optional)", 
            font=("Segoe UI", 11),
            bg=self.BG_LIGHT, 
            fg=self.TEXT_PRIMARY,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        desc_entry = tk.Entry(
            content, 
            font=("Calibri", 12), 
            width=45,
            relief="solid",
            bd=1
        )
        desc_entry.pack(fill="x", pady=(0, 20))
        
        # Two-column layout for options
        options_frame = tk.Frame(content, bg=self.BG_LIGHT)
        options_frame.pack(fill="x", pady=(0, 25))
        
        # Left column - Focus Area
        left_col = tk.Frame(options_frame, bg=self.BG_LIGHT)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        tk.Label(
            left_col, 
            text="Focus Area", 
            font=("Segoe UI", 11),
            bg=self.BG_LIGHT, 
            fg=self.TEXT_PRIMARY,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        focus_areas = ["Career", "Health", "Learning", "Personal", "Finance", "Family", "Social", "General"]
        focus_var = tk.StringVar(value="Career")
        
        focus_combo = ttk.Combobox(
            left_col,
            textvariable=focus_var,
            values=focus_areas,
            font=("Calibri", 11),
            state="readonly",
            width=20
        )
        focus_combo.pack(fill="x")
        
        # Right column - Time Frame
        right_col = tk.Frame(options_frame, bg=self.BG_LIGHT)
        right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        tk.Label(
            right_col, 
            text="Time Frame", 
            font=("Segoe UI", 11),
            bg=self.BG_LIGHT, 
            fg=self.TEXT_PRIMARY,
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        time_frame_var = tk.StringVar(value=time_frame)
        time_frame_combo = ttk.Combobox(
            right_col,
            textvariable=time_frame_var,
            values=["Week", "Month"],
            font=("Calibri", 11),
            state="readonly",
            width=20
        )
        time_frame_combo.pack(fill="x")
        
        # Priority selection
        tk.Label(
            content, 
            text="Priority", 
            font=("Segoe UI", 11),
            bg=self.BG_LIGHT, 
            fg=self.TEXT_PRIMARY,
            anchor="w"
        ).pack(fill="x", pady=(0, 10))
        
        priority_frame = tk.Frame(content, bg=self.BG_LIGHT)
        priority_frame.pack(fill="x", pady=(0, 25))
        
        priority_var = tk.StringVar(value="Medium")
        
        for p in ["High", "Medium", "Low"]:
            color = self.PRIORITY_COLORS[p]["fg"]
            rb = tk.Radiobutton(
                priority_frame,
                text=p,
                variable=priority_var,
                value=p,
                font=("Calibri", 11, "bold"),
                bg=self.BG_LIGHT,
                fg=color,
                selectcolor=self.BG_LIGHT,
                activebackground=self.BG_LIGHT,
                activeforeground=color,
                padx=15
            )
            rb.pack(side="left")
        
        # Buttons
        button_frame = tk.Frame(content, bg=self.BG_LIGHT)
        button_frame.pack(fill="x", pady=(10, 0))
        
        def submit():
            heading = heading_entry.get().strip()
            if not heading:
                messagebox.showerror("Error", "Plan heading is required!", parent=dialog)
                return
            
            description = desc_entry.get().strip()
            focus = focus_var.get()
            priority = priority_var.get()
            time_frame = time_frame_var.get()
            
            # Save to database
            add_plan(heading, description, focus, priority, time_frame)
            
            # Refresh the view
            self.refresh_plans()
            
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        tk.Button(
            button_frame,
            text="Create Plan",
            font=("Segoe UI", 12, "bold"),
            bg=self.ACCENT_GREEN,
            fg="white",
            bd=0,
            padx=25,
            pady=10,
            activebackground="#0ca678",
            activeforeground="white",
            cursor="hand2",
            command=submit
        ).pack(side="left", padx=(0, 10))
        
        tk.Button(
            button_frame,
            text="Cancel",
            font=("Segoe UI", 12),
            bg="#e2e8f0",
            fg=self.TEXT_SECONDARY,
            bd=0,
            padx=25,
            pady=10,
            activebackground="#cbd5e0",
            activeforeground=self.TEXT_PRIMARY,
            cursor="hand2",
            command=cancel
        ).pack(side="left")
        
        # Keyboard shortcuts
        dialog.bind('<Return>', lambda e: submit())
        dialog.bind('<Escape>', lambda e: cancel())
    
    def refresh_plans(self):
        """Refresh both Week and Month tabs"""
        # Clear existing content
        if hasattr(self, 'week_content'):
            for widget in self.week_content.winfo_children():
                widget.destroy()
        if hasattr(self, 'month_content'):
            for widget in self.month_content.winfo_children():
                widget.destroy()
        
        # Get plans from database
        week_plans = list_plans("Week")
        month_plans = list_plans("Month")
        
        # Display week plans
        if week_plans:
            for i, plan in enumerate(week_plans):
                self.create_plan_card(self.week_content, plan, i)
        else:
            self.show_empty_state(self.week_content, "week")
        
        # Display month plans
        if month_plans:
            for i, plan in enumerate(month_plans):
                self.create_plan_card(self.month_content, plan, i)
        else:
            self.show_empty_state(self.month_content, "month")
    
    def create_plan_card(self, parent, plan, index):
        """Create a card to display a plan"""
        # Plan structure: (id, heading, description, focus_area, priority, time_frame, created_at, updated_at, status)
        plan_id = plan[0]
        heading = plan[1]
        description = plan[2] if plan[2] else ""
        focus = plan[3]
        priority = plan[4]
        time_frame = plan[5]
        
        # Card frame
        card = tk.Frame(
            parent,
            bg=self.CARD_BG,
            bd=0,
            relief="flat",
            highlightbackground="#e2e8f0",
            highlightthickness=1
        )
        card.pack(fill="x", padx=5, pady=6)
        
        # Content area
        content = tk.Frame(card, bg=self.CARD_BG)
        content.pack(fill="x", padx=20, pady=15)
        
        # Left side - main content
        left_section = tk.Frame(content, bg=self.CARD_BG)
        left_section.pack(side="left", fill="both", expand=True)
        
        # Title row
        title_row = tk.Frame(left_section, bg=self.CARD_BG)
        title_row.pack(anchor="w", pady=(0, 8))
        
        # Index number
        tk.Label(
            title_row,
            text=f"{index + 1}.",
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_LIGHT
        ).pack(side="left", padx=(0, 8))
        
        # Heading
        tk.Label(
            title_row,
            text=heading,
            font=("Segoe UI", 13, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_PRIMARY
        ).pack(side="left")
        
        # Badges row
        badges_row = tk.Frame(left_section, bg=self.CARD_BG)
        badges_row.pack(anchor="w", pady=(0, 8))
        
        # Focus Area badge
        focus_color = self.FOCUS_COLORS.get(focus, {"bg": "#f1f5f9", "fg": "#475569"})
        focus_badge = tk.Label(
            badges_row,
            text=f"🎯 {focus}",
            font=("Calibri", 10),
            bg=focus_color["bg"],
            fg=focus_color["fg"],
            padx=8,
            pady=2,
            relief="flat"
        )
        focus_badge.pack(side="left", padx=(0, 8))
        
        # Priority badge
        priority_color = self.PRIORITY_COLORS.get(priority, {"bg": "#f1f5f9", "fg": "#475569"})
        priority_icon = "🔴" if priority == "High" else "🟠" if priority == "Medium" else "🔵"
        priority_badge = tk.Label(
            badges_row,
            text=f"{priority_icon} {priority}",
            font=("Calibri", 10, "bold"),
            bg=priority_color["bg"],
            fg=priority_color["fg"],
            padx=8,
            pady=2,
            relief="flat"
        )
        priority_badge.pack(side="left", padx=(0, 8))
        
        # Time frame badge
        time_color = "#7e3af2" if time_frame == "Week" else "#8b5cf6"
        time_badge = tk.Label(
            badges_row,
            text=f"📅 {time_frame}",
            font=("Calibri", 10),
            bg=time_color,
            fg="white",
            padx=8,
            pady=2,
            relief="flat"
        )
        time_badge.pack(side="left")
        
        # Description (if exists)
        if description:
            tk.Label(
                left_section,
                text=description,
                font=("Calibri", 11),
                bg=self.CARD_BG,
                fg=self.TEXT_SECONDARY,
                wraplength=500,
                justify="left",
                anchor="w"
            ).pack(anchor="w", pady=(5, 0))
        
        # Right side - actions
        right_section = tk.Frame(content, bg=self.CARD_BG)
        right_section.pack(side="right", padx=(10, 0))
        
        # Edit button
        edit_btn = tk.Button(
            right_section,
            text="✏️ Edit",
            font=("Segoe UI", 10),
            bg="#f1f5f9",
            fg=self.TEXT_SECONDARY,
            bd=0,
            padx=12,
            pady=4,
            activebackground="#e2e8f0",
            cursor="hand2",
            command=lambda: self.show_edit_dialog(plan)
        )
        edit_btn.pack(side="left", padx=2)
        
        # Delete button
        delete_btn = tk.Button(
            right_section,
            text="🗑️ Delete",
            font=("Segoe UI", 10),
            bg="#fee2e2",
            fg="#b91c1c",
            bd=0,
            padx=12,
            pady=4,
            activebackground="#fecaca",
            cursor="hand2",
            command=lambda: self.delete_plan(plan_id, heading)
        )
        delete_btn.pack(side="left", padx=2)
    
    def show_empty_state(self, parent, time_frame):
        """Show empty state message"""
        empty_frame = tk.Frame(parent, bg=self.BG_LIGHT)
        empty_frame.pack(fill="both", expand=True, pady=60)
        
        # Icon
        icon = "📆" if time_frame == "week" else "📅"
        tk.Label(
            empty_frame,
            text=icon,
            font=("Segoe UI", 48),
            bg=self.BG_LIGHT,
            fg=self.TEXT_LIGHT
        ).pack()
        
        # Message
        frame_name = "week" if time_frame == "week" else "month"
        tk.Label(
            empty_frame,
            text=f"No {frame_name} plans yet",
            font=("Segoe UI", 16, "bold"),
            bg=self.BG_LIGHT,
            fg=self.TEXT_SECONDARY
        ).pack(pady=(10, 5))
        
        tk.Label(
            empty_frame,
            text=f"Click 'Add {frame_name.capitalize()} Plan' to create your first goal",
            font=("Segoe UI", 11),
            bg=self.BG_LIGHT,
            fg=self.TEXT_LIGHT
        ).pack()
    
    def delete_plan(self, plan_id, heading):
        """Delete a plan after confirmation"""
        if messagebox.askyesno(
            "Confirm Delete",
            f'Delete plan "{heading}"?',
            parent=self.window
        ):
            delete_plan(plan_id)
            self.refresh_plans()
    
    def show_edit_dialog(self, plan):
        """Show dialog to edit an existing plan"""
        # To be implemented
        messagebox.showinfo("Coming Soon", "Edit functionality will be added soon!", parent=self.window)