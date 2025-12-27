import tkinter as tk
import sqlite3
from exporter import export_notes, export_tasks
from ui_helper import apply_theme
import theme

DB_NAME = "app.db"

def open_dashboard(user_id):
    root = tk.Tk()
    root.title("FocusFlow | Dashboard")
    root.state("zoomed")
    root.minsize(900, 600)

    top_bar = tk.Frame(root)
    top_bar.pack(fill="x", padx=10)

    tk.Label(top_bar, text="FocusFlow Dashboard", font=("Arial", 20, "bold")).pack(side="left")

    profile_btn = tk.Button(
        top_bar,
        text="👤",
        font=("Arial", 14),
        command=lambda: open_profile_popup(root, user_id)
    )
    profile_btn.pack(side="right")
    


    summary = tk.Frame(root)
    summary.pack(pady=20)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM notes WHERE user_id=?", (user_id,))
    notes_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id=?", (user_id,))
    tasks_count = cursor.fetchone()[0]
    conn.close()

    tk.Label(summary, text=f"📝 Notes: {notes_count}").grid(row=0, column=0, padx=20)
    tk.Label(summary, text=f"✅ Tasks: {tasks_count}").grid(row=0, column=1, padx=20)

    btns = tk.Frame(root)
    btns.pack(pady=40)

    tk.Button(btns, text="Notes Manager", width=18,
              command=lambda: open_notes(user_id)).grid(row=0, column=0, padx=10)
              
    tk.Button(btns, text="Task Manager", width=18,
              command=lambda: open_tasks(user_id)).grid(row=0, column=1, padx=10)
              

    tk.Button(btns, text="Export Notes 📤",
              command=lambda: export_notes(user_id)).grid(row=1, column=0, pady=10)
              
    tk.Button(btns, text="Export Tasks 📤",
              command=lambda: export_tasks(user_id)).grid(row=1, column=1, pady=10)
              

   

    apply_theme(root)
    root.mainloop()

def toggle_all(root):
    theme.toggle()
    apply_theme(root)

def open_notes(user_id):
    import notes
    notes.open_notes(user_id)

def open_tasks(user_id):
    import tasks
    tasks.open_tasks(user_id)

def logout(root):
    root.destroy()
    import login
    login.main()

def open_profile_popup(parent, user_id):
    popup = tk.Toplevel(parent)
    popup.overrideredirect(True)
    popup.geometry("250x180")

    popup.update_idletasks()

    start_y = parent.winfo_y() + 40
    end_y = parent.winfo_y() + 80
    x = parent.winfo_x() + parent.winfo_width() - 260

    popup.geometry(f"+{x}+{start_y}")

    popup.grab_set()

    # Fetch username
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id=?", (user_id,))
    username = cursor.fetchone()[0]
    conn.close()

    tk.Label(popup, text="👤 Profile", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(popup, text=f"Username: {username}").pack(pady=5)

    tk.Frame(popup, height=1).pack(fill="x", pady=5)

    tk.Button(
        popup,
        text="Toggle Theme",
        command=lambda: [toggle_all(parent), popup.destroy()]
    ).pack(pady=5)
    

    tk.Button(
        popup,
        text="Logout",
        fg="red",
        command=lambda: [popup.destroy(), logout(parent)]
    ).pack(pady=5)
    

    apply_theme(popup)

    animate_popup(popup, x, start_y, end_y)

def animate_popup(win, x, current_y, target_y):
    if current_y < target_y:
        current_y += 5
        win.geometry(f"+{x}+{current_y}")
        win.after(10, lambda: animate_popup(win, x, current_y, target_y))

def add_hover_effect(widget):
    def on_enter(e):
        widget.configure(relief="raised")

    def on_leave(e):
        widget.configure(relief="flat")

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)
