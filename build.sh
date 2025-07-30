#!/bin/bash
echo "🚀 Gereksinimler yükleniyor..."
pip install -r requirements.txt
python -m playwright install
echo "✅ Build tamamlandı."
