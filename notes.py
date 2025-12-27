import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from ui_helper import apply_theme

DB_NAME = "app.db"

class NotesApp:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.title("FocusFlow | Notes")
        self.root.state("zoomed")
        self.root.minsize(900, 600)

        tk.Label(self.root, text="Notes Manager", font=("Arial", 18, "bold")).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Title").grid(row=0, column=0)
        self.title = tk.Entry(frame, width=30)
        self.title.grid(row=0, column=1, padx=10)

        tk.Label(frame, text="Category").grid(row=0, column=2)
        self.category = tk.Entry(frame, width=20)
        self.category.grid(row=0, column=3)

        tk.Label(frame, text="Content").grid(row=1, column=0)
        self.content = tk.Entry(frame, width=70)
        self.content.grid(row=1, column=1, columnspan=3, pady=5)

        tk.Button(frame, text="Add Note", command=self.add_note).grid(row=2, column=1)
        

        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Title", "Category", "Date"),
            show="headings"
        )
        for c in ("ID", "Title", "Category", "Date"):
            self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True)

        tk.Button(self.root, text="Delete Selected",
                  fg="red", command=self.delete_note).pack(pady=10)
                  

        self.load_notes()
        apply_theme(self.root)
        self.root.mainloop()

    def connect(self):
        return sqlite3.connect(DB_NAME)

    def add_note(self):
        if not self.title.get() or not self.content.get():
            messagebox.showerror("Error", "Title and content required")
            return

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes VALUES (NULL,?,?,?,?,?)",
            (self.user_id, self.title.get(), self.content.get(),
             self.category.get(), datetime.now().strftime("%Y-%m-%d %H:%M"))
        )
        conn.commit()
        conn.close()
        self.load_notes()

    def load_notes(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT id,title,category,created_at FROM notes WHERE user_id=?",
            (self.user_id,)
        )
        for r in cur.fetchall():
            self.tree.insert("", "end", values=r)
        conn.close()

    def delete_note(self):
        sel = self.tree.selection()
        if sel:
            nid = self.tree.item(sel[0])["values"][0]
            conn = self.connect()
            conn.execute("DELETE FROM notes WHERE id=?", (nid,))
            conn.commit()
            conn.close()
            self.load_notes()

def open_notes(user_id):
    NotesApp(user_id)
