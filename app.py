#!/usr/bin/env python3
"""
Flask web application for Rob Rufus Sermon Directory
Deployable to Railway with PostgreSQL database
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
from google.cloud import storage
from urllib.parse import urlparse

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure database
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///sermons.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Cloud Storage configuration
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 'rob-rufus-sermons-1757906372')
GCS_SERVICE_ACCOUNT_KEY = os.environ.get('GCS_SERVICE_ACCOUNT_KEY')

# Initialize Google Cloud Storage client
def get_gcs_client():
    """Get Google Cloud Storage client with service account credentials"""
    try:
        if GCS_SERVICE_ACCOUNT_KEY:
            # Use service account key from environment variable
            import json as json_lib
            service_account_info = json_lib.loads(GCS_SERVICE_ACCOUNT_KEY)
            client = storage.Client.from_service_account_info(service_account_info)
        else:
            # Use default credentials (for local development)
            client = storage.Client()
        return client
    except Exception as e:
        logger.error(f"Failed to initialize GCS client: {e}")
        return None

def generate_signed_url(bucket_name, object_name, expiration_hours=24):
    """Generate a signed URL for a Google Cloud Storage object"""
    try:
        client = get_gcs_client()
        if not client:
            return None
            
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        
        # Generate signed URL valid for specified hours
        expiration = datetime.utcnow() + timedelta(hours=expiration_hours)
        
        signed_url = blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="GET"
        )
        
        return signed_url
        
    except Exception as e:
        logger.error(f"Failed to generate signed URL for {object_name}: {e}")
        return None

# Database Models
class Sermon(db.Model):
    __tablename__ = 'sermons'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    title = db.Column(db.String(500), nullable=False)
    date = db.Column(db.Date, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    themes = db.Column(db.JSON, nullable=False)  # Store as JSON array (PostgreSQL will use JSONB)
    url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        # Generate signed URL for Google Cloud Storage files
        download_url = self.url
        
        # Check if this is a Google Cloud Storage URL
        if 'storage.googleapis.com' in self.url or 'gs://' in self.url:
            # Extract object name from URL
            if 'storage.googleapis.com' in self.url:
                # Parse URL like: https://storage.googleapis.com/bucket-name/object-name
                parsed_url = urlparse(self.url)
                object_name = parsed_url.path.lstrip('/')
                # Remove bucket name from path
                if object_name.startswith(GCS_BUCKET_NAME + '/'):
                    object_name = object_name[len(GCS_BUCKET_NAME) + 1:]
            else:
                # Parse gs:// URL like: gs://bucket-name/object-name
                object_name = self.url.replace(f'gs://{GCS_BUCKET_NAME}/', '')
            
            # Generate signed URL
            signed_url = generate_signed_url(GCS_BUCKET_NAME, object_name)
            if signed_url:
                download_url = signed_url
        
        return {
            'id': self.id,
            'filename': self.filename,
            'title': self.title,
            'date': self.date.isoformat(),
            'year': self.year,
            'themes': self.themes,
            'url': download_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Routes
@app.route('/')
def index():
    """Serve the main sermon directory page"""
    return render_template('index.html')

@app.route('/api/sermons')
def get_sermons():
    """API endpoint to get all sermons with optional filtering"""
    try:
        # Get query parameters
        search = request.args.get('search', '').lower()
        themes = request.args.getlist('themes')
        sort_by = request.args.get('sort', 'newest')
        limit = request.args.get('limit', type=int)
        
        # Build query
        query = Sermon.query
        
        # Apply search filter
        if search:
            # Use PostgreSQL-specific search for better performance
            if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI']:
                query = query.filter(
                    db.or_(
                        Sermon.title.ilike(f'%{search}%'),
                        Sermon.themes.op('?')(search),  # PostgreSQL JSON operator
                        db.func.to_tsvector('english', Sermon.title).op('@@')(db.func.plainto_tsquery('english', search))
                    )
                )
            else:
                # Fallback for SQLite (local development)
                query = query.filter(
                    db.or_(
                        Sermon.title.ilike(f'%{search}%'),
                        Sermon.date.cast(db.String).ilike(f'%{search}%')
                    )
                )
        
        # Apply theme filters
        if themes:
            for theme in themes:
                if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI']:
                    query = query.filter(Sermon.themes.op('?')(theme))
                else:
                    # Fallback for SQLite - search in JSON string
                    query = query.filter(Sermon.themes.like(f'%"{theme}"%'))
        
        # Apply sorting
        if sort_by == 'newest':
            query = query.order_by(Sermon.date.desc())
        elif sort_by == 'oldest':
            query = query.order_by(Sermon.date.asc())
        elif sort_by == 'title':
            query = query.order_by(Sermon.title.asc())
        elif sort_by == 'title-desc':
            query = query.order_by(Sermon.title.desc())
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        # Execute query
        sermons = query.all()
        
        return jsonify({
            'sermons': [sermon.to_dict() for sermon in sermons],
            'total': len(sermons),
            'filters': {
                'search': search,
                'themes': themes,
                'sort': sort_by
            }
        })
        
    except Exception as e:
        logger.error(f"Error fetching sermons: {e}")
        return jsonify({'error': 'Failed to fetch sermons'}), 500

@app.route('/api/stats')
def get_stats():
    """API endpoint to get sermon statistics"""
    try:
        # Get total count
        total_sermons = Sermon.query.count()
        
        # Get theme counts
        theme_counts = {}
        sermons = Sermon.query.all()
        
        for sermon in sermons:
            for theme in sermon.themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Get year counts
        year_counts = {}
        for sermon in sermons:
            year_counts[sermon.year] = year_counts.get(sermon.year, 0) + 1
        
        # Get date range
        if sermons:
            dates = [sermon.date for sermon in sermons]
            date_range = {
                'earliest': min(dates).isoformat(),
                'latest': max(dates).isoformat()
            }
        else:
            date_range = {'earliest': None, 'latest': None}
        
        return jsonify({
            'total_sermons': total_sermons,
            'themes': theme_counts,
            'years': year_counts,
            'date_range': date_range
        })
        
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({'error': 'Failed to fetch statistics'}), 500

@app.route('/api/themes')
def get_themes():
    """API endpoint to get available themes"""
    try:
        # Get all unique themes
        all_themes = set()
        sermons = Sermon.query.all()
        
        for sermon in sermons:
            all_themes.update(sermon.themes)
        
        # Count theme usage
        theme_counts = {}
        for sermon in sermons:
            for theme in sermon.themes:
                theme_counts[theme] = theme_counts.get(theme, 0) + 1
        
        # Sort by count
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        
        return jsonify({
            'themes': [{'name': theme, 'count': count} for theme, count in sorted_themes]
        })
        
    except Exception as e:
        logger.error(f"Error fetching themes: {e}")
        return jsonify({'error': 'Failed to fetch themes'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Database initialization
def init_db():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")

def populate_db_from_json():
    """Populate database from existing JSON file"""
    json_file = 'sermon_metadata.json'
    
    if not os.path.exists(json_file):
        logger.warning(f"JSON file {json_file} not found. Skipping population.")
        return
    
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        sermons_data = data.get('sermons', [])
        
        with app.app_context():
            # Clear existing data
            Sermon.query.delete()
            
            # Insert new data
            for sermon_data in sermons_data:
                sermon = Sermon(
                    filename=sermon_data['filename'],
                    title=sermon_data['title'],
                    date=datetime.strptime(sermon_data['date'], '%Y-%m-%d').date(),
                    year=sermon_data['year'],
                    themes=sermon_data['themes'],
                    url=sermon_data['url']
                )
                db.session.add(sermon)
            
            db.session.commit()
            logger.info(f"Populated database with {len(sermons_data)} sermons")
            
    except Exception as e:
        logger.error(f"Error populating database: {e}")

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Populate from JSON if available
    populate_db_from_json()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
