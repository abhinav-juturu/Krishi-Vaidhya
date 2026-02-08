
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    try:
        response = requests.get(BASE_URL)
        print(f"Home: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Home failed: {e}")

def test_login():
    url = f"{BASE_URL}/api/users/login"
    data = {
        "phone": "9876543210",
        "name": "Test User",
        "language": "en",
        "crops": ["Wheat"]
    }
    try:
        response = requests.post(url, json=data)
        print(f"Login: {response.status_code}")
        print(response.json())
    except Exception as e:
        print(f"Login failed: {e}")

if __name__ == "__main__":
    print("Testing Backend API...")
    test_home()
    test_login()
