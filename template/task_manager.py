import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os
from leveling_system import add_xp

TASK_FILE = "tasks.json"


def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data
            else:
                return {}  # fallback if corrupted
    return {}

def save_tasks(data):
    with open(TASK_FILE, "w") as file:
        json.dump(data, file, indent=4)

def view_tasks_gui(root, username, update_callback=None):
    tasks = load_tasks().get(username, [])
    window = tk.Toplevel(root)
    window.title("📋 Task Manager")

    def refresh():
        window.destroy()
        view_tasks_gui(root, username, update_callback)

    for idx, task in enumerate(tasks):
        status = "✅" if task["done"] else "❌"
        tk.Label(window, text=f"{idx+1}. {task['text']} - {status}").pack()

    def add_task():
        text = simpledialog.askstring("New Task", "Enter task:", parent=window)
        if text:
            tasks.append({"text": text, "done": False})
            data = load_tasks()
            data[username] = tasks
            save_tasks(data)
            refresh()

    def complete_task():
        index = simpledialog.askinteger("Complete Task", "Enter task number to complete:", parent=window)
        if index and 0 < index <= len(tasks):
            tasks[index - 1]["done"] = True
            add_xp(username, 10)  # 🎁 XP reward
            if update_callback:
                update_callback()
            data = load_tasks()
            data[username] = tasks
            save_tasks(data)
            refresh()
        else:
            messagebox.showerror("Error", "Invalid task number")

    tk.Button(window, text="➕ Add Task", command=add_task).pack(pady=2)
    tk.Button(window, text="✅ Complete Task", command=complete_task).pack(pady=2)
