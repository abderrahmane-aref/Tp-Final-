# Test Notifications Feature
# Run this to add some test notifications

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Add a test notification
cur.execute(
    "INSERT INTO notifications (title, message) VALUES (?, ?)",
    ("System Ready", "Medical Records System is now online and ready to use!")
)

conn.commit()
conn.close()

print("✅ Test notification added!")
print("🌐 Open http://localhost:8000 and click on Notifications to see it")
