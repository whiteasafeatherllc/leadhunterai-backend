import asyncio

async def fetch_leads(keyword):
    # Demo async scraping logic (replace with full implementation)
    await asyncio.sleep(0.1)
    return [
        {"platform": "reddit", "title": f"Sample post for {keyword}", "snippet": "Demo snippet", "url": "https://reddit.com/demo"},
        {"platform": "duckduckgo", "title": f"Sample result for {keyword}", "snippet": "Demo snippet", "url": "https://duckduckgo.com/demo"}
    ]
