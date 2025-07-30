#!/bin/bash

echo "📦 Gereksinimler yükleniyor..."
pip install -r requirements.txt

echo "🎭 Playwright tarayıcıları indiriliyor..."
python -c "from playwright.__main__ import main; main(['install', 'chromium'])"

echo "✅ Build tamamlandı."
