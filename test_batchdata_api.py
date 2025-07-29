#!/usr/bin/env python3
"""
Test script for BatchData API connectivity and authentication
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_batchdata_authentication():
    """Test different authentication methods for BatchData API"""
    
    api_key = os.getenv("BATCHDATA_API_KEY")
    if not api_key:
        print("❌ No BATCHDATA_API_KEY found in environment variables")
        print("💡 Please add your BatchData API key to the .env file")
        return False
    
    print(f"🔑 Testing with API key: {api_key[:10]}...")
    
    # Test different authentication methods
    auth_methods = [
        {
            "name": "Bearer Token",
            "headers": {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
        },
        {
            "name": "X-API-Key Header",
            "headers": {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-API-Key': api_key
            }
        },
        {
            "name": "api-key Header",
            "headers": {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'api-key': api_key
            }
        },
        {
            "name": "API-Key Header",
            "headers": {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'API-Key': api_key
            }
        },
        {
            "name": "Query Parameter",
            "headers": {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            "params": {"api_key": api_key}
        }
    ]
    
    # Test endpoints
    endpoints = [
        {
            "name": "Property Search",
            "url": "https://api.batchdata.com/api/v1/property/search",
            "method": "POST",
            "data": {
                "searchCriteria": {
                    "query": "Phoenix, AZ"
                },
                "options": {
                    "useYearBuilt": True,
                    "skip": 0,
                    "take": 1
                }
            }
        },
        {
            "name": "Property Lookup",
            "url": "https://api.batchdata.com/api/v1/property/lookup/all-attributes",
            "method": "POST",
            "data": {
                "requests": [
                    {
                        "address": {
                            "street": "26823 N 31st Dr",
                            "city": "Phoenix",
                            "state": "AZ",
                            "zip": "85083"
                        }
                    }
                ]
            }
        }
    ]
    
    successful_methods = []
    
    for auth_method in auth_methods:
        print(f"\n🔍 Testing {auth_method['name']} authentication...")
        
        for endpoint in endpoints:
            try:
                print(f"  📡 Testing {endpoint['name']}...")
                
                if auth_method['method'] == 'POST':
                    if 'params' in auth_method:
                        response = requests.post(
                            endpoint['url'],
                            headers=auth_method['headers'],
                            params=auth_method['params'],
                            json=endpoint['data'],
                            timeout=30
                        )
                    else:
                        response = requests.post(
                            endpoint['url'],
                            headers=auth_method['headers'],
                            json=endpoint['data'],
                            timeout=30
                        )
                
                print(f"    Status: {response.status_code}")
                print(f"    Headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    print(f"    ✅ SUCCESS! {auth_method['name']} works with {endpoint['name']}")
                    successful_methods.append({
                        "auth_method": auth_method['name'],
                        "endpoint": endpoint['name'],
                        "headers": auth_method['headers']
                    })
                    
                    # Try to parse response
                    try:
                        result = response.json()
                        if 'results' in result and 'properties' in result.get('results', {}):
                            properties = result['results']['properties']
                            print(f"    📊 Found {len(properties)} properties")
                            if properties:
                                prop = properties[0]
                                if 'address' in prop:
                                    addr = prop['address']
                                    print(f"    🏠 Sample property: {addr.get('street', 'Unknown')}, {addr.get('city', 'Unknown')}")
                        else:
                            print(f"    📄 Response: {result}")
                    except json.JSONDecodeError:
                        print(f"    📄 Response (not JSON): {response.text[:200]}...")
                        
                elif response.status_code == 401:
                    print(f"    ❌ Unauthorized - Invalid API key or authentication method")
                elif response.status_code == 403:
                    print(f"    ❌ Forbidden - Authentication method not accepted")
                elif response.status_code == 429:
                    print(f"    ⚠️ Rate limited - Too many requests")
                else:
                    print(f"    ❌ Error: {response.status_code}")
                    print(f"    📄 Response: {response.text[:200]}...")
                    
            except Exception as e:
                print(f"    ❌ Exception: {str(e)}")
    
    # Summary
    print(f"\n📋 Authentication Test Summary:")
    if successful_methods:
        print(f"✅ Found {len(successful_methods)} working authentication method(s):")
        for method in successful_methods:
            print(f"   - {method['auth_method']} with {method['endpoint']}")
        
        # Show the working headers
        working_headers = successful_methods[0]['headers']
        print(f"\n🔧 Working headers configuration:")
        for key, value in working_headers.items():
            if 'key' in key.lower() or 'auth' in key.lower():
                print(f"   {key}: {value[:10]}...")
            else:
                print(f"   {key}: {value}")
        
        return True
    else:
        print("❌ No working authentication methods found")
        print("\n💡 Troubleshooting tips:")
        print("   1. Verify your API key is correct")
        print("   2. Check your BatchData account has sufficient credits")
        print("   3. Ensure your account is activated")
        print("   4. Check BatchData API documentation for current authentication method")
        return False

def test_simple_connection():
    """Test basic connectivity to BatchData API"""
    print("\n🌐 Testing basic connectivity...")
    
    try:
        # Test basic connectivity
        response = requests.get("https://api.batchdata.com/api/v1", timeout=10)
        print(f"   API base URL status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ API base URL is accessible")
        else:
            print("   ⚠️ API base URL returned non-200 status")
            
    except Exception as e:
        print(f"   ❌ Cannot connect to API base URL: {str(e)}")

if __name__ == "__main__":
    print("🔧 BatchData API Authentication Test")
    print("=" * 50)
    
    # Test basic connectivity
    test_simple_connection()
    
    # Test authentication
    success = test_batchdata_authentication()
    
    if success:
        print(f"\n🎉 Authentication test completed successfully!")
        print("💡 You can now use the application with real data.")
    else:
        print(f"\n❌ Authentication test failed.")
        print("💡 Please check your API key and try again.")