import aiohttp
from bs4 import BeautifulSoup

# Common headers to look like a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


# Expand keyword into multiple useful search phrases
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
# Twitter (via Nitter mirror)
# --------------------------
async def fetch_twitter(keyword: str):
    queries = expand_queries(keyword)
    results = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for q in queries:
            url = f"https://nitter.net/search?f=tweets&q={q}"
            try:
                async with session.get(url, timeout=10) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    tweets = soup.select(".timeline-item .tweet-content")
                    for t in tweets[:5]:
                        results.append({
                            "platform": "Twitter",
                            "text": t.get_text(strip=True),
                            "link": "https://nitter.net" + t.find_parent("a")["href"]
                        })
            except Exception as e:
                results.append({"platform": "Twitter", "text": f"Error: {e}", "link": ""})

    return results or [{"platform": "Twitter", "text": "No results", "link": ""}]


# --------------------------
# Reddit
# --------------------------
async def fetch_reddit(keyword: str):
    queries = expand_queries(keyword)
    results = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for q in queries:
            url = f"https://www.reddit.com/search/?q={q}"
            try:
                async with session.get(url, timeout=10) as resp:
                    html = await resp.text()
                    soup = BeautifulSoup(html, "html.parser")
                    posts = soup.select("h3")
                    for p in posts[:5]:
                        results.append({
                            "platform": "Reddit",
                            "text": p.get_text(strip=True),
                            "link": url
                        })
            except Exception as e:
                results.append({"platform": "Reddit", "text": f"Error: {e}", "link": ""})

    return results or [{"platform": "Reddit", "text": "No results", "link": ""}]


# --------------------------
# Instagram (via DuckDuckGo proxy search)
# --------------------------
async def fetch_instagram(keyword: str):
    queries = expand_queries(keyword)
    results = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for q in queries:
            url = f"https://duckduckgo.com/html/?q=site:instagram.com {q}"
            try:
                async with session.get(url, timeout=10) as resp:
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
# TikTok (via DuckDuckGo proxy search)
# --------------------------
async def fetch_tiktok(keyword: str):
    queries = expand_queries(keyword)
    results = []

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for q in queries:
            url = f"https://duckduckgo.com/html/?q=site:tiktok.com {q}"
            try:
                async with session.get(url, timeout=10) as resp:
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
