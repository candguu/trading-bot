# 🚀 Render.com'a Deploy Rehberi (Ücretsiz)

## Adım 1: GitHub Hesabı Oluştur (Yoksa)

1. https://github.com adresine git
2. "Sign up" ile hesap oluştur
3. Email'ini doğrula

## Adım 2: GitHub'a Proje Yükle

### Windows PowerShell'de:

```powershell
# Proje klasörüne git
cd C:\Users\ahmet\OneDrive\Masaüstü\trading_bot_project

# Git başlat
git init

# Tüm dosyaları ekle
git add .

# Commit yap
git commit -m "Initial commit - Trading Bot"

# GitHub'da yeni repo oluştur (tarayıcıda):
# https://github.com/new
# Repo adı: trading-bot
# Public veya Private seç
# "Create repository" tıkla

# GitHub'a bağlan (kendi username'ini yaz)
git remote add origin https://github.com/KULLANICI_ADIN/trading-bot.git

# Push et
git branch -M main
git push -u origin main
```

**Not:** İlk push'ta GitHub kullanıcı adı ve token isteyecek.

### GitHub Token Oluştur:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token (classic)"
3. "repo" seçeneğini işaretle
4. Token'ı kopyala (bir daha göremezsin!)
5. Push yaparken şifre yerine bu token'ı kullan

## Adım 3: Render.com Hesabı Oluştur

1. https://render.com adresine git
2. "Get Started" → "Sign up with GitHub"
3. GitHub ile giriş yap
4. Render'a GitHub erişimi ver

## Adım 4: Web Service Oluştur

1. Render Dashboard'da "New +" → "Web Service"
2. GitHub repo'nu seç: `trading-bot`
3. "Connect" tıkla

## Adım 5: Ayarları Yap

### Genel Ayarlar:
- **Name:** `trading-bot` (veya istediğin isim)
- **Region:** `Frankfurt` (Türkiye'ye en yakın)
- **Branch:** `main`
- **Root Directory:** (boş bırak)
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:app`

### Instance Type:
- **Free** seç

## Adım 6: Environment Variables Ekle

"Environment" sekmesine git ve ekle:

| Key | Value | Açıklama |
|-----|-------|----------|
| `BINANCE_API_KEY` | (senin API key'in) | Binance Testnet API |
| `BINANCE_SECRET_KEY` | (senin secret key'in) | Binance Testnet Secret |
| `SECRET_KEY` | (rastgele 32 karakter) | Flask session key |
| `LOGIN_USERNAME` | `admin` | Giriş kullanıcı adı |
| `LOGIN_PASSWORD` | (güçlü şifre) | Giriş şifresi |

**Secret Key Oluştur:**
```python
import secrets
print(secrets.token_hex(32))
```

## Adım 7: Deploy Et!

1. "Create Web Service" tıkla
2. Deploy başlayacak (5-10 dakika sürer)
3. Log'ları izle

## Adım 8: Link'ini Al

Deploy tamamlandığında:
```
https://trading-bot-xxxx.onrender.com
```

Bu link'i telefonundan aç! 🎉

---

## 📱 Kullanım

### İlk Erişim
- 15 dakika kullanılmazsa uyur
- İlk erişimde 30 saniye bekle (uyanıyor)
- Sonra normal çalışır

### Ana Ekrana Ekle (Mobil)
1. Link'i aç
2. Tarayıcı menüsü → "Ana ekrana ekle"
3. Artık uygulama gibi kullanabilirsin!

---

## 🔄 Güncelleme Yapmak

Kod değiştirdiğinde:

```powershell
cd C:\Users\ahmet\OneDrive\Masaüstü\trading_bot_project

git add .
git commit -m "Güncelleme açıklaması"
git push
```

Render otomatik deploy edecek!

---

## 🐛 Sorun Giderme

### Deploy Başarısız Olursa

1. **Log'ları kontrol et:**
   - Render Dashboard → Service → Logs

2. **Sık karşılaşılan hatalar:**

   **Hata:** `ModuleNotFoundError`
   **Çözüm:** `requirements.txt` eksik paket var, ekle

   **Hata:** `Port already in use`
   **Çözüm:** Start command'da `$PORT` kullan

   **Hata:** `Database locked`
   **Çözüm:** SQLite yerine PostgreSQL kullan (ileride)

### Bot Çalışmıyor

1. **Log'lara bak:**
   ```
   Render Dashboard → Logs
   ```

2. **Environment variables kontrol et:**
   - API key'ler doğru mu?
   - Secret key var mı?

3. **Manuel restart:**
   ```
   Render Dashboard → Manual Deploy → Deploy latest commit
   ```

---

## 💡 İpuçları

### 1. Uyumayı Önle (Opsiyonel)

Ücretsiz bir cron servisi kullan:
- https://cron-job.org
- Her 10 dakikada bir site'ni ping'le
- Böylece hiç uyumaz

**Cron Job Ayarı:**
- URL: `https://trading-bot-xxxx.onrender.com`
- Interval: Every 10 minutes

### 2. Custom Domain (Opsiyonel)

Kendi domain'in varsa:
1. Render → Settings → Custom Domain
2. Domain'ini ekle
3. DNS ayarlarını yap

### 3. Veritabanı Yedekleme

SQLite dosyası her deploy'da sıfırlanır!

**Çözüm 1:** PostgreSQL kullan (Render ücretsiz veriyor)
**Çözüm 2:** Veritabanını dışarıda tut (Supabase, PlanetScale)

---

## 🎯 Sonraki Adımlar

### PostgreSQL'e Geç (Önerilen)

Render ücretsiz PostgreSQL veriyor:

1. Render → New → PostgreSQL
2. Free plan seç
3. Database URL'i kopyala
4. `database.py`'yi güncelle (SQLite → PostgreSQL)

### SSL/HTTPS

Render otomatik SSL veriyor! ✅
Link'in zaten HTTPS olacak.

### Monitoring

Render Dashboard'dan:
- CPU kullanımı
- Memory kullanımı
- Request sayısı
- Log'lar

---

## 📞 Destek

**Render Docs:** https://render.com/docs
**Community:** https://community.render.com

---

## ✅ Checklist

- [ ] GitHub hesabı oluşturdum
- [ ] Projeyi GitHub'a yükledim
- [ ] Render hesabı oluşturdum
- [ ] Web Service oluşturdum
- [ ] Environment variables ekledim
- [ ] Deploy ettim
- [ ] Link'i test ettim
- [ ] Telefondan erişebildim
- [ ] Ana ekrana ekledim

Hepsi tamam mı? Tebrikler! 🎉

---

## 🆘 Yardım Lazım?

Bir sorun olursa:
1. Render log'larını kontrol et
2. GitHub repo'nun public olduğundan emin ol
3. Environment variables'ları kontrol et
4. Manuel deploy dene

Hala çözülmezse, log'ları paylaş!
