import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models"

try:
    response = requests.get(f"{API_URL}?key={API_KEY}", timeout=10)
    if response.status_code == 200:
        models = response.json().get('models', [])
        with open("models.txt", "w") as f:
            for m in models:
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    f.write(f"{m['name']}\n")
        print("Models written to models.txt")
    else:
        print(f"Error: {response.status_code} {response.text}")
except Exception as e:
    print(f"Exception: {e}")
