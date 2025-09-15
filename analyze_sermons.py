#!/usr/bin/env python3
"""
Analyze sermon files and extract metadata for the directory
"""

import os
import re
import json
from datetime import datetime
from collections import defaultdict

def extract_sermon_metadata(filename):
    """Extract metadata from sermon filename"""
    # Remove .mp3 extension
    name = filename.replace('.mp3', '')
    
    # Extract date (YYYY-MM-DD format)
    date_match = re.match(r'^(\d{4}-\d{2}-\d{2})_(.+)$', name)
    if not date_match:
        return None
    
    date_str, title = date_match.groups()
    
    # Parse date
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None
    
    # Clean up title
    title = title.replace('_', ' ')
    
    # Extract themes based on keywords in title
    themes = extract_themes(title)
    
    return {
        'filename': filename,
        'title': title,
        'date': date_str,
        'date_obj': date,
        'year': date.year,
        'themes': themes,
        'url': f'Rob_Rufus_Sermons/{filename}'
    }

def extract_themes(title):
    """Extract thematic keywords from sermon title"""
    title_lower = title.lower()
    themes = []
    
    # Define theme keywords
    theme_keywords = {
        'Grace': ['grace', 'gospel', 'righteousness', 'forgiveness', 'mercy'],
        'Faith': ['faith', 'believe', 'trust', 'confidence'],
        'Anointing': ['anointing', 'anointed', 'power', 'supernatural'],
        'Holy Spirit': ['holy spirit', 'spirit', 'tongues', 'manifestation'],
        'Healing': ['healing', 'heal', 'sick', 'miracle', 'miracles'],
        'Worship': ['worship', 'praise', 'glory', 'presence'],
        'Identity': ['identity', 'sonship', 'christ', 'inheritance'],
        'Fear': ['fear', 'fearless', 'courage', 'bold'],
        'Love': ['love', 'compassion', 'relationship'],
        'Kingdom': ['kingdom', 'reign', 'authority', 'power'],
        'Freedom': ['freedom', 'free', 'liberated', 'liberty'],
        'Joy': ['joy', 'rejoice', 'happiness', 'gladness'],
        'Peace': ['peace', 'rest', 'comfort'],
        'Prayer': ['prayer', 'pray', 'intercession'],
        'Word': ['word', 'scripture', 'bible', 'truth'],
        'Church': ['church', 'congregation', 'ministry', 'pastor'],
        'Christmas': ['christmas', 'emmanuel', 'nativity'],
        'Easter': ['resurrection', 'cross', 'crucifixion'],
        'End Times': ['end times', 'prophecy', 'revelation', 'apocalypse']
    }
    
    for theme, keywords in theme_keywords.items():
        if any(keyword in title_lower for keyword in keywords):
            themes.append(theme)
    
    # If no themes found, add a general category
    if not themes:
        themes.append('General')
    
    return themes

def analyze_all_sermons():
    """Analyze all sermon files"""
    sermons_dir = 'Rob_Rufus_Sermons'
    sermons = []
    
    if not os.path.exists(sermons_dir):
        print(f"Directory {sermons_dir} not found!")
        return []
    
    for filename in os.listdir(sermons_dir):
        if filename.endswith('.mp3'):
            metadata = extract_sermon_metadata(filename)
            if metadata:
                sermons.append(metadata)
    
    # Sort by date (newest first)
    sermons.sort(key=lambda x: x['date_obj'], reverse=True)
    
    return sermons

def generate_theme_stats(sermons):
    """Generate statistics about themes"""
    theme_counts = defaultdict(int)
    year_counts = defaultdict(int)
    
    for sermon in sermons:
        for theme in sermon['themes']:
            theme_counts[theme] += 1
        year_counts[sermon['year']] += 1
    
    return {
        'themes': dict(theme_counts),
        'years': dict(year_counts),
        'total_sermons': len(sermons)
    }

def main():
    """Main function"""
    print("Analyzing sermon files...")
    
    sermons = analyze_all_sermons()
    stats = generate_theme_stats(sermons)
    
    print(f"Found {len(sermons)} sermons")
    print(f"Date range: {sermons[-1]['date']} to {sermons[0]['date']}")
    print(f"Themes: {list(stats['themes'].keys())}")
    
    # Save metadata to JSON file
    output_data = {
        'sermons': sermons,
        'stats': stats,
        'generated_at': datetime.now().isoformat()
    }
    
    with open('sermon_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, default=str)
    
    print("Metadata saved to sermon_metadata.json")
    
    # Print some sample data
    print("\nSample sermons:")
    for sermon in sermons[:5]:
        print(f"- {sermon['date']}: {sermon['title']} ({', '.join(sermon['themes'])})")

if __name__ == "__main__":
    main()
