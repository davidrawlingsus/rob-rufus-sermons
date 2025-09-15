#!/usr/bin/env python3
"""
Railway PostgreSQL Migration Script for Rob Rufus Sermon Directory
This script migrates sermon data to Railway's PostgreSQL database
"""

import os
import json
import sys
from datetime import datetime
from app import app, db, Sermon

def get_railway_database_url():
    """Get the DATABASE_URL from Railway environment"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not found!")
        print("Make sure you're running this in Railway or have DATABASE_URL set locally.")
        return None
    
    # Convert postgres:// to postgresql:// for SQLAlchemy
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

def setup_database():
    """Set up the database with proper PostgreSQL configuration"""
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Create indexes for better performance
            with db.engine.connect() as conn:
                conn.execute(db.text("""
                    CREATE INDEX IF NOT EXISTS idx_sermons_date ON sermons(date DESC);
                    CREATE INDEX IF NOT EXISTS idx_sermons_year ON sermons(year);
                    CREATE INDEX IF NOT EXISTS idx_sermons_filename ON sermons(filename);
                """))
                conn.commit()
            print("✅ Database indexes created successfully")
            
            return True
            
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        return False

def migrate_sermon_data():
    """Migrate sermon data from JSON to PostgreSQL"""
    json_file = 'sermon_metadata.json'
    
    if not os.path.exists(json_file):
        print(f"❌ JSON file {json_file} not found.")
        print("Please ensure sermon_metadata.json exists in the current directory.")
        return False
    
    try:
        with app.app_context():
            # Load JSON data
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            sermons_data = data.get('sermons', [])
            print(f"📊 Found {len(sermons_data)} sermons in JSON file")
            
            # Clear existing data
            Sermon.query.delete()
            print("🗑️  Cleared existing sermon data")
            
            # Insert new data in batches for better performance
            batch_size = 50
            for i in range(0, len(sermons_data), batch_size):
                batch = sermons_data[i:i + batch_size]
                
                for sermon_data in batch:
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
                        
                    except Exception as e:
                        print(f"⚠️  Error processing sermon '{sermon_data.get('title', 'Unknown')}': {e}")
                        continue
                
                # Commit batch
                db.session.commit()
                print(f"📝 Processed batch {i//batch_size + 1}/{(len(sermons_data) + batch_size - 1)//batch_size} ({len(batch)} sermons)")
            
            print(f"✅ Successfully migrated {len(sermons_data)} sermons to PostgreSQL")
            
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
    """Show comprehensive database statistics"""
    try:
        with app.app_context():
            total_sermons = Sermon.query.count()
            
            if total_sermons == 0:
                print("📊 Database is empty")
                return
            
            # Get date range
            earliest = Sermon.query.order_by(Sermon.date.asc()).first()
            latest = Sermon.query.order_by(Sermon.date.desc()).first()
            
            # Get theme counts using PostgreSQL JSONB queries
            with db.engine.connect() as conn:
                result = conn.execute(db.text("""
                    SELECT theme, COUNT(*) as count
                    FROM (
                        SELECT jsonb_array_elements_text(themes) as theme
                        FROM sermons
                    ) t
                    GROUP BY theme
                    ORDER BY count DESC
                    LIMIT 10
                """))
            
            print("📊 RAILWAY POSTGRESQL DATABASE STATISTICS")
            print("=" * 50)
            print(f"Total Sermons: {total_sermons}")
            print(f"Date Range: {earliest.date} to {latest.date}")
            print()
            print("🔥 Top Themes:")
            for row in result:
                print(f"   • {row[0]}: {row[1]} sermons")
            
            # Test JSONB queries
            print()
            print("🧪 Testing PostgreSQL JSONB queries:")
            
            # Test theme search
            with db.engine.connect() as conn:
                grace_count = conn.execute(db.text("SELECT COUNT(*) FROM sermons WHERE themes ? 'Grace & Gospel'")).scalar()
                print(f"   • Sermons with 'Grace & Gospel': {grace_count}")
                
                # Test full-text search
                search_count = conn.execute(db.text("""
                    SELECT COUNT(*) FROM sermons 
                    WHERE to_tsvector('english', title) @@ plainto_tsquery('english', 'grace')
                """)).scalar()
                print(f"   • Sermons with 'grace' in title: {search_count}")
                
    except Exception as e:
        print(f"❌ Error showing stats: {e}")

def main():
    """Main migration function"""
    print("🚀 Rob Rufus Sermon Railway PostgreSQL Migration")
    print("=" * 60)
    print()
    
    # Check if we're in Railway environment
    database_url = get_railway_database_url()
    if not database_url:
        sys.exit(1)
    
    print(f"🔗 Database URL: {database_url[:50]}...")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--stats':
        show_database_stats()
        return
    
    # Check if database already has data
    with app.app_context():
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
    
    # Set up database
    if not setup_database():
        sys.exit(1)
    
    # Migrate data
    if not migrate_sermon_data():
        sys.exit(1)
    
    print()
    print("🎉 Railway PostgreSQL migration completed successfully!")
    print("Your sermon directory is now ready for production!")
    
    # Show final stats
    print()
    show_database_stats()

if __name__ == "__main__":
    main()
