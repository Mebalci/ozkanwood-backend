FROM python:3.10-slim

# Gerekli sistem kütüphanelerini kur
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libnss3 \
    libxss1 \
    libxtst6 \
    libgbm1 \
    libxshmfence-dev \
    libx11-xcb1 \
    && apt-get clean

# Node ve Playwright tarayıcı kurulumu için gerekli
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g playwright && \
    playwright install chromium

# Uygulama dosyaları
WORKDIR /app
COPY . .

# Python bağımlılıklarını kur
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Uygulama başlat
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
