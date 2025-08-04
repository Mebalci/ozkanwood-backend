from pydantic import BaseModel, Field
from typing import List, Optional

class ProductImage(BaseModel):
    url: str

class ProductAttribute(BaseModel):
    attributeId: int
    attributeName: str
    attributeValue: str
    attributeValueId: Optional[int] = None

class Product(BaseModel):
    id: str
    productMainId: str
    productContentId: int
    productCode: int
    barcode: str
    stockCode: str
    stockUnitType: str
    brand: str
    brandId: int
    categoryName: str
    title: str
    description: str
    listPrice: float
    salePrice: float
    quantity: int
    onSale: bool
    approved: bool
    archived: bool
    blacklisted: bool
    vatRate: float
    stockUnitType: str
    attributes: List[ProductAttribute]
    images: List[ProductImage]
    productUrl: str
