import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui_helper import apply_theme

DB_NAME = "app.db"

class SignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FocusFlow | Sign Up")
        self.root.state("zoomed")
        self.root.minsize(900, 600)

        tk.Label(root, text="FocusFlow", font=("Arial", 22, "bold")).pack(pady=10)
        tk.Label(root, text="Create a new account").pack(pady=5)

        frame = tk.Frame(root)
        frame.pack(pady=40)

        tk.Label(frame, text="Username").grid(row=0, column=0, pady=5, sticky="e")
        self.username = tk.Entry(frame, width=30)
        self.username.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password").grid(row=1, column=0, pady=5, sticky="e")
        self.password = tk.Entry(frame, width=30, show="*")
        self.password.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Confirm Password").grid(row=2, column=0, pady=5, sticky="e")
        self.confirm = tk.Entry(frame, width=30, show="*")
        self.confirm.grid(row=2, column=1, pady=5)

        tk.Button(
            root,
            text="Sign Up",
            width=18,
            command=self.signup
        ).pack(pady=20)

        tk.Button(
            root,
            text="Back to Login",
            command=self.back_to_login
        ).pack()

        apply_theme(root)

    def connect(self):
        return sqlite3.connect(DB_NAME)

    def signup(self):
        username = self.username.get().strip()
        password = self.password.get()
        confirm = self.confirm.get()

        if not username or not password or not confirm:
            messagebox.showerror("Error", "All fields are required")
            return

        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account created successfully!")
            self.back_to_login()

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def back_to_login(self):
        self.root.destroy()
        import login
        login.main()


def main():
    root = tk.Tk()
    SignupApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
