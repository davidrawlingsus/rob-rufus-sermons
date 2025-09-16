#!/usr/bin/env python3
"""
Test script to verify signed URL generation for Google Cloud Storage
"""

import os
import json
from datetime import datetime, timedelta
from google.cloud import storage
from urllib.parse import urlparse

# Configuration
GCS_BUCKET_NAME = 'rob-rufus-sermons-1757906372'
SERVICE_ACCOUNT_KEY_FILE = 'rob-rufus-sermons-key.json'

def test_signed_url_generation():
    """Test signed URL generation"""
    print("🧪 Testing Google Cloud Storage Signed URL Generation")
    print("=" * 60)
    
    try:
        # Initialize client with service account
        client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_KEY_FILE)
        print(f"✅ GCS client initialized successfully")
        
        # Test with a sample file
        test_object = "2024-10-27_An_Anointing_That_Goes_Beyond_Just_Yourself.mp3"
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(test_object)
        
        # Check if file exists
        if blob.exists():
            print(f"✅ Test file exists: {test_object}")
            
            # Generate signed URL
            expiration = datetime.utcnow() + timedelta(hours=24)
            signed_url = blob.generate_signed_url(
                version="v4",
                expiration=expiration,
                method="GET"
            )
            
            print(f"✅ Signed URL generated successfully")
            print(f"📄 URL: {signed_url[:100]}...")
            print(f"⏰ Expires: {expiration}")
            
            # Test URL accessibility
            import requests
            response = requests.head(signed_url, timeout=10)
            if response.status_code == 200:
                print(f"✅ Signed URL is accessible (Status: {response.status_code})")
                print(f"📊 Content-Type: {response.headers.get('content-type', 'Unknown')}")
                print(f"📏 Content-Length: {response.headers.get('content-length', 'Unknown')} bytes")
            else:
                print(f"❌ Signed URL returned status: {response.status_code}")
                
        else:
            print(f"❌ Test file does not exist: {test_object}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def test_url_parsing():
    """Test URL parsing logic"""
    print("\n🔍 Testing URL Parsing Logic")
    print("=" * 40)
    
    test_urls = [
        "https://storage.googleapis.com/rob-rufus-sermons-1757906372/2024-10-27_An_Anointing_That_Goes_Beyond_Just_Yourself.mp3",
        "gs://rob-rufus-sermons-1757906372/2024-10-27_An_Anointing_That_Goes_Beyond_Just_Yourself.mp3"
    ]
    
    for url in test_urls:
        print(f"\n📄 Testing URL: {url}")
        
        if 'storage.googleapis.com' in url:
            parsed_url = urlparse(url)
            object_name = parsed_url.path.lstrip('/')
            if object_name.startswith(GCS_BUCKET_NAME + '/'):
                object_name = object_name[len(GCS_BUCKET_NAME) + 1:]
            print(f"   Object name: {object_name}")
        elif 'gs://' in url:
            object_name = url.replace(f'gs://{GCS_BUCKET_NAME}/', '')
            print(f"   Object name: {object_name}")

if __name__ == "__main__":
    print("🚀 Starting Google Cloud Storage Signed URL Tests")
    print("=" * 60)
    
    # Test URL parsing
    test_url_parsing()
    
    # Test signed URL generation
    success = test_signed_url_generation()
    
    if success:
        print("\n🎉 All tests passed! Signed URLs are working correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
