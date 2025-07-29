from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()

@router.get("/products")
def get_products():
    json_path = Path(__file__).resolve().parent.parent / "models" / "urunler.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []
