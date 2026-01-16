"""
تحديث دالة editPatient لإضافة headers
Update editPatient function to add headers
"""

import re

# Read the file
with open(r'c:\Users\AREF ABDERAHMAN\Desktop\tp final\templates\home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix editPatient function
pattern = r'(async function editPatient\(patientId\) \{\s+try \{\s+const response = await fetch\(`/api/patients/\$\{patientId\}`\);)'
replacement = r'async function editPatient(patientId) {\n        try {\n            const response = await fetch(`/api/patients/${patientId}`, {\n                headers: getAuthHeaders()\n            });'

if re.search(pattern, content):
    content = re.sub(pattern, replacement, content)
    print("✓ Updated editPatient function")
else:
    print("✗ editPatient pattern not found")

# Write back
with open(r'c:\Users\AREF ABDERAHMAN\Desktop\tp final\templates\home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Update complete!")
