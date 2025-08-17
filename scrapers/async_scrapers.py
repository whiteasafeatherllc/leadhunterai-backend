import aiohttp
import asyncio
from bs4 import BeautifulSoup
import httpx
import json
from typing import List

# -----------------------------
# Reddit API Scraper
# -----------------------------
async def fetch_reddit(session, keyword: str, max_results: int = 10) -> List[dict]:
    url = f"https://www.reddit.com/search.json?q={keyword}&limit={max_results}"
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (LeadHunterAI Bot)",
        "Accept": "application/json",
    }
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"Reddit returned status {resp.status}")
                return results
            data = await resp.json()
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                if not post:
                    continue
                results.append({
                    "platform": "reddit",
                    "title": post.get("title", "(no title)"),
                    "snippet": (post.get("selftext") or "")[:150],
                    "url": f"https://reddit.com{post.get('permalink', '')}"
                })
                if len(results) >= max_results:
                    break
    except Exception as e:
        print("Reddit error:", e)
    return results

# -----------------------------
# Instagram Scraper
# -----------------------------
async def fetch_instagram(session, keyword: str, max_results: int = 10) -> List[dict]:
    url = f"https://i.instagram.com/api/v1/media/search/?q={keyword}&count={max_results}"
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (LeadHunterAI Bot)",
        "x-ig-app-id": "936619743392459",  # Instagram app ID
    }
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"Instagram returned status {resp.status}")
                return results
            data = await resp.json()
            for item in data.get("items", []):
                results.append({
                    "platform": "instagram",
                    "title": item.get("caption", "").get("text", "(no caption)"),
                    "snippet": item.get("caption", "").get("text", "")[:150],
                    "url": f"https://www.instagram.com/p/{item.get('code', '')}/"
                })
                if len(results) >= max_results:
                    break
    except Exception as e:
        print("Instagram error:", e)
    return results

# -----------------------------
# TikTok Scraper
# -----------------------------
async def fetch_tiktok(session, keyword: str, max_results: int = 10) -> List[dict]:
    url = f"https://www.tiktok.com/api/search/item/?keyword={keyword}&count={max_results}"
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (LeadHunterAI Bot)",
    }
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                print(f"TikTok returned status {resp.status}")
                return results
            data = await resp.json()
            for item in data.get("items", []):
                results.append({
                    "platform": "tiktok",
                    "title": item.get("desc", "(no description)"),
                    "snippet": item.get("desc", "")[:150],
                    "url": f"https://www.tiktok.com/@{item.get('author', {}).get('unique_id', '')}/video/{item.get('id', '')}"
                })
                if len(results) >= max_results:
                    break
    except Exception as e:
        print("TikTok error:", e)
    return results

# -----------------------------
# Master Scraper
# -----------------------------
async def fetch_leads(keyword: str, max_results: int = 15) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        reddit_results, instagram_results, tiktok_results = await asyncio.gather(
            fetch_reddit(session, keyword, max_results=max_results),
            fetch_instagram(session, keyword, max_results=max_results),
            fetch_tiktok(session, keyword, max_results=max_results),
        )
        leads = reddit_results + instagram_results + tiktok_results
        return leads

# -----------------------------
# Exported Function
# -----------------------------
def search_posts(keyword: str, max_results: int = 15) -> List[dict]:
    return asyncio.run(fetch_leads(keyword, max_results=max_results))
