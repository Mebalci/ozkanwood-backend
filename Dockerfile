FROM python:3.11-slim

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    libxtst6 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    ca-certificates \
    && apt-get clean

# Çalışma klasörü
WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install chromium

# Uygulama dosyaları
COPY . .

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=10000"]
