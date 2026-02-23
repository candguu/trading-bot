FROM python:3.11-slim

WORKDIR /app

# Sistem paketlerini yükle
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python paketlerini yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Port
ENV PORT=5001
EXPOSE 5001

# Başlat
CMD gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:app
