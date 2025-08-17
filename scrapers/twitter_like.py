import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

async def fetch_html(url, timeout=20):
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=timeout) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text

# -----------------------------
# Twitter Search
# -----------------------------
async def search_twitter(keyword: str, max_results: int = 15):
    url = f"https://twitter.com/search?q={keyword}&f=live"
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    results = []
    tweets = soup.select("article")[:max_results]
    for tweet in tweets:
        text_tag = tweet.find("div", attrs={"data-testid": "tweetText"})
        link_tag = tweet.find("a", href=True)
        if text_tag and link_tag:
            results.append({
                "title": text_tag.get_text(strip=True),
                "snippet": "",
                "url": f"https://twitter.com{link_tag['href']}"
            })
    return results

# -----------------------------
# Instagram Search
# -----------------------------
async def search_instagram(keyword: str, max_results: int = 15):
    url = f"https://www.instagram.com/explore/tags/{keyword}/"
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    results = []
    posts = soup.select("a[href*='/p/']")[:max_results]
    for post in posts:
        results.append({
            "title": "Instagram Post",
            "snippet": "",
            "url": f"https://www.instagram.com{post['href']}"
        })
    return results

# -----------------------------
# TikTok Search
# -----------------------------
async def search_tiktok(keyword: str, max_results: int = 15):
    url = f"https://www.tiktok.com/tag/{keyword}"
    html = await fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    results = []
    posts = soup.select("a[href*='/video/']")[:max_results]
    for post in posts:
        results.append({
            "title": "TikTok Video",
            "snippet": "",
            "url": f"https://www.tiktok.com{post['href']}"
        })
    return results
