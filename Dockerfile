FROM python:3.10-slim

# Sistem bağımlılıklarını yükle (Playwright için gerekli)
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip \
    libxkbcommon0 libpango-1.0-0 libcairo2 \
    fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 \
    libcups2 libdbus-1-3 libdrm2 libgbm1 libnspr4 libnss3 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils libxss1 libxtst6 \
    ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Uygulama klasörü
WORKDIR /app

# Gereken dosyaları kopyala
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Playwright ve chromium kur
RUN pip install playwright
RUN playwright install chromium
# Opsiyonel: Eğer yukarısı çalışmazsa sistem bağımlılığı olarak da:
# RUN playwright install-deps

# Tüm dosyaları kopyala
COPY . .

# Uygulamayı başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
