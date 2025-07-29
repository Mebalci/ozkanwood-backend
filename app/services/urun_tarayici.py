from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import json, time
from typing import List, Dict
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def surucu_olustur():
    chrome_driver_path = r"C:\webdrivers\chromedriver-win64\chromedriver.exe"  
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1920x1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36")

    service = Service(executable_path=chrome_driver_path)
    return webdriver.Chrome(service=service, options=options)


def urunleri_tarama(url: str) -> List[Dict]:
    driver = surucu_olustur()
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    urunler = []
    for card in soup.find_all("div", class_="p-card-wrppr"):
        try:
            urun = {
                "marka": card.find("span", class_="prdct-desc-cntnr-ttl").text.strip(),
                "baslik": card.find("span", class_="prdct-desc-cntnr-name").text.strip(),
                "alt_baslik": card.find("div", class_="product-desc-sub-text").text.strip(),
                "fiyat": card.find("div", class_="price-item").text.strip(),
                "resim": card.find("img", class_="p-card-img")["src"]
            }
            urunler.append(urun)
        except:
            continue
    return urunler

def jsona_kaydet(veri: List[Dict]):
    path = Path(__file__).resolve().parent.parent / "models" / "urunler.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)