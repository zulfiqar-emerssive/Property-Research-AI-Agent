#!/usr/bin/env python3
"""
Test script to verify the Commercial Property Research Agent setup
"""

import sys
import importlib

def test_imports():
    """Test that all required packages can be imported"""
    required_packages = [
        'streamlit',
        'requests', 
        'pandas',
        'openai',
        'markdown',
        'xhtml2pdf',
        'dotenv'
    ]
    
    print("🔍 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_local_modules():
    """Test that local modules can be imported"""
    local_modules = ['demo_data', 'config']
    
    print("\n🔍 Testing local module imports...")
    failed_imports = []
    
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return failed_imports

def test_demo_data():
    """Test demo data functionality"""
    print("\n🔍 Testing demo data...")
    
    try:
        from demo_data import get_demo_parcel_data, get_demo_research_memo, SAMPLE_APNS
        
        # Test demo parcel data
        demo_data = get_demo_parcel_data("123-45-678")
        if demo_data and "owner_details" in demo_data:
            print("✅ Demo parcel data generation")
        else:
            print("❌ Demo parcel data generation failed")
            return False
        
        # Test demo memo
        memo = get_demo_research_memo()
        if memo and len(memo) > 100:
            print("✅ Demo memo generation")
        else:
            print("❌ Demo memo generation failed")
            return False
        
        # Test sample APNs
        if SAMPLE_APNS and len(SAMPLE_APNS) > 0:
            print("✅ Sample APNs loaded")
        else:
            print("❌ Sample APNs failed to load")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Demo data test failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import APP_TITLE, SAMPLE_APNS, GPT_PROMPT_TEMPLATE
        
        if APP_TITLE:
            print("✅ App title loaded")
        else:
            print("❌ App title failed to load")
            return False
        
        if SAMPLE_APNS:
            print("✅ Sample APNs loaded from config")
        else:
            print("❌ Sample APNs failed to load from config")
            return False
        
        if GPT_PROMPT_TEMPLATE:
            print("✅ GPT prompt template loaded")
        else:
            print("❌ GPT prompt template failed to load")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Commercial Property Research Agent - Setup Test")
    print("=" * 50)
    
    # Test package imports
    failed_packages = test_imports()
    
    # Test local modules
    failed_modules = test_local_modules()
    
    # Test demo data
    demo_data_ok = test_demo_data()
    
    # Test configuration
    config_ok = test_config()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    if not failed_packages and not failed_modules and demo_data_ok and config_ok:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n📝 Next steps:")
        print("1. Set up your OpenAI API key in a .env file")
        print("2. Run: streamlit run app.py")
        print("3. Open your browser to http://localhost:8501")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
        if failed_packages:
            print(f"\n📦 Missing packages: {', '.join(failed_packages)}")
            print("Run: pip install -r requirements.txt")
        
        if failed_modules:
            print(f"\n📁 Missing local modules: {', '.join(failed_modules)}")
            print("Make sure all files are in the same directory")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 