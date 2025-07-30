#!/bin/bash
echo "📦 Gereksinimler yükleniyor..."
pip install -r requirements.txt

echo "🎭 Playwright tarayıcıları yükleniyor..."
python -m playwright install --with-deps

echo "✅ Build tamamlandı."
