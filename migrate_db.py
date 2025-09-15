#!/usr/bin/env python3
"""
Database migration script for Rob Rufus Sermon Directory
Populates the database from existing JSON data
"""

import os
import json
import sys
from datetime import datetime
from app import app, db, Sermon

def migrate_database():
    """Migrate sermon data from JSON to database"""
    
    json_file = 'sermon_metadata.json'
    
    if not os.path.exists(json_file):
        print(f"❌ JSON file {json_file} not found.")
        print("Please run analyze_sermons.py first to generate the metadata.")
        return False
    
    try:
        with app.app_context():
            # Create tables if they don't exist
            db.create_all()
            print("✅ Database tables created/verified")
            
            # Load JSON data
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            sermons_data = data.get('sermons', [])
            print(f"📊 Found {len(sermons_data)} sermons in JSON file")
            
            # Clear existing data
            Sermon.query.delete()
            print("🗑️  Cleared existing sermon data")
            
            # Insert new data
            for i, sermon_data in enumerate(sermons_data, 1):
                try:
                    sermon = Sermon(
                        filename=sermon_data['filename'],
                        title=sermon_data['title'],
                        date=datetime.strptime(sermon_data['date'], '%Y-%m-%d').date(),
                        year=sermon_data['year'],
                        themes=sermon_data['themes'],
                        url=sermon_data['url']
                    )
                    db.session.add(sermon)
                    
                    if i % 50 == 0:
                        print(f"📝 Processed {i}/{len(sermons_data)} sermons...")
                        
                except Exception as e:
                    print(f"⚠️  Error processing sermon {i}: {e}")
                    continue
            
            # Commit all changes
            db.session.commit()
            print(f"✅ Successfully migrated {len(sermons_data)} sermons to database")
            
            # Verify migration
            total_sermons = Sermon.query.count()
            print(f"🔍 Verification: {total_sermons} sermons in database")
            
            # Show sample data
            sample_sermon = Sermon.query.first()
            if sample_sermon:
                print(f"📄 Sample sermon: {sample_sermon.title} ({sample_sermon.date})")
                print(f"🏷️  Themes: {', '.join(sample_sermon.themes)}")
            
            return True
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def show_database_stats():
    """Show database statistics"""
    try:
        with app.app_context():
            total_sermons = Sermon.query.count()
            
            if total_sermons == 0:
                print("📊 Database is empty")
                return
            
            # Get date range
            earliest = Sermon.query.order_by(Sermon.date.asc()).first()
            latest = Sermon.query.order_by(Sermon.date.desc()).first()
            
            # Get theme counts
            all_sermons = Sermon.query.all()
            theme_counts = {}
            for sermon in all_sermons:
                for theme in sermon.themes:
                    theme_counts[theme] = theme_counts.get(theme, 0) + 1
            
            print("📊 DATABASE STATISTICS")
            print("=" * 40)
            print(f"Total Sermons: {total_sermons}")
            print(f"Date Range: {earliest.date} to {latest.date}")
            print(f"Themes: {len(theme_counts)} categories")
            print()
            print("🔥 Top Themes:")
            sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
            for theme, count in sorted_themes[:10]:
                print(f"   • {theme}: {count} sermons")
                
    except Exception as e:
        print(f"❌ Error showing stats: {e}")

def main():
    """Main function"""
    print("🎵 Rob Rufus Sermon Database Migration")
    print("=" * 50)
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--stats':
        show_database_stats()
        return
    
    # Check if database already has data
    with app.app_context():
        # Create tables first
        db.create_all()
        
        try:
            existing_count = Sermon.query.count()
            if existing_count > 0:
                response = input(f"Database already has {existing_count} sermons. Overwrite? (y/n): ")
                if response.lower() != 'y':
                    print("Migration cancelled.")
                    return
        except Exception:
            # Tables don't exist yet, that's fine
            pass
    
    # Perform migration
    success = migrate_database()
    
    if success:
        print()
        print("🎉 Migration completed successfully!")
        print("You can now run the Flask app with: python app.py")
        print("Or deploy to Railway with the existing configuration.")
    else:
        print()
        print("❌ Migration failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
