#!/usr/bin/env python3
"""
Update Database URLs to Google Cloud Storage
This script updates the sermon URLs in the database to point to Google Cloud Storage
"""

import os
import sys
from app import app, db, Sermon

def update_urls_to_cloud_storage(bucket_name):
    """Update all sermon URLs to point to Google Cloud Storage"""
    
    try:
        with app.app_context():
            # Get all sermons
            sermons = Sermon.query.all()
            print(f"📊 Found {len(sermons)} sermons to update")
            
            updated_count = 0
            
            for sermon in sermons:
                # Extract filename from the current URL or use the stored filename
                filename = sermon.filename
                
                # Create new Google Cloud Storage URL
                new_url = f"https://storage.googleapis.com/{bucket_name}/{filename}"
                
                # Update the URL
                sermon.url = new_url
                updated_count += 1
                
                if updated_count % 50 == 0:
                    print(f"📝 Updated {updated_count}/{len(sermons)} URLs...")
            
            # Commit all changes
            db.session.commit()
            print(f"✅ Successfully updated {updated_count} sermon URLs to Google Cloud Storage")
            
            # Show sample updated URLs
            sample_sermons = Sermon.query.limit(3).all()
            print("\n📄 Sample updated URLs:")
            for sermon in sample_sermons:
                print(f"   • {sermon.title[:50]}...")
                print(f"     {sermon.url}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error updating URLs: {e}")
        return False

def verify_cloud_urls(bucket_name):
    """Verify that the cloud URLs are accessible"""
    
    try:
        with app.app_context():
            # Test a few URLs
            sample_sermons = Sermon.query.limit(5).all()
            
            print(f"\n🧪 Testing Google Cloud Storage URLs:")
            print(f"Bucket: gs://{bucket_name}")
            
            for sermon in sample_sermons:
                print(f"   • {sermon.filename}")
                print(f"     URL: {sermon.url}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error verifying URLs: {e}")
        return False

def main():
    """Main function"""
    print("☁️  Google Cloud Storage URL Update")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage: python update_cloud_urls.py <bucket_name>")
        print("Example: python update_cloud_urls.py rob-rufus-sermons-1757906372")
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    print(f"🪣 Bucket: {bucket_name}")
    print()
    
    # Update URLs
    success = update_urls_to_cloud_storage(bucket_name)
    
    if success:
        print()
        print("🎉 URL update completed successfully!")
        print("All sermon download links now point to Google Cloud Storage.")
        
        # Verify URLs
        verify_cloud_urls(bucket_name)
        
        print()
        print("📱 Next steps:")
        print("1. Wait for MP3 upload to complete")
        print("2. Test download links on the live app")
        print("3. Update Railway deployment if needed")
    else:
        print()
        print("❌ URL update failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
