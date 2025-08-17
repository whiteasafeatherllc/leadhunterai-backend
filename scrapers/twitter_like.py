import asyncio
from scrapers.async_scrapers import fetch_twitter, fetch_instagram, fetch_tiktok

# -----------------------------
# Twitter
# -----------------------------
def search_twitter(keyword: str, max_results: int = 10):
    """Sync wrapper for async Twitter scraper"""
    return asyncio.run(fetch_twitter(keyword=keyword, max_results=max_results))


# -----------------------------
# Instagram
# -----------------------------
def search_instagram(keyword: str, max_results: int = 10):
    """Sync wrapper for async Instagram scraper"""
    return asyncio.run(fetch_instagram(keyword=keyword, max_results=max_results))


# -----------------------------
# TikTok
# -----------------------------
def search_tiktok(keyword: str, max_results: int = 10):
    """Sync wrapper for async TikTok scraper"""
    return asyncio.run(fetch_tiktok(keyword=keyword, max_results=max_results))
