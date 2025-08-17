import aiohttp
from bs4 import BeautifulSoup
import asyncio
import snscrape.modules.twitter as sntwitter

# --------------------------
# Common headers
# --------------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# --------------------------
# Expand keyword queries
# --------------------------
def expand_queries(keyword: str):
    base = keyword.strip()
    return [
        base,
        f"looking for a {base}",
        f"need a {base}",
        f"recommend a {base}",
        f"who can do {base}",
        f"help me with {base}",
    ]

# --------------------------
# Twitter (via snscrape)
# --------------------------
async def fetch_twitter(keyword: str):
    queries = expand_queries(keyword)
    results = []

    for q in queries:
        try:
            # Grab up to 5 tweets per query
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(q).get_items()):
                if i >= 5:
                    break
                results.append({
                    "platform": "Twitter",
                    "text": tweet.content,
                    "link": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
                })
        except Exception as e:
            results.append({"platform": "Twitter", "text": f"Error: {e}", "link": ""})

    return results or [{"platform": "Twitter", "text": "No results", "link": ""}]

# --------------------------
# Reddit (JSON API scraping)
# --------------------------
async def fetch_reddit(keyword: str):
    queries = expand_queries(keyword)
    results = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for q in queries:
            url = f"https://www.reddit.com/search.json?q={q}&limit=5"
            try:
                async with session.get(url) as resp:
                    data = await resp.json()
                    posts = data.get("data", {}).get("children", [])
                    for p in posts:
                        post = p.get("data", {})
                        results.append({
                            "platform": "Reddit",
                            "text": post.get("title", ""),
                            "link": f"https://reddit.com{post.get('permalink', '')}"
                        })
            except Exception as e:
                results.append({"platform": "Reddit", "text": f"Error: {e}", "link": ""})

    return results or [{"platform": "Reddit", "text": "No results", "link": ""}]

# --------------------------
# Instagram (DuckDuckGo proxy)
# --------------------------
async def fetch_instagram(keyword: str):
    queries = expand_queries(keyword)
    results = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for q in queries:
            url = f"https://duckduckgo.com/html/?q=site:instagram.com {q}"
            try:
                async with session.get(url) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    links = soup.select("a.result__a")
                    for l in links[:5]:
                        results.append({
                            "platform": "Instagram",
                            "text": l.get_text(strip=True),
                            "link": l["href"]
                        })
            except Exception as e:
                results.append({"platform": "Instagram", "text": f"Error: {e}", "link": ""})

    return results or [{"platform": "Instagram", "text": "No results", "link": ""}]

# --------------------------
# TikTok (DuckDuckGo proxy)
# --------------------------
async def fetch_tiktok(keyword: str):
    queries = expand_queries(keyword)
    results = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for q in queries:
            url = f"https://duckduckgo.com/html/?q=site:tiktok.com {q}"
            try:
                async with session.get(url) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    links = soup.select("a.result__a")
                    for l in links[:5]:
                        results.append({
                            "platform": "TikTok",
                            "text": l.get_text(strip=True),
                            "link": l["href"]
                        })
            except Exception as e:
                results.append({"platform": "TikTok", "text": f"Error: {e}", "link": ""})

    return results or [{"platform": "TikTok", "text": "No results", "link": ""}]

# --------------------------
# Run all in parallel
# --------------------------
async def search_all(keyword: str):
    tasks = [
        fetch_twitter(keyword),
        fetch_reddit(keyword),
        fetch_instagram(keyword),
        fetch_tiktok(keyword)
    ]
    results = await asyncio.gather(*tasks)
    # Flatten list of lists
    flat_results = [item for sublist in results for item in sublist]
    return flat_results
