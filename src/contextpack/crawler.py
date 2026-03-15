import trafilatura
from urllib.parse import urlparse, urljoin
from typing import Set, List, Dict
import httpx
from bs4 import BeautifulSoup
import re

DOCS_KEYWORDS = ["docs", "guide", "tutorial", "reference", "concepts"]

def is_same_domain(url1: str, url2: str) -> bool:
    return urlparse(url1).netloc == urlparse(url2).netloc

def is_doc_url(url: str) -> bool:
    url_lower = url.lower()
    return any(keyword in url_lower for keyword in DOCS_KEYWORDS)

class Crawler:
    def __init__(self, base_url: str, max_depth: int = 2, max_pages: int = 10, timeout: int = 10):
        self.base_url = base_url
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited_urls: Set[str] = set()
        self.content_map: Dict[str, str] = {}

    def get_links(self, html: str, current_url: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            full_url = urljoin(current_url, a['href']).split('#')[0]
            if is_same_domain(self.base_url, full_url) and full_url not in self.visited_urls:
                if is_doc_url(full_url):
                    links.append(full_url)
        return list(set(links))

    def crawl(self, url: str, depth: int = 0):
        if len(self.visited_urls) >= self.max_pages or depth > self.max_depth:
            return

        if url in self.visited_urls:
            return

        print(f"Crawling: {url}")
        self.visited_urls.add(url)

        try:
            with httpx.Client(timeout=self.timeout, follow_redirects=True) as client:
                response = client.get(url)
                if response.status_code != 200 or len(response.content) > 1_000_000:
                    return
                
                html = response.text
                content = trafilatura.extract(html, url=url, output_format="markdown", include_links=True)
                if content:
                    self.content_map[url] = content

            if depth < self.max_depth:
                links = self.get_links(html, url)
                for link in links:
                    self.crawl(link, depth + 1)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

def crawl_documentation(url: str, max_depth: int = 2, max_pages: int = 10) -> Dict[str, str]:
    crawler = Crawler(url, max_depth=max_depth, max_pages=max_pages)
    crawler.crawl(url)
    return crawler.content_map
