import asyncio
from app.services.trendyol import get_all_products, kaydet_urunler

async def background_updater():
    while True:
        try:
            print("🔄 Ürün verileri Trendyol'dan güncelleniyor...")
            products = await get_all_products()
            kaydet_urunler(products)
            print(f"✅ {len(products)} ürün güncellendi ve dosyaya yazıldı.")
        except Exception as e:
            print(f"⚠️ Güncelleme hatası: {e}")
        await asyncio.sleep(3600)  # 1 saatte bir güncelle
