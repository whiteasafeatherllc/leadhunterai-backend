import aiohttp
import asyncio
from bs4 import BeautifulSoup
import urllib.parse

async def fetch_reddit(keyword):
    url = f"https://www.reddit.com/search.json?q={urllib.parse.quote(keyword)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return []
            data = await resp.json()
            posts = data.get("data", {}).get("children", [])
            results = []
            for post in posts[:5]:  # Limit to 5 results
                p = post["data"]
                results.append({
                    "platform": "reddit",
                    "title": p.get("title", ""),
                    "snippet": p.get("selftext", "")[:150],
                    "url": f"https://reddit.com{p.get('permalink', '')}"
                })
            return results

async def fetch_duckduckgo(keyword):
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(keyword)}"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []
            for a in soup.find_all("a", class_="result__a")[:5]:
                parent = a.find_parent("div", class_="result")
                snippet_tag = parent.find("a", class_="result__snippet") if parent else None
                results.append({
                    "platform": "duckduckgo",
                    "title": a.get_text(),
                    "snippet": snippet_tag.get_text()[:150] if snippet_tag else "",
                    "url": a.get("href")
                })
            return results

async def fetch_twitter(keyword):
    url = f"https://twitter.com/search?q={urllib.parse.quote(keyword)}&f=live"
    headers = {"User-Agent": "Mozilla/5.0"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            results = []
            tweets = soup.find_all("div", {"data-testid": "tweet"})[:5]
            for t in tweets:
                content = t.get_text(separator=" ", strip=True)
                link_tag = t.find("a", href=True)
                url = f"https://twitter.com{link_tag['href']}" if link_tag else ""
                results.append({
                    "platform": "twitter",
                    "title": content[:100],
                    "snippet": content[100:200] if len(content) > 100 else "",
                    "url": url
                })
            return results

async def fetch_leads(keyword):
    tasks = [
        fetch_reddit(keyword),
        fetch_duckduckgo(keyword),
       # fetch_twitter(keyword)
    ]
    results = await asyncio.gather(*tasks)
    # Flatten the list
    flat_results = [item for sublist in results for item in sublist]
    return flat_results
