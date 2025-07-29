import asyncio
from threading import Thread
from app.services.urun_tarayici import urunleri_tarama_playwright, jsona_kaydet
import platform

def start_background_updater():
    """Background task başlatıcı"""
    
    def background_sync():
        """Senkron wrapper fonksiyon"""
        async def background_async():
            """Asenkron background işlemi"""
            while True:
                print("🔄 Ürünler güncelleniyor...")
                try:
                    url = "https://www.trendyol.com/sr?mid=254250&os=1"
                    veri = await urunleri_tarama_playwright(url)
                    
                    if veri:
                        jsona_kaydet(veri)
                        print(f"✅ {len(veri)} ürün başarıyla güncellendi")
                    else:
                        print("⚠️ Hiç ürün bulunamadı")
                        
                except Exception as e:
                    print(f"❌ Güncelleme hatası: {e}")
                
                # Her 1 saatte bir güncelle (3600 saniye)
                await asyncio.sleep(3600)
        
        # Windows için event loop policy ayarla
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        # Yeni event loop oluştur ve çalıştır
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(background_async())
        except KeyboardInterrupt:
            print("🛑 Background task durduruldu")
        finally:
            loop.close()
    
    # Thread başlat
    thread = Thread(target=background_sync, daemon=True)
    thread.start()
    print("🚀 Background updater başlatıldı")

# Alternatif: Daha basit yaklaşım
def start_simple_updater():
    """Basit background updater (sadece startup'ta çalışır)"""
    
    async def tek_guncelleme():
        """Tek seferlik güncelleme"""
        print("🔄 İlk ürün güncellemesi başlıyor...")
        try:
            url = "https://www.trendyol.com/sr?mid=254250&os=1"
            veri = await urunleri_tarama_playwright(url)
            
            if veri:
                jsona_kaydet(veri)
                print(f"✅ {len(veri)} ürün başarıyla yüklendi")
            else:
                print("⚠️ Hiç ürün bulunamadı")
                
        except Exception as e:
            print(f"❌ İlk yükleme hatası: {e}")
    
    def sync_wrapper():
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(tek_guncelleme())
        finally:
            loop.close()
    
    thread = Thread(target=sync_wrapper, daemon=True)
    thread.start()