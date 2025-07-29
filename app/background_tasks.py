import asyncio
from threading import Thread
from app.services.urun_tarayici import urunleri_tarama, jsona_kaydet

def start_background_updater():
    def background():
        async def loop():
            while True:
                url = "https://www.trendyol.com/sr?mid=254250&os=1"
                print("🔄 Ürünler güncelleniyor...")
                yeni_veri = urunleri_tarama(url)
                jsona_kaydet(yeni_veri)
                await asyncio.sleep(3600)  # 1 saatte bir
        asyncio.run(loop())

    t = Thread(target=background)
    t.daemon = True
    t.start()