"""
BatchData API integration for property data retrieval
"""

import requests
import json
import os
import logging
from typing import Dict, List, Optional
import streamlit as st

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchDataAPI:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BATCHDATA_API_KEY")
        self.base_url = "https://api.batchdata.com/api/v1"
        
        # BatchData API uses different authentication methods
        # Try both Bearer token and API key in headers
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Add API key to headers (BatchData might use this format)
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'
            # Also try as API key header
            self.headers['X-API-Key'] = self.api_key
            # And as a simple header
            self.headers['api-key'] = self.api_key
        
        logger.info(f"Initialized BatchData API with key: {self.api_key[:10] if self.api_key else 'None'}...")
        logger.info(f"Headers: {dict(self.headers)}")
    
    def search_property(self, query: str) -> Dict:
        """
        Search for properties using BatchData Property Search API
        """
        url = f"{self.base_url}/property/search"
        
        payload = {
            "searchCriteria": {
                "query": query
            },
            "options": {
                "useYearBuilt": True,
                "skip": 0,
                "take": 5
            }
        }
        
        logger.info(f"Searching property with query: {query}")
        logger.info(f"URL: {url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            logger.info(f"Search response status: {response.status_code}")
            logger.info(f"Search response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                logger.error(f"Search failed with status {response.status_code}")
                logger.error(f"Response text: {response.text}")
                st.error(f"Search failed: {response.status_code} - {response.text}")
                return {}
            
            response.raise_for_status()
            result = response.json()
            logger.info(f"Search successful, found {len(result.get('results', {}).get('properties', []))} properties")
            return result
        except Exception as e:
            logger.error(f"Error searching property: {str(e)}")
            st.error(f"Error searching property: {str(e)}")
            return {}
    
    def lookup_property_by_address(self, address: Dict) -> Dict:
        """
        Lookup property details using BatchData Property Lookup API
        """
        url = f"{self.base_url}/property/lookup/all-attributes"
        
        payload = {
            "requests": [
                {
                    "address": address
                }
            ]
        }
        
        logger.info(f"Looking up property by address: {address}")
        logger.info(f"URL: {url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            logger.info(f"Lookup response status: {response.status_code}")
            logger.info(f"Lookup response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                logger.error(f"Lookup failed with status {response.status_code}")
                logger.error(f"Response text: {response.text}")
                st.error(f"Lookup failed: {response.status_code} - {response.text}")
                return {}
            
            response.raise_for_status()
            result = response.json()
            logger.info(f"Lookup successful, found {len(result.get('results', {}).get('properties', []))} properties")
            return result
        except Exception as e:
            logger.error(f"Error looking up property: {str(e)}")
            st.error(f"Error looking up property: {str(e)}")
            return {}
    
    def lookup_property_by_apn(self, apn: str, state: str = "AZ") -> Dict:
        """
        Lookup property details by APN using BatchData Property Lookup API
        """
        url = f"{self.base_url}/property/lookup/all-attributes"
        
        payload = {
            "requests": [
                {
                    "apn": apn,
                    "state": state
                }
            ]
        }
        
        logger.info(f"Looking up property by APN: {apn}, state: {state}")
        logger.info(f"URL: {url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            logger.info(f"APN lookup response status: {response.status_code}")
            logger.info(f"APN lookup response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                logger.error(f"APN lookup failed with status {response.status_code}")
                logger.error(f"Response text: {response.text}")
                st.error(f"APN lookup failed: {response.status_code} - {response.text}")
                return {}
            
            response.raise_for_status()
            result = response.json()
            logger.info(f"APN lookup successful, found {len(result.get('results', {}).get('properties', []))} properties")
            return result
        except Exception as e:
            logger.error(f"Error looking up property by APN: {str(e)}")
            st.error(f"Error looking up property by APN: {str(e)}")
            return {}
    
    def parse_property_data(self, api_response: Dict) -> Dict:
        """
        Parse BatchData API response into our standardized format
        """
        logger.info("Parsing property data from API response")
        
        if not api_response or 'results' not in api_response:
            logger.warning("No results found in API response")
            return {}
        
        properties = api_response.get('results', {}).get('properties', [])
        if not properties:
            logger.warning("No properties found in results")
            return {}
        
        logger.info(f"Found {len(properties)} properties, using first one")
        
        # Get the first property
        prop = properties[0]
        
        # Extract owner information
        owner_data = {}
        if 'owner' in prop:
            owner = prop['owner']
            owner_data = {
                "owner_name": owner.get('fullName', 'Unknown'),
                "mailing_address": self._format_address(owner.get('mailingAddress', {})),
                "owner_type": owner.get('ownerStatusType', 'Unknown'),
                "owner_occupied": owner.get('ownerOccupied', False)
            }
            logger.info(f"Extracted owner: {owner_data['owner_name']}")
        
        # Extract assessment/valuation information
        valuation_data = {}
        if 'assessment' in prop:
            assessment = prop['assessment']
            valuation_data = {
                "total_value": assessment.get('totalMarketValue', 0),
                "land_value": assessment.get('assessedLandValue', 0),
                "improvement_value": assessment.get('assessedImprovementValue', 0),
                "assessment_year": assessment.get('assessmentYear', 'Unknown')
            }
            logger.info(f"Extracted valuation: ${valuation_data['total_value']:,}")
        
        # Extract sale information
        sales_data = []
        if 'deedHistory' in prop:
            for deed in prop['deedHistory'][:3]:  # Get last 3 sales
                if deed.get('salePrice', 0) > 0:  # Only include actual sales
                    sales_data.append({
                        "sale_date": deed.get('saleDate', ''),
                        "sale_price": deed.get('salePrice', 0),
                        "buyer": ', '.join(deed.get('buyers', [])),
                        "seller": ', '.join(deed.get('sellers', [])),
                        "document_type": deed.get('documentType', '')
                    })
        
        if sales_data:
            valuation_data["sales"] = sales_data
            logger.info(f"Extracted {len(sales_data)} sales records")
        
        # Extract legal information
        legal_data = {}
        if 'legal' in prop:
            legal = prop['legal']
            legal_data = {
                "legal_description": legal.get('legalDescription', 'Unknown'),
                "subdivision": legal.get('subdivisionName', 'Unknown'),
                "section_township_range": legal.get('sectionTownshipRangeMeridian', 'Unknown')
            }
        
        # Extract lot information
        if 'lot' in prop:
            lot = prop['lot']
            legal_data["parcel_size"] = f"{lot.get('lotSizeAcres', 0):.2f} acres"
            legal_data["zoning"] = lot.get('zoningCode', 'Unknown')
        
        # Extract building information
        building_data = {}
        if 'building' in prop:
            building = prop['building']
            building_data = {
                "year_built": building.get('yearBuilt', 'Unknown'),
                "square_feet": building.get('totalBuildingAreaSquareFeet', 'Unknown'),
                "bedrooms": building.get('roomCount', 'Unknown'),
                "bathrooms": building.get('bathroomCount', 'Unknown')
            }
        
        # Extract APN
        apn_data = {}
        if 'ids' in prop:
            ids = prop['ids']
            apn_data = {
                "apn": ids.get('apn', 'Unknown'),
                "old_apn": ids.get('oldApn', 'Unknown')
            }
            logger.info(f"Extracted APN: {apn_data['apn']}")
        
        result = {
            "owner_details": owner_data,
            "valuation": valuation_data,
            "legal": legal_data,
            "building": building_data,
            "apn_info": apn_data,
            "raw_data": prop,
            "is_real_data": True
        }
        
        logger.info("Successfully parsed property data")
        return result
    
    def _format_address(self, address: Dict) -> str:
        """Format address dictionary into string"""
        if not address:
            return "Unknown"
        
        parts = []
        if address.get('houseNumber'):
            parts.append(address['houseNumber'])
        if address.get('street'):
            parts.append(address['street'])
        if address.get('city'):
            parts.append(address['city'])
        if address.get('state'):
            parts.append(address['state'])
        if address.get('zip'):
            parts.append(address['zip'])
        
        return ', '.join(parts) if parts else "Unknown"
    
    def test_connection(self) -> bool:
        """Test API connection with a simple search"""
        logger.info("Testing BatchData API connection")
        try:
            result = self.search_property("Phoenix, AZ")
            success = 'results' in result and 'properties' in result.get('results', {})
            logger.info(f"API connection test: {'SUCCESS' if success else 'FAILED'}")
            return success
        except Exception as e:
            logger.error(f"API connection test failed: {str(e)}")
            return False

# Helper functions for the main app
def fetch_batchdata_property(address: str = None, apn: str = None) -> Dict:
    """
    Fetch property data from BatchData API
    """
    logger.info(f"Fetching BatchData property - Address: {address}, APN: {apn}")
    
    api = BatchDataAPI()
    
    if not api.api_key:
        logger.error("No BatchData API key found")
        st.error("❌ BatchData API key not found. Please add BATCHDATA_API_KEY to your .env file.")
        return {}
    
    if address:
        # Parse address into components
        address_parts = address.split(',')
        if len(address_parts) >= 3:
            street = address_parts[0].strip()
            city = address_parts[1].strip()
            state_zip = address_parts[2].strip().split()
            state = state_zip[0] if state_zip else "AZ"
            zip_code = state_zip[1] if len(state_zip) > 1 else ""
            
            address_dict = {
                "street": street,
                "city": city,
                "state": state,
                "zip": zip_code
            }
            
            logger.info(f"Parsed address: {address_dict}")
            st.info(f"🔍 Looking up property at: {address}")
            response = api.lookup_property_by_address(address_dict)
        else:
            logger.error(f"Invalid address format: {address}")
            st.error("❌ Invalid address format. Please use: 'Street, City, State ZIP'")
            return {}
    elif apn:
        logger.info(f"Looking up by APN: {apn}")
        st.info(f"🔍 Looking up property by APN: {apn}")
        response = api.lookup_property_by_apn(apn)
    else:
        logger.error("No address or APN provided")
        st.error("❌ No address or APN provided")
        return {}
    
    if response and 'results' in response:
        logger.info("Successfully received API response")
        return api.parse_property_data(response)
    else:
        logger.warning("No property data found in response")
        st.warning("⚠️ No property data found")
        return {}

def test_batchdata_api():
    """Test BatchData API connectivity"""
    logger.info("Testing BatchData API connectivity")
    api = BatchDataAPI()
    return api.test_connection()