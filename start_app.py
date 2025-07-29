#!/usr/bin/env python3
"""
Startup script for the Commercial Property Research Agent
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'requests', 
        'pandas',
        'markdown',
        'xhtml2pdf',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    print("🏢 Commercial Property Research Agent")
    print("=" * 40)
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"⚠️ Missing packages: {', '.join(missing)}")
        choice = input("Install missing dependencies? (y/n): ").lower().strip()
        
        if choice == 'y':
            if not install_dependencies():
                print("❌ Failed to install dependencies. Please install manually:")
                print("pip install -r requirements.txt")
                return
        else:
            print("❌ Cannot run without required dependencies")
            return
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️ No .env file found")
        print("💡 Creating .env file from template...")
        
        if os.path.exists('env_template.txt'):
            with open('env_template.txt', 'r') as f:
                template = f.read()
            
            with open('.env', 'w') as f:
                f.write(template)
            
            print("✅ Created .env file")
            print("📝 Please edit .env file and add your OpenAI API key")
        else:
            print("❌ env_template.txt not found")
    
    # Choose which version to run
    print("\n🚀 Choose version to run:")
    print("1. Simple Version (No OpenAI required)")
    print("2. Full Version (With OpenAI integration)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("🎭 Starting Simple Version...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app_simple.py"])
    elif choice == "2":
        print("🤖 Starting Full Version...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()