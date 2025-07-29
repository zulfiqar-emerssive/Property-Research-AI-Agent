#!/usr/bin/env python3
"""
Test script to check Maricopa County API endpoints
"""

import requests
import json

def test_maricopa_endpoints():
    """Test various Maricopa County API endpoints"""
    
    test_apn = "123-45-678"
    
    # Different base URLs to try
    base_urls = [
        "https://mcassessor.maricopa.gov/api/v1",
        "https://mcassessor.maricopa.gov/api",
        "https://mcassessor.maricopa.gov/parcel",
        "https://mcassessor.maricopa.gov"
    ]
    
    # Different endpoint patterns
    endpoint_patterns = [
        "/parcel/{apn}/owner-details",
        "/parcel/{apn}/valuation",
        "/parcel/{apn}/legal",
        "/{apn}/owner-details",
        "/{apn}/valuation", 
        "/{apn}/legal",
        "/parcel/{apn}",
        "/{apn}"
    ]
    
    print("🔍 Testing Maricopa County API Endpoints")
    print("=" * 50)
    
    for base_url in base_urls:
        print(f"\n📍 Testing base URL: {base_url}")
        
        for pattern in endpoint_patterns:
            endpoint = pattern.format(apn=test_apn)
            full_url = base_url + endpoint
            
            try:
                print(f"  Testing: {full_url}")
                response = requests.get(full_url, timeout=10)
                print(f"    Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"    Content-Type: {response.headers.get('content-type', 'unknown')}")
                    print(f"    Content-Length: {len(response.text)}")
                    
                    if response.text.strip():
                        try:
                            data = response.json()
                            print(f"    JSON Response: {type(data)} - {len(str(data))} chars")
                            if isinstance(data, dict):
                                print(f"    Keys: {list(data.keys())}")
                        except json.JSONDecodeError:
                            print(f"    Text Response: {response.text[:200]}...")
                    else:
                        print("    Empty response")
                elif response.status_code == 404:
                    print("    Not Found")
                elif response.status_code == 403:
                    print("    Forbidden")
                else:
                    print(f"    Error: {response.status_code}")
                    
            except Exception as e:
                print(f"    Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ API endpoint testing completed")

if __name__ == "__main__":
    test_maricopa_endpoints()