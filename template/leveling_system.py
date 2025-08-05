import json
import os

LEVEL_FILE = "levels.json"

def load_levels():
    if os.path.exists(LEVEL_FILE):
        with open(LEVEL_FILE, "r") as file:
            return json.load(file)
    return {}

def save_levels(data):
    with open(LEVEL_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_level(username):
    levels = load_levels()
    return levels.get(username, {}).get("level", 1)

def get_current_xp(username):
    levels = load_levels()
    return levels.get(username, {}).get("xp", 0)

def xp_needed(level):
    return 100 * level

def add_xp(username, amount):
    levels = load_levels()
    if username not in levels:
        levels[username] = {"level": 1, "xp": 0}

    user_data = levels[username]
    user_data["xp"] += amount

    while user_data["xp"] >= xp_needed(user_data["level"]):
        user_data["xp"] -= xp_needed(user_data["level"])
        user_data["level"] += 1
        print(f"🎉 {username} leveled up to {user_data['level']}!")

    save_levels(levels)
