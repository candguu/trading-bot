# 🌐 Trading Bot'u Online Yapma Rehberi

## Seçenek 1: Kendi Bilgisayarında (Ücretsiz)

### Adım 1: Bilgisayarının IP Adresini Öğren

**Windows:**
```bash
ipconfig
```
`IPv4 Address` satırını bul (örn: 192.168.1.100)

**Telefondan Erişim (Aynı WiFi):**
```
http://192.168.1.100:5001
```

### Adım 2: İnternetten Erişim (Port Forwarding)

1. **Modem/Router'a gir:**
   - Tarayıcıda: `http://192.168.1.1` veya `http://192.168.0.1`
   - Kullanıcı adı/şifre: genelde `admin/admin` veya modem üzerinde yazıyor

2. **Port Forwarding Ayarları:**
   - "Port Forwarding" veya "Sanal Sunucu" bölümünü bul
   - Yeni kural ekle:
     - **Dış Port:** 5001
     - **İç Port:** 5001
     - **İç IP:** 192.168.1.100 (senin bilgisayarın)
     - **Protokol:** TCP

3. **Dış IP'ni Öğren:**
   - https://whatismyipaddress.com
   - Örnek: 85.123.45.67

4. **Telefondan Eriş:**
   ```
   http://85.123.45.67:5001
   ```

### ⚠️ Güvenlik Uyarıları

- Güçlü şifre kullan (.env dosyasında)
- Sadece güvendiğin kişilerle paylaş
- Firewall aktif olsun

---

## Seçenek 2: VPS/Cloud Server (Önerilen - 7/24)

### A) DigitalOcean / Linode / Vultr (Ücretli - $5/ay)

#### 1. VPS Satın Al
- **DigitalOcean:** https://www.digitalocean.com (en popüler)
- **Vultr:** https://www.vultr.com (ucuz)
- **Linode:** https://www.linode.com (güvenilir)

**Önerilen Paket:**
- 1 CPU
- 1GB RAM
- Ubuntu 22.04 LTS
- $5-6/ay

#### 2. VPS'e Bağlan

```bash
ssh root@YOUR_VPS_IP
```

#### 3. Gerekli Paketleri Yükle

```bash
# Sistem güncellemesi
apt update && apt upgrade -y

# Python ve pip
apt install python3 python3-pip python3-venv -y

# Git
apt install git -y

# Nginx (web server)
apt install nginx -y
```

#### 4. Projeyi Yükle

```bash
# Proje klasörü oluştur
mkdir -p /var/www/trading-bot
cd /var/www/trading-bot

# Dosyaları yükle (FTP veya Git ile)
# Veya bilgisayarından kopyala:
# scp -r C:\Users\ahmet\OneDrive\Masaüstü\trading_bot_project/* root@YOUR_VPS_IP:/var/www/trading-bot/
```

#### 5. Python Sanal Ortamı Oluştur

```bash
cd /var/www/trading-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 6. Systemd Service Oluştur (Otomatik Başlatma)

```bash
nano /etc/systemd/system/trading-bot.service
```

İçeriği:
```ini
[Unit]
Description=Trading Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/var/www/trading-bot
Environment="PATH=/var/www/trading-bot/venv/bin"
ExecStart=/var/www/trading-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Kaydet ve çık (Ctrl+X, Y, Enter)

#### 7. Servisi Başlat

```bash
systemctl daemon-reload
systemctl enable trading-bot
systemctl start trading-bot
systemctl status trading-bot
```

#### 8. Nginx Reverse Proxy (Port 80'den Erişim)

```bash
nano /etc/nginx/sites-available/trading-bot
```

İçeriği:
```nginx
server {
    listen 80;
    server_name YOUR_VPS_IP;

    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /socket.io {
        proxy_pass http://127.0.0.1:5001/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Aktif et:
```bash
ln -s /etc/nginx/sites-available/trading-bot /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 9. Firewall Ayarları

```bash
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS (ileride SSL için)
ufw enable
```

#### 10. Eriş!

```
http://YOUR_VPS_IP
```

---

### B) Ücretsiz Cloud (Render.com)

#### 1. Render.com'a Kaydol
https://render.com

#### 2. GitHub'a Yükle (Önce)

```bash
cd C:\Users\ahmet\OneDrive\Masaüstü\trading_bot_project
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/USERNAME/trading-bot.git
git push -u origin main
```

#### 3. Render'da Web Service Oluştur

- "New +" → "Web Service"
- GitHub repo'nu seç
- Ayarlar:
  - **Name:** trading-bot
  - **Environment:** Python 3
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `python main.py`
  - **Plan:** Free

#### 4. Environment Variables Ekle

- `BINANCE_API_KEY`
- `BINANCE_SECRET_KEY`
- `SECRET_KEY`
- `LOGIN_USERNAME`
- `LOGIN_PASSWORD`

#### 5. Deploy Et!

Render otomatik deploy edecek. URL:
```
https://trading-bot-xxxx.onrender.com
```

⚠️ **Ücretsiz planda:**
- 15 dakika inactivity sonrası uyur
- İlk erişimde 30 saniye bekler
- Aylık 750 saat limit

---

## Seçenek 3: Ngrok (Test İçin - Geçici)

Hızlı test için:

```bash
# Ngrok indir: https://ngrok.com/download
# Çalıştır:
ngrok http 5001
```

Sana geçici bir URL verecek:
```
https://abc123.ngrok.io
```

⚠️ Her yeniden başlatmada URL değişir!

---

## 📱 Mobil Erişim İçin İpuçları

### 1. Responsive Tasarım
Zaten responsive, mobilde güzel görünüyor ✅

### 2. PWA (Progressive Web App) Yap

Ana dizine `manifest.json` ekle:
```json
{
  "name": "TradingBot Pro",
  "short_name": "TradingBot",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0b0e11",
  "theme_color": "#f3ba2f",
  "icons": [
    {
      "src": "/static/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

`templates/index.html` head'e ekle:
```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#f3ba2f">
```

Artık "Ana Ekrana Ekle" ile uygulama gibi kullanabilirsin!

---

## 🔒 SSL/HTTPS Ekle (Önerilen)

### Let's Encrypt (Ücretsiz)

```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d yourdomain.com
```

Otomatik yenileme:
```bash
certbot renew --dry-run
```

---

## 📊 Monitoring (İzleme)

### PM2 ile İzleme (Alternatif)

```bash
npm install -g pm2
pm2 start main.py --name trading-bot --interpreter python3
pm2 startup
pm2 save
pm2 monit
```

---

## 🆘 Sorun Giderme

### Log'ları Kontrol Et

**Systemd:**
```bash
journalctl -u trading-bot -f
```

**PM2:**
```bash
pm2 logs trading-bot
```

### Servis Yeniden Başlat

```bash
systemctl restart trading-bot
# veya
pm2 restart trading-bot
```

---

## 💡 Hangi Seçeneği Seçmeliyim?

| Seçenek | Maliyet | Süreklilik | Kolay Kurulum | Önerilen |
|---------|---------|------------|---------------|----------|
| Kendi PC | Ücretsiz | PC açıkken | ⭐⭐⭐⭐⭐ | Test için |
| VPS | $5/ay | 7/24 | ⭐⭐⭐ | ✅ En iyi |
| Render Free | Ücretsiz | Uyur | ⭐⭐⭐⭐ | Deneme için |
| Ngrok | Ücretsiz | Geçici | ⭐⭐⭐⭐⭐ | Hızlı test |

**Önerim:** VPS al, 7/24 çalışsın, her yerden eriş! 🚀
