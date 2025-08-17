from typing import List
from scrapers.async_scrapers import fetch_twitter, fetch_instagram, fetch_tiktok
import asyncio

def search_twitter(keyword: str, max_results: int = 10) -> List[dict]:
    async def wrapper():
        import aiohttp
        async with aiohttp.ClientSession() as session:
            return await fetch_twitter(session, keyword, max_results=max_results)
    return asyncio.run(wrapper())

def search_instagram(keyword: str, max_results: int = 10) -> List[dict]:
    async def wrapper():
        import aiohttp
        async with aiohttp.ClientSession() as session:
            return await fetch_instagram(session, keyword, max_results=max_results)
    return asyncio.run(wrapper())

def search_tiktok(keyword: str, max_results: int = 10) -> List[dict]:
    async def wrapper():
        import aiohttp
        async with aiohttp.ClientSession() as session:
            return await fetch_tiktok(session, keyword, max_results=max_results)
    return asyncio.run(wrapper())
