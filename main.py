from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aiohttp
import asyncio
from bs4 import BeautifulSoup

app = FastAPI()

# ✅ Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["https://leadhunterapp.superlativeorganics.shop"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Scraper Functions
# ------------------------

async def fetch_reddit(session, keyword: str):
    url = f"https://www.reddit.com/search/?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    async with session.get(url, headers=headers) as resp:
        text = await resp.text()
        soup = BeautifulSoup(text, "html.parser")
        for post in soup.select("a[href*='/r/']"):
            title = post.get_text(strip=True)
            link = "https://reddit.com" + post.get("href", "")
            if title and link:
                results.append({
                    "platform": "reddit",
                    "title": title,
                    "url": link
                })
    return results[:10]  # limit results


async def fetch_duckduckgo(session, keyword: str):
    url = f"https://duckduckgo.com/html/?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    async with session.get(url, headers=headers) as resp:
        text = await resp.text()
        soup = BeautifulSoup(text, "html.parser")
        for res in soup.select(".result__title a"):
            title = res.get_text(strip=True)
            link = res.get("href")
            if title and link:
                results.append({
                    "platform": "duckduckgo",
                    "title": title,
                    "url": link
                })
    return results[:10]


async def fetch_leads(keyword: str):
    async with aiohttp.ClientSession() as session:
        reddit = await fetch_reddit(session, keyword)
        ddg = await fetch_duckduckgo(session, keyword)
        return reddit + ddg


# ------------------------
# API Endpoint
# ------------------------

@app.get("/search")
async def search(keyword: str):
    try:
        results = await fetch_leads(keyword)
        return results if results else [{"message": "No results found"}]
    except Exception as e:
        return {"error": str(e)}
