import os
import requests

API_KEY = "81af5f756d664b44960cb3edc0830425"
BASE_URL = "https://api.rentcast.io/v1"

def get_property_record(address: str):
    url = f"{BASE_URL}/properties"
    params = {"address": address}
    headers = {
        "X-Api-Key": API_KEY,
        "Accept": "application/json"
    }
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    address = "5500 Grand Lake Dr, San Antonio, TX 78244"
    try:
        data = get_property_record(address)
        print("Formatted Address:", data.get("formattedAddress"))
        print("Assessor ID:", data.get("assessorID"))
        print("Last Sale Date:", data.get("lastSaleDate"))
        print("Last Sale Price:", data.get("lastSalePrice"))
        print("Owner Names:", data.get("owner", {}).get("names"))
        print("AVM (if available):", data.get("avm", {}).get("value"))
    except requests.HTTPError as e:
        print("HTTP error:", e, e.response.text)
