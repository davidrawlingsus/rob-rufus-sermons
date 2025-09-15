#!/usr/bin/env python3
"""
Check Google Cloud Storage Upload Progress
This script checks how many MP3 files have been uploaded to the bucket
"""

import subprocess
import sys

def check_upload_progress(bucket_name):
    """Check how many files are in the bucket vs local files"""
    
    try:
        # Count local MP3 files
        result = subprocess.run(['find', 'Rob_Rufus_Sermons', '-name', '*.mp3'], 
                              capture_output=True, text=True)
        local_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
        local_count = len([f for f in local_files if f])
        
        print(f"📁 Local MP3 files: {local_count}")
        
        # Count files in Google Cloud Storage bucket
        result = subprocess.run(['gcloud', 'storage', 'ls', f'gs://{bucket_name}/'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            cloud_files = result.stdout.strip().split('\n') if result.stdout.strip() else []
            cloud_count = len([f for f in cloud_files if f.endswith('.mp3')])
            print(f"☁️  Cloud MP3 files: {cloud_count}")
            
            # Calculate progress
            if local_count > 0:
                progress = (cloud_count / local_count) * 100
                print(f"📊 Upload progress: {progress:.1f}%")
                
                if cloud_count == local_count:
                    print("✅ Upload complete!")
                    return True
                else:
                    print("⏳ Upload still in progress...")
                    return False
            else:
                print("❌ No local files found")
                return False
        else:
            print(f"❌ Error checking cloud bucket: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking progress: {e}")
        return False

def show_upload_status(bucket_name):
    """Show detailed upload status"""
    
    print(f"🪣 Bucket: gs://{bucket_name}")
    print("=" * 50)
    
    # Check progress
    is_complete = check_upload_progress(bucket_name)
    
    if is_complete:
        print()
        print("🎉 All files uploaded! You can now:")
        print("1. Run: python update_cloud_urls.py rob-rufus-sermons-1757906372")
        print("2. Test the download links on your live app")
    else:
        print()
        print("⏳ Upload still in progress. Check again in a few minutes.")
        print("You can run this script again to check progress.")

def main():
    """Main function"""
    print("📊 Google Cloud Storage Upload Progress Checker")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("Usage: python check_upload_progress.py <bucket_name>")
        print("Example: python check_upload_progress.py rob-rufus-sermons-1757906372")
        sys.exit(1)
    
    bucket_name = sys.argv[1]
    show_upload_status(bucket_name)

if __name__ == "__main__":
    main()
