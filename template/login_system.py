import hashlib
import json
import os

USER_FILE = "users.json"

# Load users from file
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

# Save users to file
def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Hash password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register new user (returns message)
def register_user(username, password):
    users = load_users()
    if username in users:
        return "⚠️ Username already exists."
    users[username] = hash_password(password)
    save_users(users)
    return "✅ Registration successful!"

# Login user (returns True/False)
def login_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    return users.get(username) == hashed
