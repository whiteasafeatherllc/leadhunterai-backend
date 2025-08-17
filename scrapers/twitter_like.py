from scrapers.async_scrapers import fetch_twitter, fetch_instagram, fetch_tiktok
import asyncio

async def _gather(func, keyword, max_results=10):
    return await func(keyword=keyword, max_results=max_results)

def search_twitter(keyword, max_results=10):
    return asyncio.run(fetch_twitter_wrapper(keyword, max_results))

def search_instagram(keyword, max_results=10):
    return asyncio.run(fetch_instagram_wrapper(keyword, max_results))

def search_tiktok(keyword, max_results=10):
    return asyncio.run(fetch_tiktok_wrapper(keyword, max_results))

async def fetch_twitter_wrapper(keyword, max_results=10):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        return await fetch_twitter(session, keyword, max_results=max_results)

async def fetch_instagram_wrapper(keyword, max_results=10):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        return await fetch_instagram(session, keyword, max_results=max_results)

async def fetch_tiktok_wrapper(keyword, max_results=10):
    import aiohttp
    async with aiohttp.ClientSession() as session:
        return await fetch_tiktok(session, keyword, max_results=max_results)
