#!/bin/bash

echo "📦 requirements.txt yükleniyor..."
pip install -r requirements.txt

echo "🔧 PLAYWRIGHT_BROWSERS_PATH set ediliyor..."
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/ms-playwright

echo "🎭 Playwright chromium indiriliyor..."
python -m playwright install chromium

echo "✅ Build tamamlandı."
