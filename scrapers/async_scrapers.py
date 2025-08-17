import aiohttp
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

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
                        link_tag = t.find_parent("a")
                        link = "https://nitter.net" + link_tag["href"] if link_tag else ""
                        results.append({
                            "platform": "Twitter",
                            "title": t.get_text(strip=True),
                            "url": link,
                            "snippet": t.get_text(strip=True)
                        })
            except Exception as e:
                results.append({"platform": "Twitter", "title": f"Error: {e}", "url": "", "snippet": ""})
    return results or [{"platform": "Twitter", "title": "No results", "url": "", "snippet": ""}]

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
                            "title": p.get_text(strip=True),
                            "url": url,
                            "snippet": p.get_text(strip=True)
                        })
            except Exception as e:
                results.append({"platform": "Reddit", "title": f"Error: {e}", "url": "", "snippet": ""})
    return results or [{"platform": "Reddit", "title": "No results", "url": "", "snippet": ""}]

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
                            "title": l.get_text(strip=True),
                            "url": l["href"],
                            "snippet": l.get_text(strip=True)
                        })
            except Exception as e:
                results.append({"platform": "Instagram", "title": f"Error: {e}", "url": "", "snippet": ""})
    return results or [{"platform": "Instagram", "title": "No results", "url": "", "snippet": ""}]

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
                            "title": l.get_text(strip=True),
                            "url": l["href"],
                            "snippet": l.get_text(strip=True)
                        })
            except Exception as e:
                results.append({"platform": "TikTok", "title": f"Error: {e}", "url": "", "snippet": ""})
    return results or [{"platform": "TikTok", "title": "No results", "url": "", "snippet": ""}]
