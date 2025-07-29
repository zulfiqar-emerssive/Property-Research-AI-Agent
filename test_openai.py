#!/usr/bin/env python3
"""
Test script to verify OpenAI client setup
"""

import os
from dotenv import load_dotenv

def test_openai_setup():
    """Test OpenAI client initialization"""
    
    print("🔍 Testing OpenAI Client Setup")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OpenAI API key found: {api_key[:10]}...")
    else:
        print("❌ OpenAI API key not found")
        print("💡 Create a .env file with: OPENAI_API_KEY=your_key_here")
        return False
    
    # Test client initialization
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
        
        # Test a simple API call
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'Hello World'"}],
                max_tokens=10
            )
            print("✅ OpenAI API call successful")
            print(f"   Response: {response.choices[0].message.content}")
            return True
        except Exception as e:
            print(f"❌ OpenAI API call failed: {str(e)}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI client initialization failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_openai_setup()
    if success:
        print("\n🎉 OpenAI setup is working correctly!")
    else:
        print("\n⚠️ OpenAI setup needs attention.")
        print("💡 Try running: pip install openai==1.3.7")