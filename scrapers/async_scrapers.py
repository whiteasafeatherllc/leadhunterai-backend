import aiohttp
import asyncio
from bs4 import BeautifulSoup
import httpx

# -----------------------------
# Reddit Scraper
# -----------------------------
async def fetch_reddit(session, keyword, max_results=10):
    url = f"https://www.reddit.com/search.json?q={keyword}&limit={max_results}"
    results = []
    headers = {"User-Agent": "Mozilla/5.0 (LeadHunterAI Bot)"}
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return results
            data = await resp.json()
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
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
# DuckDuckGo Fallback Scraper
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
# Exported function
# -----------------------------
def fetch_leads_sync(keyword, max_results=15):
    return asyncio.run(fetch_leads(keyword, max_results=max_results))
