from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from scrapers.async_scrapers import fetch_leads

app = FastAPI()

# -----------------------------
# Enable CORS (needed for frontend)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Search Endpoint
# -----------------------------
@app.get("/search")
async def search(keyword: str):
    results = await fetch_leads(keyword)
    return results

# -----------------------------
# Message Generator Endpoint
# -----------------------------
@app.get("/generate_message")
async def generate_message(name: str = "there", service: str = "your services"):
    return {
        "message": f"Hi {name}, I saw you might be interested in {service}. "
                   f"I’d love to connect and see how I can help you!"
    }

# 👉 keep all your other routes untouched (they will still work)
