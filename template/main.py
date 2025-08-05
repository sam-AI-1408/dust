import tkinter as tk
from tkinter import messagebox, ttk
from login_system import register_user, login_user
from task_manager import view_tasks_gui
from acedamic_tracker import view_academic_gui, log_study_session
from leveling_system import get_level, get_current_xp

# Global current user
current_user = {"username": None}

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Academic Assistant")
        self.root.geometry("500x400")
        self.level_label = None
        self.main_menu()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Sam AI", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Login", command=self.login_page, width=20).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_page, width=20).pack(pady=10)

    def register_page(self):
        self.clear_screen()
        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=10)
        username = tk.Entry(self.root)
        password = tk.Entry(self.root, show="*")
        username.pack(pady=5)
        password.pack(pady=5)

        def do_register():
            result = register_user(username.get(), password.get())
            messagebox.showinfo("Result", result)
            self.main_menu()

        tk.Button(self.root, text="Register", command=do_register).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def login_page(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)
        username = tk.Entry(self.root)
        password = tk.Entry(self.root, show="*")
        username.pack(pady=5)
        password.pack(pady=5)

        def do_login():
            if login_user(username.get(), password.get()):
                current_user["username"] = username.get()
                self.dashboard()
            else:
                messagebox.showerror("Error", "Invalid login")

        tk.Button(self.root, text="Login", command=do_login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack()

    def update_dashboard(self):
        if self.level_label:
            level = get_level(current_user['username'])
            xp = get_current_xp(current_user['username'])
            self.level_label.config(text=f"Level: {level} | XP: {xp}")

    def dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Hello, {current_user['username']}", font=("Arial", 16)).pack(pady=10)

        self.level_label = tk.Label(self.root, text="")
        self.level_label.pack()
        self.update_dashboard()

        # Pass update callback to submodules so they can refresh XP/level
        tk.Button(
            self.root, text="📋 Task Manager",
            command=lambda: view_tasks_gui(self.root, current_user["username"], self.update_dashboard)
        ).pack(pady=5)

        tk.Button(
            self.root, text="📚 Academic Tracker",
            command=lambda: view_academic_gui(self.root, current_user["username"], self.update_dashboard)
        ).pack(pady=5)

        tk.Button(
            self.root, text="⏱️ Log Study Session",
            command=lambda: log_study_session(self.root, current_user["username"], self.update_dashboard)
        ).pack(pady=5)

        tk.Button(self.root, text="🚪 Logout", command=self.main_menu).pack(pady=20)

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
