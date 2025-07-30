FROM python:3.12-slim

# Sistem bağımlılıkları (Chromium için)
RUN apt-get update && apt-get install -y \
  libnss3 libatk1.0-0 libatk-bridge2.0-0 libgbm1 libcups2 \
  libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
  libpango-1.0-0 libasound2 libdbus-1-3 libx11-6 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python paketleri
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Playwright ve Chromium yükle
RUN python -m playwright install chromium

# Kodu kopyala
COPY . .

# PORT
EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
