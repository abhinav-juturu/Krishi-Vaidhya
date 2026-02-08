import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODELS_TO_TEST = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]

for model in MODELS_TO_TEST:
    print(f"Testing {model}...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Hello, explain how AI works in 5 words."}]
        }]
    }
    
    try:
        response = requests.post(
            f"{url}?key={API_KEY}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("SUCCESS!")
            print(response.json())
            break
        else:
            print(f"Failed: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
    print("-" * 30)
