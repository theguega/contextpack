import httpx
from bs4 import BeautifulSoup
from typing import List

def search_duckduckgo(query: str, max_results: int = 5) -> List[str]:
    """
    Performs a DuckDuckGo HTML search and returns the top result URLs.
    """
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        with httpx.Client(timeout=10, follow_redirects=True) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for result in soup.find_all('a', class_='result__url', href=True):
                if len(results) >= max_results:
                    break
                results.append(result['href'].strip())
                
            return results
    except Exception as e:
        print(f"Error searching DuckDuckGo: {e}")
        return []
