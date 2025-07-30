# 1. Temel Python imajı
FROM python:3.10-slim

# 2. Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libxss1 \
    libxtst6 \
    ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Uygulama dizini
WORKDIR /app

# 4. Gerekli dosyaları kopyala
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 5. Playwright kurulum ve tarayıcı indir
RUN pip install playwright && playwright install chromium

# 6. Uygulama dosyaları
COPY . .

# 7. Başlatma komutu
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
