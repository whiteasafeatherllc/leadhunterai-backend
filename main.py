from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from scrapers.async_scrapers import fetch_leads

app = FastAPI()

# Allow your frontend domain
origins = [
    "http://leadhunterapp.superlativeorganics.shop",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(keyword: str):
    if not keyword:
        raise HTTPException(status_code=400, detail="Keyword is required")
    results = await fetch_leads(keyword)
    return results
