import requests

# Test login
url = "http://localhost:8000/login"
data = {
    "username": "testnurse",
    "password": "testpass"
}

response = requests.post(url, data=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")