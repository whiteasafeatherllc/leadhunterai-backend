import aiohttp
import asyncio
from bs4 import BeautifulSoup

# -----------------------------
# DuckDuckGo Scraper (Fallback)
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
                        "platform": "duckduckgo",
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
    headers = {"User-Agent": "Mozilla/5.0 (LeadHunterAI Bot)", "Accept": "application/json"}
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
# Twitter / Instagram / TikTok Scrapers
# -----------------------------
async def fetch_twitter(session, keyword, max_results=10):
    url = f"https://nitter.net/search?f=tweets&q={keyword}"
    results = []
    try:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            for tweet in soup.select(".timeline-item")[:max_results]:
                content = tweet.select_one(".tweet-content")
                link = tweet.select_one("a.timeline-link")
                if content and link:
                    results.append({
                        "platform": "twitter",
                        "title": content.get_text(strip=True),
                        "snippet": content.get_text(strip=True),
                        "url": "https://nitter.net" + link["href"]
                    })
    except Exception as e:
        print("Twitter fetch error:", e)
    return results

async def fetch_instagram(session, keyword, max_results=10):
    url = f"https://www.instagram.com/web/search/topsearch/?context=user&query={keyword}"
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            for user in data.get("users", [])[:max_results]:
                username = user.get("user", {}).get("username", "")
                if username:
                    results.append({
                        "platform": "instagram",
                        "title": username,
                        "snippet": f"Instagram user {username}",
                        "url": f"https://instagram.com/{username}"
                    })
    except Exception as e:
        print("Instagram fetch error:", e)
    return results

async def fetch_tiktok(session, keyword, max_results=10):
    url = f"https://www.tiktok.com/tag/{keyword}"
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with session.get(url, headers=headers) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            for post in soup.select("a")[:max_results]:
                href = post.get("href")
                if href and "video" in href:
                    results.append({
                        "platform": "tiktok",
                        "title": "TikTok post",
                        "snippet": "TikTok content",
                        "url": f"https://www.tiktok.com{href}"
                    })
    except Exception as e:
        print("TikTok fetch error:", e)
    return results

# -----------------------------
# Master collector
# -----------------------------
async def fetch_leads(keyword, max_results=15):
    async with aiohttp.ClientSession() as session:
        reddit_results, ddg_results = await asyncio.gather(
            fetch_reddit(session, keyword, max_results=max_results),
            fetch_duckduckgo(session, keyword, max_results=max_results),
        )
        leads = reddit_results or ddg_results
        return leads

# -----------------------------
# Exported synchronous function
# -----------------------------
def search_posts(keyword, max_results=15):
    return asyncio.run(fetch_leads(keyword, max_results=max_results))
