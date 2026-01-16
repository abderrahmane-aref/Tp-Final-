import sqlite3
import os

# Database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

print("Current users in database:")
print("ID | Username | Password | Role")
print("-" * 40)
for user in users:
    print(f"{user[0]} | {user[1]} | {user[2]} | {user[3]}")

conn.close()