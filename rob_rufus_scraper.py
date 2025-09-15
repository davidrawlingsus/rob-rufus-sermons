#!/usr/bin/env python3
"""
Rob Rufus Sermon Scraper
Downloads all English language sermons from City Church International
"""

import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RobRufusScraper:
    def __init__(self, base_url="https://www.ccihk.com/audio-sermon-english/category/Rob+Rufus"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.download_dir = "Rob_Rufus_Sermons"
        self.downloaded_files = set()
        
        # Create download directory
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Load already downloaded files to avoid duplicates
        self._load_downloaded_files()
    
    def _load_downloaded_files(self):
        """Load list of already downloaded files to avoid duplicates"""
        if os.path.exists(self.download_dir):
            for filename in os.listdir(self.download_dir):
                if filename.endswith('.mp3'):
                    self.downloaded_files.add(filename)
    
    def _get_soup(self, url, max_retries=3):
        """Fetch URL content with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                    return None
    
    def _sanitize_filename(self, filename):
        """Sanitize filename for filesystem compatibility"""
        # Remove or replace invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove extra spaces and replace with underscores
        filename = re.sub(r'\s+', '_', filename)
        # Remove multiple underscores
        filename = re.sub(r'_+', '_', filename)
        # Remove leading/trailing underscores
        filename = filename.strip('_')
        return filename
    
    def _extract_date_from_sermon(self, soup, sermon_url):
        """Extract date from sermon page"""
        # Try multiple selectors for date
        date_selectors = [
            'time[datetime]',
            '.date',
            '.sermon-date',
            '.post-date',
            'span.date',
            'div.date'
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                # Try datetime attribute first
                if date_elem.get('datetime'):
                    try:
                        return datetime.fromisoformat(date_elem['datetime'].replace('Z', '+00:00'))
                    except:
                        pass
                
                # Try text content
                date_text = date_elem.get_text().strip()
                if date_text:
                    # Try various date formats
                    date_formats = [
                        '%B %d, %Y',
                        '%d %B %Y',
                        '%Y-%m-%d',
                        '%m/%d/%Y',
                        '%d/%m/%Y'
                    ]
                    
                    for fmt in date_formats:
                        try:
                            return datetime.strptime(date_text, fmt)
                        except:
                            continue
        
        # If no date found, try to extract from URL or use current date
        logger.warning(f"Could not extract date from {sermon_url}, using current date")
        return datetime.now()
    
    def _extract_title_from_sermon(self, soup, sermon_url):
        """Extract title from sermon page"""
        # Try multiple selectors for title
        title_selectors = [
            'h1',
            '.sermon-title',
            '.post-title',
            '.entry-title',
            'title'
        ]
        
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text().strip()
                if title and title != "City Church International":
                    return title
        
        # Fallback: extract from URL
        url_path = urlparse(sermon_url).path
        title = url_path.split('/')[-1].replace('-', ' ').title()
        return title
    
    def _find_download_link(self, soup, sermon_url):
        """Find the MP3 download link on sermon page"""
        # Look for Squarespace audio embed (most common)
        audio_embed = soup.select_one('.sqs-audio-embed')
        if audio_embed and audio_embed.get('data-url'):
            mp3_url = audio_embed['data-url']
            if mp3_url.endswith('.mp3'):
                return mp3_url
        
        # Look for various download link patterns
        download_selectors = [
            'a[href*=".mp3"]',
            'a[href*="download"]',
            'a[href*="audio"]',
            'a[href*="sermon"]',
            '.download-link',
            '.audio-download',
            'a[download]'
        ]
        
        for selector in download_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute
                    full_url = urljoin(sermon_url, href)
                    if full_url.endswith('.mp3') or 'download' in href.lower():
                        return full_url
        
        # Look for audio elements
        audio_elem = soup.select_one('audio source')
        if audio_elem and audio_elem.get('src'):
            return urljoin(sermon_url, audio_elem['src'])
        
        return None
    
    def _download_mp3(self, mp3_url, filename):
        """Download MP3 file"""
        try:
            response = self.session.get(mp3_url, stream=True, timeout=60)
            response.raise_for_status()
            
            filepath = os.path.join(self.download_dir, filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Downloaded: {filename}")
            self.downloaded_files.add(filename)
            return True
            
        except Exception as e:
            logger.error(f"Failed to download {mp3_url}: {e}")
            return False
    
    def _process_sermon_page(self, sermon_url):
        """Process individual sermon page"""
        logger.info(f"Processing sermon: {sermon_url}")
        
        soup = self._get_soup(sermon_url)
        if not soup:
            return False
        
        # Extract sermon details
        title = self._extract_title_from_sermon(soup, sermon_url)
        date = self._extract_date_from_sermon(soup, sermon_url)
        
        # Find download link
        mp3_url = self._find_download_link(soup, sermon_url)
        if not mp3_url:
            logger.warning(f"No download link found for {sermon_url}")
            return False
        
        # Create filename
        date_str = date.strftime('%Y-%m-%d')
        sanitized_title = self._sanitize_filename(title)
        filename = f"{date_str}_{sanitized_title}.mp3"
        
        # Check if already downloaded
        if filename in self.downloaded_files:
            logger.info(f"Already downloaded: {filename}")
            return True
        
        # Download the file
        return self._download_mp3(mp3_url, filename)
    
    def _get_sermon_links_from_page(self, soup, page_url):
        """Extract sermon links from a listing page"""
        sermon_links = []
        
        # Look for various link patterns
        link_selectors = [
            'article a[href*="audio-sermon-english"]',
            '.post a[href*="audio-sermon-english"]',
            '.sermon-item a[href]',
            'a[href*="audio-sermon-english"]'
        ]
        
        for selector in link_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href and 'audio-sermon-english' in href:
                    # Filter out category, tag, author, and other non-sermon links
                    if not any(x in href for x in ['category', 'tag', 'author', '?offset', '?format']):
                        full_url = urljoin(page_url, href)
                        if full_url not in sermon_links:
                            sermon_links.append(full_url)
        
        return sermon_links
    
    def _get_next_page_url(self, soup, current_url):
        """Find the next page URL (Older link)"""
        # Look for pagination links - Squarespace uses different structure
        pagination_links = soup.find_all('a', href=True)
        for link in pagination_links:
            text = link.get_text().strip().lower()
            href = link.get('href')
            if 'older' in text and href:
                return urljoin(current_url, href)
        
        # Also look for next page links
        next_link = soup.select_one('a[rel="next"]')
        if next_link and next_link.get('href'):
            return urljoin(current_url, next_link['href'])
        
        return None
    
    def scrape_all_sermons(self):
        """Main method to scrape all sermons"""
        logger.info("Starting Rob Rufus sermon scraping...")
        
        current_url = self.base_url
        total_processed = 0
        total_downloaded = 0
        
        while current_url:
            logger.info(f"Processing page: {current_url}")
            
            soup = self._get_soup(current_url)
            if not soup:
                logger.error(f"Failed to load page: {current_url}")
                break
            
            # Get sermon links from current page
            sermon_links = self._get_sermon_links_from_page(soup, current_url)
            logger.info(f"Found {len(sermon_links)} sermons on this page")
            
            # Process each sermon
            for sermon_url in sermon_links:
                total_processed += 1
                if self._process_sermon_page(sermon_url):
                    total_downloaded += 1
                
                # Be respectful - add delay between requests
                time.sleep(1)
            
            # Find next page
            current_url = self._get_next_page_url(soup, current_url)
            
            if current_url:
                logger.info(f"Moving to next page: {current_url}")
                time.sleep(2)  # Delay between pages
        
        logger.info(f"Scraping completed. Processed: {total_processed}, Downloaded: {total_downloaded}")
        return total_downloaded

def main():
    """Main function"""
    scraper = RobRufusScraper()
    
    try:
        downloaded_count = scraper.scrape_all_sermons()
        print(f"\nScraping completed successfully!")
        print(f"Total sermons downloaded: {downloaded_count}")
        print(f"Files saved in: {scraper.download_dir}")
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise

if __name__ == "__main__":
    main()
