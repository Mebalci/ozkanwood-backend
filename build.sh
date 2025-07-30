#!/bin/bash

echo "🚀 Gereksinimler yükleniyor..."
pip install -r requirements.txt

echo "🎭 Chromium indiriliyor..."
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/ms-playwright
python -m playwright install chromium

echo "✅ Build tamamlandı."
