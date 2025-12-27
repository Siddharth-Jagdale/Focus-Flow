import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from tkcalendar import Calendar
from ui_helper import apply_theme

DB_NAME = "app.db"


class TaskApp:
    def __init__(self, user_id):
        self.user_id = user_id

        self.root = tk.Tk()
        self.root.title("FocusFlow | Tasks")
        self.root.state("zoomed")
        self.root.minsize(900, 600)

        tk.Label(
            self.root,
            text="Task Manager",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Entry Frame
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Task").grid(row=0, column=0, padx=5)
        self.task_entry = tk.Entry(frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=10)

        tk.Label(frame, text="Priority").grid(row=0, column=2)
        self.priority_cb = ttk.Combobox(
            frame,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=15
        )
        self.priority_cb.current(0)
        self.priority_cb.grid(row=0, column=3, padx=10)

        tk.Label(frame, text="Due Date").grid(row=1, column=0, pady=10)
        self.due_entry = tk.Entry(frame, width=20)
        self.due_entry.grid(row=1, column=1, padx=10)

        tk.Button(
            frame,
            text="📅 Pick Date",
            command=self.open_calendar
        ).grid(row=1, column=2, padx=5)

        tk.Button(
            frame,
            text="Add Task",
            command=self.add_task
        ).grid(row=2, column=1, pady=15)

                # -------- FILTER & SORT BAR --------
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Filter by Priority:").grid(row=0, column=0, padx=5)

        self.filter_priority = ttk.Combobox(
            filter_frame,
            values=["All", "Low", "Medium", "High"],
            state="readonly",
            width=12
        )
        self.filter_priority.current(0)
        self.filter_priority.grid(row=0, column=1, padx=5)

        tk.Button(
            filter_frame,
            text="Apply Filter",
            command=self.load_tasks
        ).grid(row=0, column=2, padx=10)

        tk.Label(filter_frame, text="Sort by Due Date:").grid(row=0, column=3, padx=5)

        self.sort_order = ttk.Combobox(
            filter_frame,
            values=["Ascending", "Descending"],
            state="readonly",
            width=12
        )
        self.sort_order.current(0)
        self.sort_order.grid(row=0, column=4, padx=5)


        # Table
        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Task", "Priority", "Status", "Due"),
            show="headings"
        )

        for col in ("ID", "Task", "Priority", "Status", "Due"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Mark as Done",
            command=self.mark_done
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Delete Task",
            fg="red",
            command=self.delete_task
        ).grid(row=0, column=1, padx=10)

        self.load_tasks()
        apply_theme(self.root)
        self.root.mainloop()

    # ---------- DATE PICKER ----------
    def open_calendar(self):
        top = tk.Toplevel(self.root)
        top.title("Select Due Date")
        top.grab_set()

        cal = Calendar(
            top,
            selectmode="day",
            date_pattern="yyyy-mm-dd"
        )
        cal.pack(padx=20, pady=20)

        def set_date():
            self.due_entry.delete(0, tk.END)
            self.due_entry.insert(0, cal.get_date())
            top.destroy()

        tk.Button(top, text="Select", command=set_date).pack(pady=10)

    # ---------- DATABASE ----------
    def connect(self):
        return sqlite3.connect(DB_NAME)

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_cb.get()
        due = self.due_entry.get()

        if not task or not due:
            messagebox.showerror("Error", "Task and Due Date required")
            return

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (user_id, title, priority, status, due_date)
            VALUES (?, ?, ?, 'Pending', ?)
        """, (self.user_id, task, priority, due))

        conn.commit()
        conn.close()

        self.task_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)

        self.load_tasks()

    def load_tasks(self):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        priority = self.filter_priority.get()
        order = self.sort_order.get()

        query = """
            SELECT id, title, priority, status, due_date
            FROM tasks
            WHERE user_id=?
        """
        params = [self.user_id]

        # Apply priority filter
        if priority != "All":
            query += " AND priority=?"
            params.append(priority)

        # Apply sorting
        if order == "Ascending":
            query += " ORDER BY due_date ASC"
        else:
            query += " ORDER BY due_date DESC"

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)

        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

        conn.close()

    def mark_done(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a task")
            return

        task_id = self.tree.item(selected[0])["values"][0]

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status='Done' WHERE id=?",
            (task_id,)
        )
        conn.commit()
        conn.close()

        self.load_tasks()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a task")
            return

        task_id = self.tree.item(selected[0])["values"][0]

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

        self.load_tasks()


def open_tasks(user_id):
    TaskApp(user_id)
