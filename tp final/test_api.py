import requests

# Test adding a user
url = "http://localhost:8000/api/admin/users"
headers = {
    "X-User-Role": "Admin",
    "X-User-Name": "admin"
}
data = {
    "username": "testnurse",
    "password": "testpass",
    "role": "Nurse"
}

response = requests.post(url, headers=headers, data=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")