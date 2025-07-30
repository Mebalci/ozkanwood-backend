#!/bin/bash
set -e
echo "🔧 Paketler kuruluyor..."
pip install --upgrade pip
pip install --use-feature=2020-resolver -r requirements.txt

echo "🎭 Chromium indiriliyor..."
# PLAYWRIGHT_BROWSERS_PATH zaten env var ile tanımlı
python -m playwright install chromium

echo "✅ Build tamamlandı."
