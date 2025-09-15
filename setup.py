#!/usr/bin/env python3
"""
Setup script for Rob Rufus Sermon Scraper
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    """Main setup function"""
    print("Setting up Rob Rufus Sermon Scraper...")
    
    if install_requirements():
        print("\n🎉 Setup completed successfully!")
        print("\nTo run the scraper:")
        print("python rob_rufus_scraper.py")
    else:
        print("\n❌ Setup failed. Please install dependencies manually:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()
