from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from async_scrapers import fetch_twitter, fetch_reddit, fetch_instagram, fetch_tiktok
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(keyword: str = Query(...), platforms: str = Query("twitter,reddit,instagram,tiktok")):
    tasks = []
    platform_list = [p.strip().lower() for p in platforms.split(",")]

    if "twitter" in platform_list:
        tasks.append(fetch_twitter(keyword))
    if "reddit" in platform_list:
        tasks.append(fetch_reddit(keyword))
    if "instagram" in platform_list:
        tasks.append(fetch_instagram(keyword))
    if "tiktok" in platform_list:
        tasks.append(fetch_tiktok(keyword))

    results = await asyncio.gather(*tasks)
    flat_results = [item for sublist in results for item in sublist]
    return flat_results
