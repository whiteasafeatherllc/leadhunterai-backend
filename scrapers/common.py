
import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

def fetch_html(url, timeout=20):
    with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=timeout) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.text

def soup_from_url(url):
    html = fetch_html(url)
    return BeautifulSoup(html, "html.parser")
