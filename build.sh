#!/bin/bash

echo "🚀 Build başlıyor..."

# Python bağımlılıklarını yükle
echo "📦 Python paketleri yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

# Sistem seviyesinde Chromium kurulumu dene
echo "🔧 Sistem Chromium kurulumu kontrol ediliyor..."
if command -v chromium-browser &> /dev/null; then
    echo "✅ Sistem Chromium mevcut"
else
    echo "⚠️ Sistem Chromium bulunamadı"
fi

# Playwright ortam değişkenlerini ayarla
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/ms-playwright
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0

echo "🎭 Playwright tarayıcı kurulumu..."
echo "Browser path: $PLAYWRIGHT_BROWSERS_PATH"

# Playwright kurulum dizinini oluştur
mkdir -p /opt/render/.cache/ms-playwright

# Birden fazla yöntemle dene
echo "📥 Yöntem 1: Python modülü ile kurulum..."
python -c "
import subprocess
import sys
try:
    from playwright.sync_api import Playwright
    from playwright import __main__ as playwright_main
    playwright_main.main(['install', 'chromium'])
    print('✅ Playwright modülü ile kurulum başarılı')
except Exception as e:
    print(f'❌ Playwright modülü hatası: {e}')
    sys.exit(1)
"

# Kurulumu doğrula
echo "🔍 Kurulum doğrulanıyor..."
python -c "
import os
from playwright.sync_api import sync_playwright

try:
    with sync_playwright() as p:
        browser_path = p.chromium.executable_path
        print(f'Browser executable path: {browser_path}')
        if os.path.exists(browser_path):
            print('✅ Chromium executable mevcut')
        else:
            print('❌ Chromium executable bulunamadı')
            # Alternatif path'leri kontrol et
            possible_paths = [
                '/opt/render/.cache/ms-playwright/chromium-*/chrome-linux/chrome',
                '/opt/render/.cache/ms-playwright/chromium-*/chrome-linux/headless_shell',
                '/usr/bin/chromium-browser',
                '/usr/bin/google-chrome',
                '/usr/bin/chromium'
            ]
            import glob
            for pattern in possible_paths:
                matches = glob.glob(pattern)
                if matches:
                    print(f'Alternatif bulundu: {matches[0]}')
                    break
except Exception as e:
    print(f'Doğrulama hatası: {e}')
"

echo "✅ Build tamamlandı!"
