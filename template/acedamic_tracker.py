import json
import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from leveling_system import add_xp

DATA_FILE = "academic_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"dates": [], "completed_topics": [], "pending_topics": [], "study_log": []}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def view_academic_gui(root, username, update_callback=None):
    data = load_data()
    window = tk.Toplevel(root)
    window.title("📚 Academic Tracker")

    def refresh():
        window.destroy()
        view_academic_gui(root, username, update_callback)

    dates_text = "\n".join([f"{d['title']} - {d['date']}" for d in data["dates"]]) or "No important dates"
    tk.Label(window, text="📅 Exam/Project Dates:", font=("Arial", 12, "bold")).pack()
    tk.Label(window, text=dates_text).pack()

    completed = "\n".join(data["completed_topics"]) or "None"
    pending = "\n".join(data["pending_topics"]) or "None"

    tk.Label(window, text="\n✅ Completed Topics:", font=("Arial", 12, "bold")).pack()
    tk.Label(window, text=completed).pack()

    tk.Label(window, text="\n🕒 Pending Topics:", font=("Arial", 12, "bold")).pack()
    tk.Label(window, text=pending).pack()

    def add_date():
        title = simpledialog.askstring("Event", "Enter exam/project title:", parent=window)
        date = simpledialog.askstring("Date", "Enter date (YYYY-MM-DD):", parent=window)
        try:
            datetime.strptime(date, "%Y-%m-%d")
            data["dates"].append({"title": title, "date": date})
            save_data(data)
            refresh()
        except:
            messagebox.showerror("Invalid", "Enter a valid date format.")

    def add_completed():
        topic = simpledialog.askstring("Completed", "Enter completed topic:", parent=window)
        if topic:
            if topic not in data["completed_topics"]:
                data["completed_topics"].append(topic)
            if topic in data["pending_topics"]:
                data["pending_topics"].remove(topic)
            add_xp(username, 15)
            if update_callback:
                update_callback()
            save_data(data)
            refresh()

    def add_pending():
        topic = simpledialog.askstring("Pending", "Enter topic to complete:", parent=window)
        if topic and topic not in data["pending_topics"]:
            data["pending_topics"].append(topic)
            save_data(data)
            refresh()

    tk.Button(window, text="➕ Add Exam/Project Date", command=add_date).pack(pady=2)
    tk.Button(window, text="📌 Add Pending Topic", command=add_pending).pack(pady=2)
    tk.Button(window, text="✅ Add Completed Topic", command=add_completed).pack(pady=2)
    tk.Button(window, text="⏱️ Log Study Session", command=lambda: log_study_session(window, username, update_callback)).pack(pady=5)

def log_study_session(root, username, update_callback=None):
    data = load_data()
    subject = simpledialog.askstring("Study", "What subject did you study?", parent=root)
    if not subject:
        return
    start = time.time()
    messagebox.showinfo("Study", "Timer started! Click OK when done.")
    end = time.time()
    duration = round((end - start) / 60, 2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    data["study_log"].append({
        "subject": subject,
        "duration_min": duration,
        "timestamp": timestamp
    })
    save_data(data)
    add_xp(username, int(duration))  # XP = minutes studied
    if update_callback:
        update_callback()
    messagebox.showinfo("Done", f"{duration} minutes logged. XP gained: {int(duration)}")
