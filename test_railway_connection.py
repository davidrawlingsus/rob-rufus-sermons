#!/usr/bin/env python3
"""
Test Railway PostgreSQL Connection
This script tests the connection to Railway's PostgreSQL database
"""

import os
import sys
from app import app, db

def test_connection():
    """Test the database connection"""
    try:
        with app.app_context():
            # Test basic connection
            result = db.engine.execute("SELECT 1 as test").fetchone()
            print(f"✅ Database connection successful: {result[0]}")
            
            # Test PostgreSQL version
            version = db.engine.execute("SELECT version()").fetchone()[0]
            print(f"📊 PostgreSQL version: {version}")
            
            # Test if we can create tables
            db.create_all()
            print("✅ Tables created successfully")
            
            # Test JSONB functionality
            result = db.engine.execute("SELECT '[\"test\"]'::jsonb ? 'test' as jsonb_test").fetchone()
            print(f"✅ JSONB support: {result[0]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Railway PostgreSQL Connection")
    print("=" * 50)
    
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Make sure you're running this in Railway or have DATABASE_URL set")
        return False
    
    print(f"🔗 Database URL: {database_url[:50]}...")
    print()
    
    success = test_connection()
    
    if success:
        print()
        print("🎉 All tests passed! Railway PostgreSQL is ready for migration.")
    else:
        print()
        print("❌ Connection tests failed. Check your Railway setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()
