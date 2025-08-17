from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrapers.async_scrapers import fetch_leads

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(keyword: str):
    results = await fetch_leads(keyword)
    return results
