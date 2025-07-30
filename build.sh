#!/bin/bash
set -e
echo "🚀 Paketler yükleniyor..."
pip install --upgrade pip
pip install --use-feature=2020-resolver -r requirements.txt

echo "🎭 Chromium indiriliyor..."
python -m playwright install chromium
echo "✅ Build tamamlandı."
