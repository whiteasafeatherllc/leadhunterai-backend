import requests
from bs4 import BeautifulSoup

def soup_from_url(url, headers=None):
    # Use a default User-Agent to avoid being blocked
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")
