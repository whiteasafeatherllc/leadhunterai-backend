from scrapers.async_scrapers import fetch_twitter, fetch_instagram, fetch_tiktok
import aiohttp
import asyncio

def search_twitter(keyword, max_results=10):
    async def wrapper():
        async with aiohttp.ClientSession() as session:
            return await fetch_twitter(session, keyword, max_results)
    return asyncio.run(wrapper())

def search_instagram(keyword, max_results=10):
    async def wrapper():
        async with aiohttp.ClientSession() as session:
            return await fetch_instagram(session, keyword, max_results)
    return asyncio.run(wrapper())

def search_tiktok(keyword, max_results=10):
    async def wrapper():
        async with aiohttp.ClientSession() as session:
            return await fetch_tiktok(session, keyword, max_results)
    return asyncio.run(wrapper())
