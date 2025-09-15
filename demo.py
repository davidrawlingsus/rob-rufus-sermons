#!/usr/bin/env python3
"""
Demo script to show the sermon directory features
"""

import json
import webbrowser
import os
from datetime import datetime

def show_stats():
    """Display statistics about the sermon collection"""
    try:
        with open('sermon_metadata.json', 'r') as f:
            data = json.load(f)
        
        sermons = data['sermons']
        stats = data['stats']
        
        print("🎵 Rob Rufus Sermon Directory Demo")
        print("=" * 50)
        print(f"📊 Total Sermons: {stats['total_sermons']}")
        print(f"📅 Date Range: {sermons[-1]['date']} to {sermons[0]['date']}")
        print(f"🏷️  Themes: {len(stats['themes'])} categories")
        print()
        
        print("🔥 Most Popular Themes:")
        sorted_themes = sorted(stats['themes'].items(), key=lambda x: x[1], reverse=True)
        for theme, count in sorted_themes[:10]:
            print(f"   • {theme}: {count} sermons")
        print()
        
        print("📈 Sermons by Year:")
        sorted_years = sorted(stats['years'].items(), key=lambda x: x[0], reverse=True)
        for year, count in sorted_years[:5]:
            print(f"   • {year}: {count} sermons")
        print()
        
        print("✨ Recent Sermons:")
        for sermon in sermons[:5]:
            print(f"   • {sermon['date']}: {sermon['title']}")
            print(f"     Themes: {', '.join(sermon['themes'])}")
        print()
        
    except FileNotFoundError:
        print("❌ sermon_metadata.json not found. Run analyze_sermons.py first.")
        return False
    
    return True

def open_directory():
    """Open the sermon directory in the default browser"""
    html_file = os.path.abspath('sermon_directory.html')
    
    if not os.path.exists(html_file):
        print("❌ sermon_directory.html not found.")
        return False
    
    print("🌐 Opening sermon directory in your browser...")
    webbrowser.open(f'file://{html_file}')
    print("✅ Directory opened!")
    return True

def main():
    """Main demo function"""
    print("Welcome to the Rob Rufus Sermon Directory Demo!\n")
    
    # Show statistics
    if not show_stats():
        return
    
    # Ask if user wants to open the directory
    try:
        response = input("Would you like to open the sermon directory? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            open_directory()
        else:
            print("You can open sermon_directory.html manually in your browser.")
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
    
    print("\n🎉 Demo complete! Enjoy browsing the sermons!")

if __name__ == "__main__":
    main()
