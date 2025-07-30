#!/bin/bash

echo "📦 Gereksinimler yükleniyor..."
pip install -r requirements.txt

# Playwright tarayıcıları doğru yere indir
export PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/.cache/ms-playwright

echo "🎭 Chromium indiriliyor..."
npx playwright install chromium

echo "✅ Build tamamlandı."
