from fastapi import APIRouter
from services.trendyol import get_all_products
from models.product import Product

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=list[Product])
def get_products():
    products = get_all_products()
    return products
