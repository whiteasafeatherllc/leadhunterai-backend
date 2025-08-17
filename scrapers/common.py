import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/123.0.0.0 Safari/537.36"
}

def fetch_html(url, timeout=20):
    """
    Fetches the HTML content of a URL using httpx.
    Raises an exception if the request fails.
    """
    with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=timeout) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text

def soup_from_url(url):
    """
    Returns a BeautifulSoup object from the HTML of the given URL.
    """
    html = fetch_html(url)
    return BeautifulSoup(html, "html.parser")
