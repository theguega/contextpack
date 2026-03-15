import requests
import xml.etree.ElementTree as ET
import re
from typing import Optional, Dict

def fetch_arxiv_data(id_or_query: str) -> Optional[Dict[str, str]]:
    """
    Contacts the arXiv API and parses the response to get metadata and PDF URL.
    Returns a dictionary with 'title', 'summary', 'pdf_url', and 'entry_id'.
    """
    base_url = "http://export.arxiv.org/api/query"

    # Check if it looks like an arXiv ID (e.g. 1706.03762 or quant-ph/0401062)
    # A simple regex for arXiv IDs:
    arxiv_id_pattern = re.compile(r'^\d{4}\.\d{4,5}(v\d+)?$|^[a-z\-]+(\.[A-Z]{2})?/\d{7}(v\d+)?$')

    if arxiv_id_pattern.match(id_or_query):
        params = {"id_list": id_or_query, "max_results": 1}
    else:
        # Search query
        params = {"search_query": f"all:{id_or_query}", "max_results": 1}

    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    # The arXiv API uses Atom namespace
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    entry = root.find("atom:entry", ns)
    if entry is None:
        return None

    title = entry.find("atom:title", ns).text.strip() if entry.find("atom:title", ns) is not None else "Unknown Title"
    summary = entry.find("atom:summary", ns).text.strip() if entry.find("atom:summary", ns) is not None else "No summary"
    entry_id = entry.find("atom:id", ns).text.strip() if entry.find("atom:id", ns) is not None else id_or_query

    pdf_url = None
    for link in entry.findall("atom:link", ns):
        if link.get("title") == "pdf" or link.get("type") == "application/pdf":
            pdf_url = link.get("href")
            break

    if pdf_url and not pdf_url.endswith(".pdf"):
        pdf_url += ".pdf"

    return {
        "title": title,
        "summary": summary,
        "pdf_url": pdf_url,
        "entry_id": entry_id
    }
