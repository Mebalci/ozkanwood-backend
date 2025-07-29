import asyncio
from playwright.async_api import async_playwright
import json
from typing import List, Dict
from pathlib import Path

async def urunleri_tarama_playwright(url: str) -> List[Dict]:
    """Playwright ile Trendyol scraping - Güncellenmiş API"""
    urunler = []
    
    async with async_playwright() as p:
        # Chromium browser başlat (headless mode)
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-web-security'
            ]
        )
        
        # Context oluştur (user agent burada ayarlanır)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        page = await context.new_page()
        
        try:
            print(f"📡 Sayfa yükleniyor: {url}")
            # Sayfayı yükle
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Sayfanın yüklenmesini bekle
            await page.wait_for_timeout(3000)
            
            # Ürün kartlarını bekle (birden fazla selector dene)
            selectors = [".p-card-wrppr", "[data-testid='product-card']", ".product-item"]
            cards = []
            
            for selector in selectors:
                try:
                    await page.wait_for_selector(selector, timeout=10000)
                    cards = await page.query_selector_all(selector)
                    if cards:
                        print(f"✅ {len(cards)} ürün kartı bulundu ({selector})")
                        break
                except:
                    continue
            
            if not cards:
                print("⚠️ Ürün kartı bulunamadı, sayfa içeriğini kontrol ediliyor...")
                content = await page.content()
                print(f"Sayfa boyutu: {len(content)} karakter")
                # HTML'nin bir kısmını logla
                if "trendyol" in content.lower():
                    print("✅ Trendyol sayfası yüklendi")
                else:
                    print("❌ Sayfa düzgün yüklenmemiş olabilir")
                return urunler
            
            # Ürün kartlarını işle
            for i, card in enumerate(cards):
                try:
                    # Farklı selector'ları dene
                    marka_selectors = [".prdct-desc-cntnr-ttl", ".product-brand", "[data-testid='brand']"]
                    marka = ""
                    for sel in marka_selectors:
                        marka_element = await card.query_selector(sel)
                        if marka_element:
                            marka = await marka_element.inner_text()
                            break
                    
                    # Başlık
                    baslik_selectors = [".prdct-desc-cntnr-name", ".product-title", "[data-testid='title']"]
                    baslik = ""
                    for sel in baslik_selectors:
                        baslik_element = await card.query_selector(sel)
                        if baslik_element:
                            baslik = await baslik_element.inner_text()
                            break
                    
                    # Alt başlık
                    alt_baslik_element = await card.query_selector(".product-desc-sub-text")
                    alt_baslik = await alt_baslik_element.inner_text() if alt_baslik_element else ""
                    
                    # Fiyat
                    fiyat_selectors = [".prc-box-dscntd", ".price-item", ".product-price", "[data-testid='price']"]
                    fiyat = ""
                    for sel in fiyat_selectors:
                        fiyat_element = await card.query_selector(sel)
                        if fiyat_element:
                            fiyat = await fiyat_element.inner_text()
                            break
                    
                    # Resim
                    img_selectors = [".p-card-img", ".product-image", "img"]
                    resim = ""
                    for sel in img_selectors:
                        img_element = await card.query_selector(sel)
                        if img_element:
                            resim = await img_element.get_attribute("src")
                            if resim:
                                if not resim.startswith("http"):
                                    resim = f"https:{resim}"
                                break
                    
                    # Veri kontrolü ve kayıt
                    if marka.strip() or baslik.strip():  # En azından biri olsun
                        urun = {
                            "marka": marka.strip(),
                            "baslik": baslik.strip(),
                            "alt_baslik": alt_baslik.strip(),
                            "fiyat": fiyat.strip(),
                            "resim": resim
                        }
                        urunler.append(urun)
                        
                        # İlk 3 ürünü logla
                        if i < 3:
                            print(f"Ürün {i+1}: {marka} - {baslik} - {fiyat}")
                        
                except Exception as e:
                    print(f"Ürün {i+1} işlenirken hata: {e}")
                    continue
                    
        except Exception as e:
            print(f"❌ Sayfa yüklenirken hata: {e}")
            
        finally:
            await browser.close()
    
    print(f"🎉 Toplam {len(urunler)} ürün başarıyla işlendi")
    return urunler

def jsona_kaydet(veri: List[Dict]):
    """Verileri JSON dosyasına kaydet"""
    path = Path(__file__).resolve().parent.parent / "models" / "urunler.json"
    path.parent.mkdir(exist_ok=True)  # models klasörünü oluştur
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(veri)} ürün kaydedildi")