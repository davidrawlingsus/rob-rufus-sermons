#!/usr/bin/env python3
"""
Update sermon metadata with optimized thematic categories
"""

import json
import re
from collections import defaultdict

def load_sermons():
    """Load existing sermon data"""
    with open('sermon_metadata.json', 'r') as f:
        data = json.load(f)
    return data

def extract_optimized_themes(title):
    """Extract themes using the optimized categorization"""
    title_lower = title.lower()
    themes = []
    
    # Optimized theme definitions based on analysis
    theme_keywords = {
        'Grace & Gospel': [
            'grace', 'gospel', 'righteousness', 'forgiveness', 'mercy', 'love', 'compassion',
            'covenant', 'blessing', 'favor', 'finished', 'work', 'cross', 'blood', 'gift',
            'established', 'assurance', 'self', 'righteousness'
        ],
        'Anointing & Power': [
            'anointing', 'anointed', 'power', 'supernatural', 'miracles', 'manifestation',
            'glory', 'presence', 'heaven', 'divine', 'increasing', 'greater', 'fire',
            'awesome', 'single', 'out', 'crowd'
        ],
        'Holy Spirit': [
            'spirit', 'holy', 'tongues', 'manifestation', 'presence', 'glory', 'cloud',
            'moving', 'living', 'person', 'comfort', 'joy', 'manifests', 'visits',
            'angels', 'service'
        ],
        'Faith & Trust': [
            'faith', 'believe', 'trust', 'confidence', 'assurance', 'certainty', 'promises',
            'inheritance', 'blessings', 'miracles', 'supernatural', 'important', 'why',
            'effortless', 'enjoys'
        ],
        'Worship & Praise': [
            'worship', 'praise', 'glory', 'presence', 'throne', 'room', 'attracts',
            'manifestation', 'humility', 'ultimate', 'blessings', 'lives', 'god'
        ],
        'Healing & Miracles': [
            'healing', 'heal', 'sick', 'miracle', 'miracles', 'power', 'supernatural',
            'compassion', 'forgiveness', 'twin', 'remembering', 'will', 'all', 'holds',
            'back', 'greater', 'after', 'jesus', 'went', 'heaven'
        ],
        'Kingdom & Authority': [
            'kingdom', 'reign', 'authority', 'power', 'government', 'shoulders',
            'heaven', 'earth', 'colonising', 'kiss', 'positioning', 'yourself',
            'speed', 'up', 'supernatural', 'lightning', 'conductor'
        ],
        'Freedom & Liberation': [
            'freedom', 'free', 'liberated', 'liberty', 'orphan', 'spirit', 'masks',
            'religious', 'political', 'control', 'overthrowing', 'condemnation',
            'guilt', 'fully', 'covered', 'glory'
        ],
        'Spiritual Warfare': [
            'warfare', 'enemy', 'outwit', 'accusation', 'spirit', 'religious',
            'political', 'control', 'overthrowing', 'struggle', 'authentic',
            'tactics', 'trick', 'unbelief'
        ],
        'Fear & Courage': [
            'fear', 'fearless', 'courage', 'bold', 'living', 'times', 'judgement',
            'wrath', 'condemnation', 'guilt', 'totally', 'free', 'from'
        ],
        'Word & Truth': [
            'word', 'scripture', 'bible', 'truth', 'knowledge', 'key', 'restoring',
            'gospel', 'grace', 'law', 'foundation', 'discerning', 'legalism'
        ],
        'Peace & Rest': [
            'peace', 'rest', 'comfort', 'covenant', 'shadow', 'living', 'under',
            'god', 'anointing', 'brings', 'stress', 'free', 'near', 'to'
        ],
        'Prayer & Intercession': [
            'prayer', 'pray', 'intercession', 'tongues', 'power', 'equipping',
            'incredible', 'speaking', 'wisdom', 'true'
        ],
        'Identity & Sonship': [
            'identity', 'sonship', 'christ', 'inheritance', 'gift', 'righteousness',
            'established', 'secure', 'christianity', 'believable', 'workmanship',
            'created', 'christ'
        ],
        'Joy & Happiness': [
            'joy', 'rejoice', 'happiness', 'gladness', 'wonderful', 'thoughts',
            'inspired', 'imagination', 'first', 'love', 'god', 'things', 'steal',
            'our'
        ],
        'Church & Ministry': [
            'church', 'congregation', 'ministry', 'pastor', 'delivering', 'people',
            'cultures', 'effective', 'winning', 'lost', 'bringers', 'wonderful'
        ],
        'Christmas & Easter': [
            'christmas', 'emmanuel', 'nativity', 'resurrection', 'cross', 'crucifixion',
            'easter', 'prophetic', 'message', 'just', 'about', 'day'
        ],
        'End Times & Prophecy': [
            'end', 'times', 'prophecy', 'revelation', 'apocalypse', 'elijah',
            'urgency', 'anointing', 'prophetic', 'alignment'
        ],
        'Discipleship & Growth': [
            'discipleship', 'growth', 'maturity', 'congregational', 'signs',
            'building', 'culture', 'presence', 'increasing', 'anointing'
        ],
        'Testimonies & Reports': [
            'testimonies', 'reports', 'europe', 'ministry', 'trip', 'south', 'africa',
            'grand', 'opening', 'session', 'qa'
        ]
    }
    
    # Check for theme matches
    for theme, keywords in theme_keywords.items():
        if any(keyword in title_lower for keyword in keywords):
            themes.append(theme)
    
    # If no themes found, add a general category
    if not themes:
        themes.append('General')
    
    return themes

def update_sermon_themes():
    """Update all sermons with optimized themes"""
    data = load_sermons()
    sermons = data['sermons']
    
    print("🔄 Updating sermon themes with optimized categorization...")
    
    # Update themes for each sermon
    for sermon in sermons:
        sermon['themes'] = extract_optimized_themes(sermon['title'])
    
    # Regenerate statistics
    theme_counts = defaultdict(int)
    year_counts = defaultdict(int)
    
    for sermon in sermons:
        for theme in sermon['themes']:
            theme_counts[theme] += 1
        year_counts[sermon['year']] += 1
    
    data['stats'] = {
        'themes': dict(theme_counts),
        'years': dict(year_counts),
        'total_sermons': len(sermons)
    }
    
    # Save updated data
    with open('sermon_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)
    
    print("✅ Updated sermon themes successfully!")
    
    # Show new theme distribution
    print("\n📊 NEW THEME DISTRIBUTION:")
    sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
    
    for theme, count in sorted_themes:
        if count > 0:
            percentage = (count / len(sermons)) * 100
            print(f"   • {theme}: {count} sermons ({percentage:.1f}%)")
    
    return data

def main():
    """Main function"""
    try:
        update_sermon_themes()
        print("\n🎉 Theme update complete! The directory will now use optimized thematic filters.")
    except Exception as e:
        print(f"❌ Error updating themes: {e}")

if __name__ == "__main__":
    main()
