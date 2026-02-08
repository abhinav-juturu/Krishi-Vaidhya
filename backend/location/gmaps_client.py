# kvb/location/location_service.py
from .gmaps_client import reverse_geocode


def extract_location_components(geo_json: dict) -> dict:
    components = geo_json["results"][0]["address_components"]

    def get(type_name):
        for c in components:
            if type_name in c["types"]:
                return c["long_name"]
        return None

    return {
        "village": get("locality") or get("sublocality"),
        "district": get("administrative_area_level_2"),
        "state": get("administrative_area_level_1")
    }


def normalize_location(lat: float, lng: float) -> dict:
    geo_json = reverse_geocode(lat, lng)

    location = extract_location_components(geo_json)

    return {
        "lat": lat,
        "lng": lng,
        **location
    }
