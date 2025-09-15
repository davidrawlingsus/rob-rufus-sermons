#!/usr/bin/env python3
"""
Deep analysis of sermon titles to suggest optimal thematic filter chips
"""

import json
import re
from collections import defaultdict, Counter
from datetime import datetime

def load_sermons():
    """Load sermon data"""
    with open('sermon_metadata.json', 'r') as f:
        data = json.load(f)
    return data['sermons']

def extract_keywords_from_title(title):
    """Extract meaningful keywords from sermon title"""
    # Remove common words and clean up
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
    }
    
    # Clean and split title
    words = re.findall(r'\b[a-zA-Z]+\b', title.lower())
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords

def analyze_sermon_themes():
    """Analyze all sermon titles to identify key themes"""
    sermons = load_sermons()
    
    # Collect all keywords
    all_keywords = []
    keyword_sermons = defaultdict(list)
    
    for sermon in sermons:
        keywords = extract_keywords_from_title(sermon['title'])
        all_keywords.extend(keywords)
        
        for keyword in keywords:
            keyword_sermons[keyword].append(sermon)
    
    # Count keyword frequency
    keyword_counts = Counter(all_keywords)
    
    # Group related keywords into themes
    theme_groups = {
        'Grace & Gospel': [
            'grace', 'gospel', 'righteousness', 'forgiveness', 'mercy', 'love', 'compassion',
            'covenant', 'blessing', 'favor', 'finished', 'work', 'cross', 'blood'
        ],
        'Faith & Trust': [
            'faith', 'believe', 'trust', 'confidence', 'assurance', 'certainty', 'promises',
            'inheritance', 'blessings', 'miracles', 'supernatural'
        ],
        'Anointing & Power': [
            'anointing', 'anointed', 'power', 'supernatural', 'miracles', 'manifestation',
            'glory', 'presence', 'heaven', 'divine', 'increasing', 'greater'
        ],
        'Holy Spirit': [
            'spirit', 'holy', 'tongues', 'manifestation', 'presence', 'glory', 'cloud',
            'moving', 'living', 'person', 'comfort', 'joy'
        ],
        'Healing & Miracles': [
            'healing', 'heal', 'sick', 'miracle', 'miracles', 'power', 'supernatural',
            'compassion', 'forgiveness', 'twin', 'remembering'
        ],
        'Worship & Praise': [
            'worship', 'praise', 'glory', 'presence', 'throne', 'room', 'attracts',
            'manifestation', 'humility', 'ultimate'
        ],
        'Identity & Sonship': [
            'identity', 'sonship', 'christ', 'inheritance', 'gift', 'righteousness',
            'established', 'secure', 'christianity', 'believable'
        ],
        'Fear & Courage': [
            'fear', 'fearless', 'courage', 'bold', 'living', 'times', 'judgement',
            'wrath', 'condemnation', 'guilt'
        ],
        'Kingdom & Authority': [
            'kingdom', 'reign', 'authority', 'power', 'government', 'shoulders',
            'heaven', 'earth', 'colonising', 'kiss'
        ],
        'Freedom & Liberation': [
            'freedom', 'free', 'liberated', 'liberty', 'orphan', 'spirit', 'masks',
            'religious', 'political', 'control'
        ],
        'Joy & Happiness': [
            'joy', 'rejoice', 'happiness', 'gladness', 'wonderful', 'thoughts',
            'inspired', 'imagination', 'first', 'love'
        ],
        'Peace & Rest': [
            'peace', 'rest', 'comfort', 'covenant', 'shadow', 'living', 'under',
            'god', 'anointing', 'brings'
        ],
        'Prayer & Intercession': [
            'prayer', 'pray', 'intercession', 'tongues', 'power', 'equipping',
            'incredible', 'speaking'
        ],
        'Word & Truth': [
            'word', 'scripture', 'bible', 'truth', 'knowledge', 'key', 'restoring',
            'gospel', 'grace', 'law'
        ],
        'Church & Ministry': [
            'church', 'congregation', 'ministry', 'pastor', 'delivering', 'people',
            'cultures', 'effective', 'winning', 'lost'
        ],
        'Christmas & Easter': [
            'christmas', 'emmanuel', 'nativity', 'resurrection', 'cross', 'crucifixion',
            'easter', 'prophetic', 'message'
        ],
        'End Times & Prophecy': [
            'end', 'times', 'prophecy', 'revelation', 'apocalypse', 'elijah',
            'urgency', 'anointing', 'prophetic'
        ],
        'Spiritual Warfare': [
            'warfare', 'enemy', 'outwit', 'accusation', 'spirit', 'religious',
            'political', 'control', 'overthrowing'
        ],
        'Discipleship & Growth': [
            'discipleship', 'growth', 'maturity', 'congregational', 'signs',
            'building', 'culture', 'presence', 'increasing'
        ],
        'Testimonies & Reports': [
            'testimonies', 'reports', 'europe', 'ministry', 'trip', 'south', 'africa',
            'grand', 'opening', 'session'
        ]
    }
    
    # Analyze which themes are most represented
    theme_stats = {}
    for theme, keywords in theme_groups.items():
        matching_sermons = set()
        for keyword in keywords:
            if keyword in keyword_sermons:
                for sermon in keyword_sermons[keyword]:
                    matching_sermons.add(sermon['filename'])
        theme_stats[theme] = len(matching_sermons)
    
    # Sort themes by frequency
    sorted_themes = sorted(theme_stats.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_themes, keyword_counts, theme_groups

def suggest_optimal_chips():
    """Suggest optimal thematic filter chips based on analysis"""
    sorted_themes, keyword_counts, theme_groups = analyze_sermon_themes()
    
    print("🎯 THEMATIC FILTER CHIP ANALYSIS")
    print("=" * 60)
    print()
    
    print("📊 CURRENT THEME DISTRIBUTION:")
    for theme, count in sorted_themes:
        if count > 0:
            print(f"   • {theme}: {count} sermons")
    print()
    
    # Suggest optimal chips (themes with 10+ sermons)
    optimal_chips = [(theme, count) for theme, count in sorted_themes if count >= 10]
    
    print("🎯 SUGGESTED OPTIMAL FILTER CHIPS:")
    print("(Themes with 10+ sermons for meaningful filtering)")
    print()
    
    for i, (theme, count) in enumerate(optimal_chips, 1):
        print(f"{i:2d}. {theme:<25} ({count:3d} sermons)")
    
    print()
    print("💡 RECOMMENDATIONS:")
    print()
    
    # Top 12 most useful themes
    top_themes = optimal_chips[:12]
    print("🏆 TOP 12 MOST USEFUL FILTER CHIPS:")
    for theme, count in top_themes:
        print(f"   • {theme} ({count} sermons)")
    
    print()
    print("📱 MOBILE-FIRST CONSIDERATIONS:")
    print("   • Limit to 8-10 chips for mobile screens")
    print("   • Use shorter, clearer names")
    print("   • Group related themes if needed")
    
    print()
    print("🎨 SUGGESTED MOBILE CHIPS (8 most useful):")
    mobile_chips = [
        ("Grace & Gospel", optimal_chips[0][1] if optimal_chips else 0),
        ("Anointing & Power", optimal_chips[1][1] if len(optimal_chips) > 1 else 0),
        ("Holy Spirit", optimal_chips[2][1] if len(optimal_chips) > 2 else 0),
        ("Faith & Trust", optimal_chips[3][1] if len(optimal_chips) > 3 else 0),
        ("Worship & Praise", optimal_chips[4][1] if len(optimal_chips) > 4 else 0),
        ("Healing & Miracles", optimal_chips[5][1] if len(optimal_chips) > 5 else 0),
        ("Identity & Sonship", optimal_chips[6][1] if len(optimal_chips) > 6 else 0),
        ("Kingdom & Authority", optimal_chips[7][1] if len(optimal_chips) > 7 else 0)
    ]
    
    for theme, count in mobile_chips:
        if count > 0:
            print(f"   • {theme} ({count} sermons)")
    
    return optimal_chips, mobile_chips

def analyze_keyword_patterns():
    """Analyze keyword patterns for additional insights"""
    sorted_themes, keyword_counts, theme_groups = analyze_sermon_themes()
    
    print()
    print("🔍 KEYWORD ANALYSIS:")
    print("=" * 40)
    print()
    
    print("🔥 MOST FREQUENT KEYWORDS:")
    top_keywords = keyword_counts.most_common(20)
    for keyword, count in top_keywords:
        print(f"   • {keyword}: {count} times")
    
    print()
    print("📈 THEME COVERAGE ANALYSIS:")
    total_sermons = len(load_sermons())
    
    for theme, count in sorted_themes[:10]:
        if count > 0:
            percentage = (count / total_sermons) * 100
            print(f"   • {theme}: {count} sermons ({percentage:.1f}%)")

def main():
    """Main analysis function"""
    print("🎵 ROB RUFUS SERMON THEME ANALYSIS")
    print("=" * 60)
    print()
    
    try:
        optimal_chips, mobile_chips = suggest_optimal_chips()
        analyze_keyword_patterns()
        
        print()
        print("✅ ANALYSIS COMPLETE!")
        print("Use these insights to optimize your filter chips for better user experience.")
        
    except FileNotFoundError:
        print("❌ sermon_metadata.json not found. Run analyze_sermons.py first.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
