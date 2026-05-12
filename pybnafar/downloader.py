import requests
from bs4 import BeautifulSoup
import os
import time
from typing import List, Dict
from .utils import logger, sanitize_filename
from .constants import OPENDATASUS_CKAN_API, OPENDATASUS_URL

class BnafarDownloader:
    """
    Intelligent Downloader: Official CKAN API + Scraper Fallback with Resilience.
    """
    
    def __init__(self, workspace_dir: str):
        self.workspace_dir = workspace_dir
        os.makedirs(workspace_dir, exist_ok=True)

    def fetch_sources(self, use_api: bool = True) -> List[Dict[str, str]]:
        """Attempts to fetch data sources with fallback logic."""
        sources = []
        if use_api:
            try:
                # API request with timeout and session for reuse
                with requests.Session() as s:
                    response = s.get(OPENDATASUS_CKAN_API, timeout=15)
                    response.raise_for_status()
                    resources = response.json().get('result', {}).get('resources', [])
                    for res in resources:
                        if res.get('format', '').lower() == 'csv':
                            sources.append({'title': res['name'], 'url': res['url']})
                if sources: 
                    return sources
            except Exception as e:
                logger.warning(f"Official API unavailable, switching to scraping: {e}")

        # Fallback Scraping
        try:
            response = requests.get(OPENDATASUS_URL, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            for item in soup.find_all('li', class_='resource-item'):
                link = item.find('a', class_='resource-url-analytics')
                if link:
                    sources.append({
                        'title': item.find('a', class_='heading').get('title').strip(),
                        'url': link['href']
                    })
        except Exception as e:
            logger.error(f"Total failure in fetching data sources: {e}")
        
        return sources

    def download(self, url: str, filename: str, retries: int = 3) -> str:
        """Download with integrity check and automatic retries."""
        path = os.path.join(self.workspace_dir, sanitize_filename(filename))
        
        for attempt in range(retries):
            try:
                with requests.get(url, stream=True, timeout=60) as r:
                    r.raise_for_status()
                    with open(path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
                return path
            except Exception as e:
                if attempt < retries - 1:
                    wait = (attempt + 1) * 2
                    logger.warning(f"Download failed, retrying in {wait}s... ({e})")
                    time.sleep(wait)
                else:
                    logger.error(f"Critical failure downloading {url}: {e}")
                    raise
        return path

