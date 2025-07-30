#!/bin/bash

echo "🚀 Gereksinimler yükleniyor..."
pip install -r requirements.txt

echo "🎭 Playwright tarayıcıları indiriliyor..."
python -m playwright install chromium

echo "✅ Build tamamlandı."
