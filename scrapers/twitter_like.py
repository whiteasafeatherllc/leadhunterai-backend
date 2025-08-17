
from .duckduckgo import search

def search_twitter(query, max_results=20):
    return search(query, site="twitter.com", max_results=max_results)

def search_instagram(query, max_results=20):
    return search(query, site="instagram.com", max_results=max_results)

def search_tiktok(query, max_results=20):
    return search(query, site="tiktok.com", max_results=max_results)
