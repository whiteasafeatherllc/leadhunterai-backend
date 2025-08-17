from scrapers.async_scrapers import fetch_twitter, fetch_instagram, fetch_tiktok
import asyncio
import aiohttp

async def _wrapper(func, keyword, max_results=10):
    async with aiohttp.ClientSession() as session:
        return await func(session, keyword, max_results=max_results)

def search_twitter(keyword, max_results=10):
    return asyncio.run(_wrapper(fetch_twitter, keyword, max_results))

def search_instagram(keyword, max_results=10):
    return asyncio.run(_wrapper(fetch_instagram, keyword, max_results))

def search_tiktok(keyword, max_results=10):
    return asyncio.run(_wrapper(fetch_tiktok, keyword, max_results))
