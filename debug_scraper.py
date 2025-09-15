#!/usr/bin/env python3
"""
Debug script to examine the structure of sermon pages
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def debug_sermon_page(url):
    """Debug a single sermon page to understand its structure"""
    print(f"Debugging: {url}")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        
        # Look for all links
        print("\n=== ALL LINKS ===")
        links = soup.find_all('a', href=True)
        for i, link in enumerate(links[:20]):  # Show first 20 links
            href = link.get('href')
            text = link.get_text().strip()
            print(f"{i+1}. {href} - '{text}'")
        
        # Look for audio elements
        print("\n=== AUDIO ELEMENTS ===")
        audio_elements = soup.find_all('audio')
        for audio in audio_elements:
            print(f"Audio: {audio}")
            sources = audio.find_all('source')
            for source in sources:
                print(f"  Source: {source.get('src')}")
        
        # Look for download-related elements
        print("\n=== DOWNLOAD ELEMENTS ===")
        download_elements = soup.find_all(['a', 'button'], string=lambda text: text and 'download' in text.lower())
        for elem in download_elements:
            print(f"Download element: {elem}")
        
        # Look for MP3 links
        print("\n=== MP3 LINKS ===")
        mp3_links = soup.find_all('a', href=lambda href: href and '.mp3' in href)
        for link in mp3_links:
            print(f"MP3 link: {link.get('href')} - '{link.get_text().strip()}'")
        
        # Look for any JavaScript that might load the audio
        print("\n=== SCRIPT TAGS ===")
        scripts = soup.find_all('script')
        for i, script in enumerate(scripts[:5]):  # Show first 5 scripts
            if script.string and ('mp3' in script.string.lower() or 'audio' in script.string.lower()):
                print(f"Script {i+1}: {script.string[:200]}...")
        
        # Save HTML for manual inspection
        with open('debug_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"\nHTML saved to debug_page.html")
        
    except Exception as e:
        print(f"Error: {e}")

def debug_listing_page(url):
    """Debug the listing page to understand link structure"""
    print(f"Debugging listing page: {url}")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print(f"Status Code: {response.status_code}")
        
        # Look for sermon links
        print("\n=== POTENTIAL SERMON LINKS ===")
        all_links = soup.find_all('a', href=True)
        sermon_links = []
        
        for link in all_links:
            href = link.get('href')
            text = link.get_text().strip()
            if href and 'audio-sermon-english' in href and 'category' not in href and 'tag' not in href and 'author' not in href:
                sermon_links.append((href, text))
        
        for i, (href, text) in enumerate(sermon_links[:10]):  # Show first 10
            print(f"{i+1}. {href} - '{text}'")
        
        # Look for pagination
        print("\n=== PAGINATION LINKS ===")
        pagination_links = soup.find_all('a', href=True)
        for link in pagination_links:
            text = link.get_text().strip().lower()
            if 'older' in text or 'next' in text or 'page' in text:
                print(f"Pagination: {link.get('href')} - '{link.get_text().strip()}'")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Test with a known sermon page
    test_sermon_url = "https://www.ccihk.com/audio-sermon-english/encounters-with-god-rob-rufus"
    debug_sermon_page(test_sermon_url)
    
    print("\n" + "="*50 + "\n")
    
    # Test with the listing page
    listing_url = "https://www.ccihk.com/audio-sermon-english/category/Rob+Rufus"
    debug_listing_page(listing_url)
