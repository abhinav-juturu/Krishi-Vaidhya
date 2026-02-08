import requests

API_KEY = "YOUR_API_KEY"

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    "location": "11.0168,76.9558",  # Coimbatore
    "radius": 3000,
    "keyword": "agriculture store",
    "key": API_KEY
}

res = requests.get(url, params=params)
print(res.json()["status"])
