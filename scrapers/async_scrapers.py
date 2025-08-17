# async_scrapers.py
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json

# -----------------------------
# DuckDuckGo Scraper (Fallback for Reddit)
# -----------------------------
async def fetch_duckduckgo(session, keyword, max_results=10):
    url = f"https://html.duckduckgo.com/html/?q=site:reddit.com {keyword}"
    results = []
    try:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            for result in soup.select(".result__body")[:max_results]:
                title = result.select_one(".result__title")
                snippet = result.select_one(".result__snippet")
                link = result.select_one("a.result__a")
                if title and link:
                    results.append({
                        "platform": "reddit",
                        "title": title.get_text(strip=True),
                        "snippet": snippet.get_text(strip=True) if snippet else "",
                        "url": link["href"]
                    })
    except Exception as e:
        print("DuckDuckGo error:", e)
    return results

# -----------------------------
# Reddit API Scraper
# -----------------------------
async def fetch_reddit(session, keyword, max_results=10):
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
# Twitter Scraper (Basic)
# -----------------------------
async def fetch_twitter(session, keyword, max_results=10):
    url = f"https://twitter.com/search?q={keyword}&f=live"
    results = []
    try:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            tweets = soup.select("div[data-testid='tweet']")[:max_results]
            for t in tweets:
                text = t.get_text(separator=" ", strip=True)
                link_tag = t.select_one("a[href*='/status/']")
                link = f"https://twitter.com{link_tag['href']}" if link_tag else ""
                results.append({
                    "platform": "twitter",
                    "title": text[:50],
                    "snippet": text,
                    "url": link
                })
    except Exception as e:
        print("Twitter error:", e)
    return results

# -----------------------------
# Instagram Scraper (Basic)
# -----------------------------
async def fetch_instagram(session, keyword, max_results=10):
    url = f"https://www.instagram.com/explore/tags/{keyword}/"
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (LeadHunterAI Bot)"}
    try:
        async with session.get(url, headers=
