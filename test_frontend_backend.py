#!/usr/bin/env python3
"""
Test Frontend-Backend Connection
This script tests the API endpoints that the frontend uses
"""

import requests
import json
import sys

def test_api_endpoints(base_url="http://localhost:5001"):
    """Test all API endpoints used by the frontend"""
    
    endpoints = [
        "/health",
        "/api/stats", 
        "/api/themes",
        "/api/sermons",
        "/api/sermons?limit=5",
        "/api/sermons?search=grace",
        "/api/sermons?themes=Grace%20%26%20Gospel"
    ]
    
    print("🧪 Testing Frontend-Backend API Connection")
    print("=" * 50)
    print(f"Base URL: {base_url}")
    print()
    
    all_passed = True
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint} - OK")
                
                # Show sample data for key endpoints
                if endpoint == "/api/stats":
                    print(f"   📊 Total sermons: {data.get('total_sermons', 'N/A')}")
                elif endpoint == "/api/themes":
                    theme_count = len(data.get('themes', []))
                    print(f"   🏷️  Themes available: {theme_count}")
                elif endpoint.startswith("/api/sermons"):
                    sermon_count = len(data.get('sermons', []))
                    print(f"   🎵 Sermons returned: {sermon_count}")
                    
            else:
                print(f"❌ {endpoint} - HTTP {response.status_code}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Connection error: {e}")
            all_passed = False
        except json.JSONDecodeError as e:
            print(f"❌ {endpoint} - JSON decode error: {e}")
            all_passed = False
        except Exception as e:
            print(f"❌ {endpoint} - Unexpected error: {e}")
            all_passed = False
    
    print()
    if all_passed:
        print("🎉 All API endpoints are working correctly!")
        print("The frontend should be able to connect to the backend successfully.")
    else:
        print("❌ Some API endpoints failed. Check the Flask app and database.")
        sys.exit(1)

def test_frontend_specific_queries(base_url="http://localhost:5001"):
    """Test queries that the frontend specifically uses"""
    
    print("\n🔍 Testing Frontend-Specific Queries")
    print("=" * 40)
    
    # Test theme filtering (as used by frontend)
    try:
        response = requests.get(f"{base_url}/api/sermons?themes=Grace%20%26%20Gospel&themes=Holy%20Spirit")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Multi-theme filtering: {len(data.get('sermons', []))} sermons")
        else:
            print(f"❌ Multi-theme filtering failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Multi-theme filtering error: {e}")
    
    # Test search functionality
    try:
        response = requests.get(f"{base_url}/api/sermons?search=grace&sort=newest")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search functionality: {len(data.get('sermons', []))} sermons found")
        else:
            print(f"❌ Search functionality failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Search functionality error: {e}")
    
    # Test sorting
    try:
        response = requests.get(f"{base_url}/api/sermons?sort=oldest&limit=3")
        if response.status_code == 200:
            data = response.json()
            sermons = data.get('sermons', [])
            if sermons:
                print(f"✅ Sorting (oldest first): {sermons[0].get('date', 'N/A')} to {sermons[-1].get('date', 'N/A')}")
            else:
                print("⚠️  Sorting test: No sermons returned")
        else:
            print(f"❌ Sorting failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Sorting error: {e}")

def main():
    """Main test function"""
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5001"
    
    test_api_endpoints(base_url)
    test_frontend_specific_queries(base_url)
    
    print("\n📱 Frontend Connection Summary:")
    print("The frontend JavaScript should now be able to:")
    print("• Load sermon statistics from /api/stats")
    print("• Load available themes from /api/themes") 
    print("• Search and filter sermons via /api/sermons")
    print("• Handle theme filtering with multiple parameters")
    print("• Sort sermons by date and title")
    print("• Display loading states and error messages")

if __name__ == "__main__":
    main()
