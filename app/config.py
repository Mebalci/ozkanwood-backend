# backend/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TRENDYOL_API_KEY")
API_SECRET = os.getenv("TRENDYOL_API_SECRET")
SUPPLIER_ID = os.getenv("TRENDYOL_SUPPLIER_ID")
