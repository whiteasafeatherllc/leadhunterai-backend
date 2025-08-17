from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

from scrapers.async_scrapers import fetch_leads
from scrapers.twitter_like import search_twitter, search_instagram, search_tiktok

app = FastAPI(title="LeadHunterAI — Social Lead Finder (MVP)", version="0.2.0")

from fastapi.middleware.cors import CORSMiddleware

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve static frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------
# SEARCH API
# ---------------------------
class SearchResponse(BaseModel):
    platform: str
    title: str
    snippet: str
    url: str


@app.get("/search", response_model=List[SearchResponse])
def search(keyword: str, platforms: Optional[str] = "twitter,reddit,instagram,tiktok", max_results: int = 15):
    platforms_list = [p.strip().lower() for p in platforms.split(",") if p.strip()]
    all_results = []

    # Reddit
    if "reddit" in platforms_list:
        try:
            results = fetch_leads(keyword, max_results=max_results)
            for r in results:
                r["platform"] = "reddit"
                all_results.append(r)
        except Exception as e:
            print("Reddit fetch failed:", e)

    # Twitter
    if "twitter" in platforms_list:
        try:
            results = search_twitter(keyword, max_results=max_results)
            for r in results:
                r["platform"] = "twitter"
                all_results.append(r)
        except Exception as e:
            print("Twitter fetch failed:", e)

    # Instagram
    if "instagram" in platforms_list:
        try:
            results = search_instagram(keyword, max_results=max_results)
            for r in results:
                r["platform"] = "instagram"
                all_results.append(r)
        except Exception as e:
            print("Instagram fetch failed:", e)

    # TikTok
    if "tiktok" in platforms_list:
        try:
            results = search_tiktok(keyword, max_results=max_results)
            for r in results:
                r["platform"] = "tiktok"
                all_results.append(r)
        except Exception as e:
            print("TikTok fetch failed:", e)

    # ✅ Deduplicate & trim
    seen = set()
    deduped = []
    for item in all_results:
        url = item.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        deduped.append(item)
        if len(deduped) >= max_results:
            break

    return deduped


# ---------------------------
# MESSAGE GENERATOR
# ---------------------------
class MessageRequest(BaseModel):
    service: str
    prospect_context: Optional[str] = ""
    tone: Optional[str] = "friendly"
    location: Optional[str] = ""


@app.post("/generate_message")
def generate_message(payload: MessageRequest):
    service = payload.service.strip()
    ctx = payload.prospect_context.strip() if payload.prospect_context else ""
    tone = (payload.tone or "friendly").lower()
    location = payload.location.strip()

    openers = {
        "friendly": "Hey there!",
        "professional": "Hi there,",
        "casual": "Yo!",
        "warm": "Hello!",
    }
    opener = openers.get(tone, openers["friendly"])

    line2 = f"I noticed your post about {ctx}." if ctx else "I came across your recent post and thought I'd reach out."
    loc = f" in {location}" if location else ""
    pitch = f"I help folks with {service}{loc} and I have a quick idea that could help you right away."
    cta = "Would you be open to a quick chat this week?"

    message = f"""{opener}

{line2}
{pitch}

If you're interested, I can share a quick plan and examples. {cta}

— {service.title()} Specialist
"""
    return {"message": message}
