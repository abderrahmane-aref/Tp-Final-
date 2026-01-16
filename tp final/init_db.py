import sqlite3
import os

# CREATE/USE database.db in the same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# users table (three users: doctor, nurse, pharma)
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
''')

# patients table
cur.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    dob TEXT,
    sex TEXT,
    last_visit TEXT,
    visit_place TEXT,
    notes TEXT
)
''')

# notifications table
cur.execute('''
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read INTEGER DEFAULT 0
)
''')

# reports table (medical reports)
cur.execute('''
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    report_type TEXT NOT NULL,
    diagnosis TEXT,
    treatment TEXT,
    medications TEXT,
    notes TEXT,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
)
''')

# prescriptions table (for doctors to add prescriptions)
cur.execute('''
CREATE TABLE IF NOT EXISTS prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    medication_name TEXT NOT NULL,
    dosage TEXT NOT NULL,
    frequency TEXT NOT NULL,
    duration TEXT NOT NULL,
    instructions TEXT,
    prescribed_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
)
''')

# Insert default users (ignore errors if they already exist)
users = [
    ("doctor", "1111", "Doctor"),
    ("nurse", "nurse123", "Nurse"),
    ("pharma", "pharma123", "Pharmacist"),
    ("admin", "admin123", "Admin"),
    ("Marwa", "marwa", "Nurse"), 
]
for u in users:
    try:
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", u)
    except sqlite3.IntegrityError:
        # user already exists, ignore
        pass

# Optional: insert a couple of example patients
example_patients = [
    ("John", "Doe", "1990-05-12", "Male", "2025-12-06", "Clinic A", "No notes"),
    ("Jane", "Smith", "1995-08-20", "Female", "2025-12-05", "Clinic B", "Allergic to penicillin")
]

for p in example_patients:
    cur.execute(
        "SELECT COUNT(*) FROM patients WHERE first_name=? AND last_name=? AND dob=?",
        (p[0], p[1], p[2])
    )
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO patients (first_name, last_name, dob, sex, last_visit, visit_place, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            p
        )

conn.commit()
conn.close()

print("Database initialized at:", DB_PATH)
