from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.tasks.background_updater import background_updater
import asyncio
import json
import os

PRODUCTS_JSON_PATH = "/tmp/products.json"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_updater())

@app.get("/")
def home():
    return {"message": "Trendyol API aktif"}

@app.get("/api/products/")
def get_products():
    try:
        with open(PRODUCTS_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        return {"error": f"Dosya okunamadı: {e}"}
