import io
import requests
from pypdf import PdfReader
from urllib.parse import urlparse

def extract_pdf_text(path_or_url: str) -> str:
    """
    Extracts text from a local PDF file or a remote PDF URL.
    """
    parsed = urlparse(path_or_url)

    # Check if it's a URL
    if parsed.scheme in ("http", "https"):
        response = requests.get(path_or_url, timeout=10)
        response.raise_for_status()
        file_obj = io.BytesIO(response.content)
    else:
        # Treat as local file path
        file_obj = open(path_or_url, "rb")

    try:
        reader = PdfReader(file_obj)
        text_pages = []
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_pages.append(extracted)
        return "\n".join(text_pages)
    finally:
        if parsed.scheme not in ("http", "https"):
            file_obj.close()
