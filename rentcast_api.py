"""
RentCast API integration for property data retrieval
"""

import os
import requests
from typing import Dict, Optional
import streamlit as st
import logging

RENTCAST_API_BASE_URL = "https://api.rentcast.io/v1"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RentCastAPI:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RENTCAST_API_KEY")
        self.headers = {
            "Accept": "application/json",
            "X-Api-Key": self.api_key
        }

    def lookup_by_address(self, address: str) -> Dict:
        url = f"{RENTCAST_API_BASE_URL}/properties"
        params = {"address": address}
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=20)
            logger.info(f"RentCast API address lookup status: {resp.status_code}")
            logger.info(f"RentCast API address lookup response: {resp.text}")
            if resp.status_code == 200:
                data = resp.json()
                # If response is a list, return the first property
                if isinstance(data, list) and data:
                    logger.info(f"RentCast API returned a list with {len(data)} items. Using the first.")
                    return data[0]
                # If response is a dict with 'properties', return the first property
                if isinstance(data, dict) and data.get("properties"):
                    logger.info(f"RentCast API returned a dict with 'properties'. Using the first.")
                    return data["properties"][0]
                st.warning("No property found for this address.")
                return {}
            else:
                st.error(f"RentCast API error: {resp.status_code} - {resp.text}")
                return {}
        except Exception as e:
            st.error(f"Error calling RentCast API: {str(e)}")
            logger.error(f"Error calling RentCast API: {str(e)}")
            return {}

    def lookup_by_apn(self, apn: str) -> Dict:
        url = f"{RENTCAST_API_BASE_URL}/properties"
        params = {"parcel_number": apn}
        try:
            resp = requests.get(url, headers=self.headers, params=params, timeout=20)
            logger.info(f"RentCast API APN lookup status: {resp.status_code}")
            logger.info(f"RentCast API APN lookup response: {resp.text}")
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and data:
                    logger.info(f"RentCast API returned a list with {len(data)} items. Using the first.")
                    return data[0]
                if isinstance(data, dict) and data.get("properties"):
                    logger.info(f"RentCast API returned a dict with 'properties'. Using the first.")
                    return data["properties"][0]
                st.warning("No property found for this APN.")
                return {}
            else:
                st.error(f"RentCast API error: {resp.status_code} - {resp.text}")
                return {}
        except Exception as e:
            st.error(f"Error calling RentCast API: {str(e)}")
            logger.error(f"Error calling RentCast API: {str(e)}")
            return {}

def fetch_rentcast_property(address: str = None, apn: str = None) -> Dict:
    api = RentCastAPI()
    if not api.api_key:
        st.error("❌ RentCast API key not found. Please add RENTCAST_API_KEY to your .env file.")
        return {}
    if address:
        return api.lookup_by_address(address)
    elif apn:
        return api.lookup_by_apn(apn)
    else:
        st.error("❌ No address or APN provided.")
        return {}