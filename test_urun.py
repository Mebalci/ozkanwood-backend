# test_urun.py
from app.services.urun_tarayici import urunleri_tarama

url = "https://www.trendyol.com/sr?mid=254250&os=1"
veri = urunleri_tarama(url)
print(f"{len(veri)} ürün bulundu")
