import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui_helper import apply_theme

DB_NAME = "app.db"

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FocusFlow | Login")
        self.root.state("zoomed")
        self.root.minsize(900, 600)

        tk.Label(root, text="FocusFlow", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(root, text="Login to continue").pack()

        tk.Label(root, text="Username").pack(pady=(20, 5))
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack(pady=(10, 5))
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", width=15, command=self.login).pack(pady=10)
        

        tk.Button(
            root,
            text="Create New Account",
            command=self.open_signup
        ).pack()
        


        apply_theme(root)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            self.root.destroy()
            import dashboard
            dashboard.open_dashboard(user[0])
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def open_signup(self):
        self.root.destroy()
        import signup
        signup.main()

def main():
    root = tk.Tk()
    LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
