"""
تحديث ملف home.html لإضافة headers للمصادقة في جميع طلبات API
Update home.html to add authentication headers to all API requests
"""

import re

# Read the original file
with open(r'c:\Users\AREF ABDERAHMAN\Desktop\tp final\templates\home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update patterns - إضافة headers لجميع طلبات fetch
updates = [
    # loadPatients function
    (
        r"(async function loadPatients\(\) \{[\s\S]*?const response = await fetch\(')(/api/patients)('\);)",
        r"\1\2', {\n                headers: getAuthHeaders()\n            });"
    ),
    # loadNotifications function
    (
        r"(async function loadNotifications\(\) \{[\s\S]*?const response = await fetch\(')(/api/notifications)('\);)",
        r"\1\2', {\n                headers: getAuthHeaders()\n            });"
    ),
    # loadReports function
    (
        r"(async function loadReports\(\) \{[\s\S]*?const response = await fetch\(')(/api/reports)('\);)",
        r"\1\2', {\n                headers: getAuthHeaders()\n            });"
    ),
    # loadPrescriptions function
    (
        r"(async function loadPrescriptions\(\) \{[\s\S]*?const response = await fetch\(')(/api/prescriptions)('\);)",
        r"\1\2', {\n                headers: getAuthHeaders()\n            });"
    ),
    # create patient
    (
        r"(const response = await fetch\(')(/api/patients)(', \{[\s\S]*?method: 'POST',)",
        r"\1\2\3\n                headers: getAuthHeaders(),"
    ),
    # get patient by ID
    (
        r"(const response = await fetch\(`/api/patients/\$\{patient_id\}`\);)",
        r"const response = await fetch(`/api/patients/${patient_id}`, {\n                headers: getAuthHeaders()\n            });"
    ),
    # update patient
    (
        r"(const response = await fetch\(`/api/patients/\$\{patientId\}`, \{[\s\S]*?method: 'PUT',)",
        r"\1\n                headers: getAuthHeaders(),"
    ),
    # delete patient
    (
        r"(const response = await fetch\(`/api/patients/\$\{patientId\}`, \{[\s\S]*?method: 'DELETE'[\s\S]*?\}\);)",
        r"const response = await fetch(`/api/patients/${patientId}`, {\n                method: 'DELETE',\n                headers: getAuthHeaders()\n            });"
    ),
    # create report
    (
        r"(const response = await fetch\(')(/api/reports)(', \{[\s\S]*?method: 'POST',)",
        r"\1\2\3\n                headers: getAuthHeaders(),"
    ),
    # create prescription
    (
        r"(const response = await fetch\(')(/api/prescriptions)(', \{[\s\S]*?method: 'POST',)",
        r"\1\2\3\n                headers: getAuthHeaders(),"
    ),
]

# Apply updates
for pattern, replacement in updates:
    if re.search(pattern, content):
        content = re.sub(pattern, replacement, content)
        print(f"✓ Updated pattern: {pattern[:50]}...")
    else:
        print(f"✗ Pattern not found: {pattern[:50]}...")

# Write updated content
with open(r'c:\Users\AREF ABDERAHMAN\Desktop\tp final\templates\home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ home.html updated successfully!")
