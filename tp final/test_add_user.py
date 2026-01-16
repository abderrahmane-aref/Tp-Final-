import sqlite3
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_user_to_db(username, password, role):
    """Add new user to database"""
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        raise Exception("Username already exists")

# Test adding a new nurse
try:
    user_id = add_user_to_db("nurse2", "nursepass", "Nurse")
    print(f"Successfully added user with ID: {user_id}")
except Exception as e:
    print(f"Error adding user: {e}")

# Check all users
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("\nCurrent users in database:")
print("ID | Username | Password | Role")
print("-" * 40)
for user in users:
    print(f"{user[0]} | {user[1]} | {user[2]} | {user[3]}")

conn.close()