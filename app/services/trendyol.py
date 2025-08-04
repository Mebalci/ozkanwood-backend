import os
from app.config import API_KEY, API_SECRET, SUPPLIER_ID
from app.models.product import Product
import base64
import json
from datetime import datetime
import httpx
import gzip

IS_RENDER = os.getenv("RENDER", "false").lower() == "true"
PRODUCTS_JSON_PATH = "/tmp/products.json"

def kaydet_urunler(products):
    os.makedirs("/tmp", exist_ok=True)
    with gzip.open(PRODUCTS_JSON_PATH + ".gz", "wt", encoding="utf-8") as f:
        json.dump({"updated_at": datetime.now().isoformat(), "products": products}, f, ensure_ascii=False, indent=2)


def generate_headers():
    credentials = f"{API_KEY}:{API_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

async def get_all_products():
    base_url = f"https://api.trendyol.com/integration/product/sellers/{SUPPLIER_ID}/products"
    page = 0
    size = 100
    all_products = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            params = {
                "approved": "true",
                "page": page,
                "size": size,
                "supplierId": SUPPLIER_ID
            }

            response = await client.get(base_url, headers=generate_headers(), params=params)
            response.raise_for_status()
            data = response.json()

            for item in data.get("content", []):
                simplified = {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "brand": item.get("brand"),
                    "description": item.get("description"),
                    "price": item.get("listPrice"),
                    "salePrice": item.get("salePrice"),
                    "quantity": item.get("quantity"),
                    "vatRate": item.get("vatRate"),
                    "images": [img["url"] for img in item.get("images", [])],
                    "attributes": [
                        {
                            "name": attr.get("attributeName"),
                            "value": attr.get("attributeValue")
                        }
                        for attr in item.get("attributes", []) if attr.get("attributeValue")
                    ],
                    "stockCode": item.get("stockCode"),
                    "barcode": item.get("barcode"),
                    "category": item.get("categoryName"),
                    "url": item.get("productUrl")
                }
                all_products.append(simplified)

            if page + 1 >= data.get("totalPages", 1):
                break
            page += 1

    return all_products
