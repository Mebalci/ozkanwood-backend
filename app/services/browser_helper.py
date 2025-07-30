import os
import logging
import subprocess
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright

logger = logging.getLogger(__name__)

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        
    def ensure_browser_installed(self):
        """Tarayıcının kurulu olduğundan emin ol"""
        try:
            # Önce mevcut kurulumu kontrol et
            with sync_playwright() as p:
                browser_path = p.chromium.executable_path
                if os.path.exists(browser_path):
                    logger.info(f"✅ Browser mevcut: {browser_path}")
                    return True
                else:
                    logger.warning(f"❌ Browser bulunamadı: {browser_path}")
        except Exception as e:
            logger.error(f"Browser kontrol hatası: {e}")
            
        # Kurulum dene
        try:
            logger.info("🎭 Playwright tarayıcısı kuruluyor...")
            from playwright.__main__ import main
            main(['install', 'chromium'])
            logger.info("✅ Browser kurulumu tamamlandı")
            return True
        except Exception as e:
            logger.error(f"Browser kurulum hatası: {e}")
            return False
    
    def get_browser_launch_options(self):
        """Render ortamına uygun browser seçenekleri"""
        return {
            'headless': True,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--no-first-run',
                '--no-zygote',
                '--single-process',
                '--disable-extensions',
                '--disable-default-apps',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--memory-pressure-off'
            ]
        }
    
    def start_browser(self):
        """Browser'ı güvenli şekilde başlat"""
        try:
            if not self.ensure_browser_installed():
                raise Exception("Browser kurulumu başarısız")
                
            self.playwright = sync_playwright().start()
            launch_options = self.get_browser_launch_options()
            
            # Sistem Chromium'u varsa onu kullanmayı dene
            system_chrome_paths = [
                '/usr/bin/chromium-browser',
                '/usr/bin/google-chrome',
                '/usr/bin/chromium'
            ]
            
            for chrome_path in system_chrome_paths:
                if os.path.exists(chrome_path):
                    logger.info(f"🔧 Sistem Chromium kullanılıyor: {chrome_path}")
                    launch_options['executable_path'] = chrome_path
                    break
            
            self.browser = self.playwright.chromium.launch(**launch_options)
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            )
            
            logger.info("✅ Browser başarıyla başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"❌ Browser başlatma hatası: {e}")
            self.cleanup()
            return False
    
    def get_page(self):
        """Yeni sayfa oluştur"""
        if not self.context:
            if not self.start_browser():
                raise Exception("Browser başlatılamadı")
        return self.context.new_page()
    
    def cleanup(self):
        """Kaynakları temizle"""
        try:
            if self.context:
                self.context.close()
                self.context = None
            if self.browser:
                self.browser.close()
                self.browser = None
            if self.playwright:
                self.playwright.stop()
                self.playwright = None
            logger.info("🧹 Browser kaynakları temizlendi")
        except Exception as e:
            logger.error(f"Browser temizleme hatası: {e}")

# Global browser manager instance
browser_manager = BrowserManager()

def get_browser_page():
    """Global browser manager'dan sayfa al"""
    return browser_manager.get_page()

def cleanup_browser():
    """Global browser manager'ı temizle"""
    browser_manager.cleanup()
