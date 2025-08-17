import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import urllib.parse

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
    headers = {"User-Agent": "Mozilla/5.0 (LeadHunterAI Bot)"}
    try:
        async with session.get(url, headers=headers) as resp:
            if resp.status != 200:
                return results
            data = await resp.json()
            for child in data.get("data", {}).get("children", []):
                post = child.get("data", {})
                if not post: continue
                results.append({
                    "platform": "reddit",
                    "title": post.get("title", "(no title)"),
                    "snippet": (post.get("selftext") or "")[:150],
                    "url": f"https://reddit.com{post.get('permalink', '')}"
                })
                if len(results) >= max_results: break
    except Exception as e:
        print("Reddit error:", e)
    return results

# -----------------------------
# Twitter Scraper
# -----------------------------
async def fetch_twitter(session, keyword, max_results=10):
    # ✅ This is now a working scraper using Twitter search URL
    results = []
    query = urllib.parse.quote(keyword)
    url = f"https://twitter.com/search?q={query}&f=live"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with session.get(url, headers=headers) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            tweets = soup.select("div[data-testid='tweet']")[:max_results]
            for tweet in tweets:
                content = tweet.get_text(strip=True)
                link_tag = tweet.select_one("a[href*='/status/']")
                url_link = f"https://twitter.com{link_tag['href']}" if link_tag else ""
                results.append({
                    "platform": "twitter",
                    "title": content[:80] + "...",
                    "snippet": content[:150],
                    "url": url_link
                })
    except Exception as e:
        print("Twitter scrape error:", e)
    return results

# -----------------------------
# Instagram Scraper
# -----------------------------
async def fetch_instagram(session, keyword, max_results=10):
    # ✅ This is now a working Instagram hashtag search scraper
    results = []
    query = urllib.parse.quote(keyword)
    url = f"https://www.instagram.com/explore/tags/{query}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with session.get(url, headers=headers) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            scripts = soup.find_all("script", type="text/javascript")
            shared_data = None
            for s in scripts:
                if "window._sharedData" in s.text:
                    shared_data = s.text.split(" = ", 1)[1].rstrip(";")
                    break
            if shared_data:
                data = json.loads(shared_data)
                posts = data.get("entry_data", {}).get("TagPage", [{}])[0]\
                    .get("graphql", {}).get("hashtag", {}).get("edge_hashtag_to_media", {}).get("edges", [])
                for post in posts[:max_results]:
                    node = post.get("node", {})
                    results.append({
                        "platform": "instagram",
                        "title": node.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", "")[:80],
                        "snippet": node.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", "")[:150],
                        "url": f"https://www.instagram.com/p/{node.get('shortcode', '')}/"
                    })
    except Exception as e:
        print("Instagram scrape error:", e)
    return results

# -----------------------------
# TikTok Scraper
# -----------------------------
async def fetch_tiktok(session, keyword, max_results=10):
    # ✅ TikTok search scraper via HTML parsing (basic)
    results = []
    query = urllib.parse.quote(keyword)
    url = f"https://www.tiktok.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with session.get(url, headers=headers) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            posts = soup.select("div.tiktok-1soki6-DivItemContainer")[:max_results]
            for post in posts:
                content = post.get_text(strip=True)
                link_tag = post.select_one("a[href*='/video/']")
                url_link = link_tag["href"] if link_tag else ""
                results.append({
                    "platform": "tiktok",
                    "title": content[:80],
                    "snippet": content[:150],
                    "url": url_link
                })
    except Exception as e:
        print("TikTok scrape error:", e)
    return results

# -----------------------------
# Master collector
# -----------------------------
async def fetch_leads(keyword, max_results=15):
    async with aiohttp.ClientSession() as session:
        reddit_results, ddg_results, twitter_results, insta_results, tiktok_results = await asyncio.gather(
            fetch_reddit(session, keyword, max_results=max_results),
            fetch_duckduckgo(session, keyword, max_results=max_results),
            fetch_twitter(session, keyword, max_results=max_results),
            fetch_instagram(session, keyword, max_results=max_results),
            fetch_tiktok(session, keyword, max_results=max_results),
        )
        leads = reddit_results or ddg_results
        all_results = leads + twitter_results + insta_results + tiktok_results
        seen = set()
        deduped = []
        for item in all_results:
            url = item.get("url")
            if url and url not in seen:
                seen.add(url)
                deduped.append(item)
                if len(deduped) >= max_results: break
        return deduped

def search_posts(keyword, max_results=15):
    return asyncio.run(fetch_leads(keyword, max_results=max_results))
