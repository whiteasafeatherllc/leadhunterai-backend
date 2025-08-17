import aiohttp
import asyncio
from bs4 import BeautifulSoup

# -----------------------------
# DuckDuckGo Scraper
# -----------------------------
async def fetch_duckduckgo(session, keyword):
    url = f"https://html.duckduckgo.com/html/?q={keyword}"
    results = []
    try:
        async with session.get(url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            for result in soup.select(".result__body"):
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
# Reddit Scraper
# -----------------------------
async def fetch_reddit(session, keyword):
    url = f"https://www.reddit.com/search.json?q={keyword}&limit=10"
    results = []
    headers = {"User-Agent": "LeadHunterAI/1.0"}
    try:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            for child in data.get("data", {}).get("children", []):
                post = child["data"]
                results.append({
                    "platform": "reddit",
                    "title": post.get("title"),
                    "snippet": post.get("selftext")[:150] if post.get("selftext") else "",
                    "url": f"https://reddit.com{post.get('permalink')}"
                })
    except Exception as e:
        print("Reddit error:", e)
    return results

# -----------------------------
# Master collector
# -----------------------------
async def fetch_leads(keyword):
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_duckduckgo(session, keyword),
            fetch_reddit(session, keyword),
            # 👉 add your other scrapers here (twitter, fb, linkedin, etc.)
        ]
        results = await asyncio.gather(*tasks)
        leads = [item for sublist in results for item in sublist]
        return leads
