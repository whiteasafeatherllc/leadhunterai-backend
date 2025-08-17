from fastapi import APIRouter, Query
import asyncio

from async_scrapers import (
    fetch_twitter,
    fetch_reddit,
    fetch_instagram,
    fetch_tiktok,
)

router = APIRouter()


@router.get("/search")
async def search(
    q: str = Query(..., description="Search keyword"),
    platforms: str = Query("twitter,reddit,instagram,tiktok", description="Comma separated list of platforms")
):
    """
    Search across multiple platforms in parallel.
    """
    platform_list = [p.strip().lower() for p in platforms.split(",") if p.strip()]
    tasks = []

    if "twitter" in platform_list:
        tasks.append(fetch_twitter(q))
    if "reddit" in platform_list:
        tasks.append(fetch_reddit(q))
    if "instagram" in platform_list:
        tasks.append(fetch_instagram(q))
    if "tiktok" in platform_list:
        tasks.append(fetch_tiktok(q))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Flatten + handle errors
    combined = []
    for res in results:
        if isinstance(res, Exception):
            combined.append({"platform": "Error", "text": str(res), "link": ""})
        else:
            combined.extend(res)

    return {"results": combined}
