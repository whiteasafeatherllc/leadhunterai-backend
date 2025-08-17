from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio

from scrapers.async_scrapers import fetch_twitter, fetch_reddit, fetch_instagram, fetch_tiktok

app = FastAPI(title="LeadHunterAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def run_all_scrapers(keyword: str, platforms: list):
    tasks = []
    results = []

    if "twitter" in platforms:
        tasks.append(fetch_twitter(keyword))
    if "reddit" in platforms:
        tasks.append(fetch_reddit(keyword))
    if "instagram" in platforms:
        tasks.append(fetch_instagram(keyword))
    if "tiktok" in platforms:
        tasks.append(fetch_tiktok(keyword))

    if tasks:
        completed = await asyncio.gather(*tasks)
        for res in completed:
            results.extend(res)

    return results or [{"platform": "None", "text": "No results", "link": ""}]

@app.post("/search")
async def search(keyword: str = Form(...), platforms: str = Form(...)):
    platform_list = [p.strip().lower() for p in platforms.split(",") if p.strip()]
    results = await run_all_scrapers(keyword, platform_list)
    return JSONResponse(content={"results": results})

@app.get("/health")
async def health_check():
    return {"status": "ok"}
