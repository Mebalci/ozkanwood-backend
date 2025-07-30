#!/bin/bash

echo "📦 Gereksinimler yükleniyor..."
pip install -r requirements.txt

# Ortam değişkeni doğru set edilmeli
export PLAYWRIGHT_BROWSERS_PATH=/usr/local/share/.cache/ms-playwright

# Doğrudan Python komutuyla chromium indir (npx gerekmez!)
echo "🎭 Chromium indiriliyor (Python içinden)..."
python -c "import subprocess; subprocess.run(['playwright', 'install', 'chromium'])"

echo "✅ Build tamamlandı."
