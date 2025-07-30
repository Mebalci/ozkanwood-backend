#!/bin/bash
set -e

echo "🔧 Paketler yükleniyor..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🌐 Chromium indiriliyor..."
python -m playwright install chromium

echo "✅ Build tamamlandı."
