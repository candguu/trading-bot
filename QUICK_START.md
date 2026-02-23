# ⚡ Hızlı Başlangıç - 5 Dakikada Online!

## 🎯 Hedef
Trading bot'unu ücretsiz olarak online yap, telefondan eriş!

## 📋 Gereksinimler
- GitHub hesabı (ücretsiz)
- Render.com hesabı (ücretsiz)
- 5 dakika

---

## 🚀 Adım Adım

### 1️⃣ GitHub Hesabı Oluştur (2 dakika)

Eğer yoksa:
1. https://github.com/signup
2. Email, kullanıcı adı, şifre gir
3. Email'ini doğrula

### 2️⃣ GitHub'a Yükle (2 dakika)

**Otomatik (Kolay):**
```powershell
.\deploy.ps1
```

Script sana soracak:
- GitHub kullanıcı adın: `ahmetxyz`
- Repo adı: `trading-bot` (Enter bas)

**Manuel (Alternatif):**
```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADIN/trading-bot.git
git push -u origin main
```

### 3️⃣ Render.com'a Deploy Et (1 dakika)

1. **Render'a git:** https://render.com
2. **GitHub ile giriş yap**
3. **New + → Web Service**
4. **Repo seç:** `trading-bot`
5. **Ayarlar:**
   - Name: `trading-bot`
   - Region: `Frankfurt`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT wsgi:app`
   - Plan: **Free**

6. **Environment Variables ekle:**
   ```
   BINANCE_API_KEY = (senin key'in)
   BINANCE_SECRET_KEY = (senin secret'in)
   SECRET_KEY = (rastgele 32 karakter)
   LOGIN_USERNAME = admin
   LOGIN_PASSWORD = (güçlü şifre)
   ```

7. **Create Web Service**

### 4️⃣ Bekle (5-10 dakika)

Deploy log'larını izle. "Live" yazısını gördüğünde hazır!

### 5️⃣ Eriş! 🎉

Link'in:
```
https://trading-bot-xxxx.onrender.com
```

Telefondan aç, giriş yap, kullan!

---

## 📱 Mobil İpuçları

### Ana Ekrana Ekle
1. Link'i aç
2. Tarayıcı menü → "Ana ekrana ekle"
3. Artık uygulama gibi!

### Uyumayı Önle
https://cron-job.org ile her 10 dakikada ping at

---

## 🔄 Güncelleme

Kod değiştirdiğinde:
```powershell
git add .
git commit -m "Güncelleme"
git push
```

Render otomatik deploy eder!

---

## ⚠️ Önemli Notlar

1. **Ücretsiz plan:**
   - 15 dakika inactivity → uyur
   - İlk erişim → 30 saniye bekle
   - Aylık 750 saat limit

2. **Veritabanı:**
   - SQLite her deploy'da sıfırlanır
   - PostgreSQL'e geç (ücretsiz)

3. **Güvenlik:**
   - Güçlü şifre kullan
   - API key'leri paylaşma

---

## 🆘 Sorun mu Var?

### Deploy başarısız
→ `RENDER_DEPLOY.md` oku

### Bot çalışmıyor
→ Render Dashboard → Logs kontrol et

### Veritabanı sıfırlanıyor
→ PostgreSQL kullan

---

## ✅ Başarı!

Artık trading bot'un online ve her yerden erişilebilir! 🎉

**Link'ini kaydet ve paylaş!**
