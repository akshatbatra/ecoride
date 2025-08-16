from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests
import os

GOOGLE_MAPS_API_KEY = "" #put api key here

def extract_city_from_geocode(geocode_json):
    for component in geocode_json.get("address_components", []):
        if "locality" in component.get("types", []):
            return component.get("long_name")
    # fallback: try administrative_area_level_2 (often city/district)
    for component in geocode_json.get("address_components", []):
        if "administrative_area_level_2" in component.get("types", []):
            return component.get("long_name")
    return None

@tool(name='get_city_name', description='Gets the city name from a textual location using Google Maps Geocoding API')
def get_city_name(location_text: str) -> str:
    """
    Given a textual location (e.g., from Google Maps autocomplete), returns the city name.
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location_text,
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Google Maps API error: {response.status_code}")
    data = response.json()
    if not data.get("results"):
        return None
    city = extract_city_from_geocode(data["results"][0])
    return city