# 📤 GitHub'a Yükleme Rehberi (Detaylı)

## 🎯 Amaç
Trading bot projeni GitHub'a yükleyeceğiz. Bu sayede Render.com'da deploy edebileceğiz.

---

## Ön Hazırlık

### 1. Git Kurulu mu Kontrol Et

PowerShell'i aç ve yaz:
```powershell
git --version
```

**Çıktı:**
- ✅ `git version 2.x.x` → Git kurulu, devam et
- ❌ `git: The term 'git' is not recognized` → Git kur

### Git Kurulumu (Gerekirse)

1. https://git-scm.com/download/win adresine git
2. "64-bit Git for Windows Setup" indir
3. Çalıştır, hep "Next" bas (varsayılan ayarlar tamam)
4. Kurulum bitince PowerShell'i KAPAT ve YENİDEN AÇ
5. `git --version` ile kontrol et

---

## ADIM 1: GitHub Hesabı Oluştur

### 1.1 GitHub'a Git
https://github.com/signup

### 1.2 Bilgileri Gir

**Email:**
```
senin@email.com
```

**Şifre:**
```
Güçlü bir şifre (en az 15 karakter)
```

**Kullanıcı Adı:**
```
ahmettrading  (veya istediğin)
```

### 1.3 Doğrulama
- Robot değilim puzzle'ı çöz
- "Create account" tıkla

### 1.4 Email Doğrulama
- Email'ine gelen kodu gir
- Hesabın aktif!

### 1.5 Anket (Opsiyonel)
- "Skip personalization" tıkla (gerek yok)

---

## ADIM 2: GitHub'da Yeni Repo Oluştur

### 2.1 New Repository
GitHub'da sağ üstte "+" → "New repository"

### 2.2 Repo Ayarları

**Repository name:**
```
trading-bot
```

**Description (opsiyonel):**
```
Crypto Trading Bot with SMA Strategy
```

**Public / Private:**
- ✅ **Public** seç (ücretsiz, herkes görebilir ama sorun değil)
- Private istersen ücretli plan gerekir

**Initialize repository:**
- ❌ "Add a README file" - İŞARETLEME
- ❌ "Add .gitignore" - İŞARETLEME  
- ❌ "Choose a license" - İŞARETLEME

### 2.3 Create Repository
"Create repository" tıkla

### 2.4 Repo URL'ini Kopyala
Açılan sayfada göreceksin:
```
https://github.com/ahmettrading/trading-bot.git
```

Bu URL'i bir yere not et! (Lazım olacak)

---

## ADIM 3: Personal Access Token Oluştur

GitHub artık şifre ile push kabul etmiyor, token gerekiyor.

### 3.1 Settings'e Git
GitHub'da sağ üstte profil fotoğrafın → "Settings"

### 3.2 Developer Settings
Sol menüde en altta "Developer settings"

### 3.3 Personal Access Tokens
"Personal access tokens" → "Tokens (classic)"

### 3.4 Generate New Token
"Generate new token (classic)" tıkla

### 3.5 Token Ayarları

**Note:**
```
Trading Bot Deploy
```

**Expiration:**
```
90 days (veya No expiration)
```

**Select scopes:**
- ✅ **repo** (tüm kutucukları işaretle)
  - repo:status
  - repo_deployment
  - public_repo
  - repo:invite
  - security_events

### 3.6 Generate Token
"Generate token" tıkla

### 3.7 Token'ı Kopyala
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **ÇOK ÖNEMLİ:** Bu token'ı HEMEN kopyala ve güvenli bir yere kaydet!
Sayfayı kapatınca bir daha göremezsin!

**Nereye kaydet:**
- Not defterine yapıştır
- Veya şifre yöneticisine kaydet

---

## ADIM 4: Proje Klasörüne Git

### 4.1 PowerShell Aç
Windows tuşu + X → "Windows PowerShell"

### 4.2 Proje Klasörüne Git
```powershell
cd C:\Users\ahmet\OneDrive\Masaüstü\trading_bot_project
```

### 4.3 Klasörü Kontrol Et
```powershell
ls
```

Görmeli:
- main.py
- database.py
- templates/
- static/
- .env
- vb.

---

## ADIM 5: Git Başlat

### 5.1 Git Init
```powershell
git init
```

**Çıktı:**
```
Initialized empty Git repository in C:/Users/ahmet/OneDrive/Masaüstü/trading_bot_project/.git/
```

### 5.2 Git Config (İlk Kez)
```powershell
git config --global user.name "Ahmet"
git config --global user.email "senin@email.com"
```

(GitHub'daki email'ini kullan)

---

## ADIM 6: Dosyaları Ekle

### 6.1 Tüm Dosyaları Ekle
```powershell
git add .
```

(Nokta önemli! Tüm dosyaları ekler)

### 6.2 Kontrol Et
```powershell
git status
```

**Çıktı:**
```
Changes to be committed:
  new file:   main.py
  new file:   database.py
  new file:   templates/index.html
  ...
```

Yeşil yazılar göreceksin - bu iyi!

---

## ADIM 7: Commit Yap

### 7.1 Commit
```powershell
git commit -m "Initial commit - Trading Bot"
```

**Çıktı:**
```
[main (root-commit) abc1234] Initial commit - Trading Bot
 50 files changed, 2000 insertions(+)
 create mode 100644 main.py
 ...
```

---

## ADIM 8: Branch Ayarla

### 8.1 Main Branch
```powershell
git branch -M main
```

(Eski adı "master" idi, şimdi "main" kullanılıyor)

---

## ADIM 9: GitHub'a Bağlan

### 9.1 Remote Ekle
```powershell
git remote add origin https://github.com/ahmettrading/trading-bot.git
```

⚠️ **DİKKAT:** Kendi kullanıcı adını ve repo adını kullan!

### 9.2 Kontrol Et
```powershell
git remote -v
```

**Çıktı:**
```
origin  https://github.com/ahmettrading/trading-bot.git (fetch)
origin  https://github.com/ahmettrading/trading-bot.git (push)
```

---

## ADIM 10: GitHub'a Push Et

### 10.1 Push
```powershell
git push -u origin main
```

### 10.2 Giriş İste
PowerShell sana soracak:

**Username:**
```
ahmettrading
```
(GitHub kullanıcı adın)

**Password:**
```
ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
⚠️ **ŞİFRE DEĞİL, TOKEN!** (Adım 3'te kopyaladığın token'ı yapıştır)

**Not:** Token'ı yapıştırırken ekranda görünmez, normal!

### 10.3 Push Başarılı
**Çıktı:**
```
Enumerating objects: 50, done.
Counting objects: 100% (50/50), done.
Delta compression using up to 8 threads
Compressing objects: 100% (45/45), done.
Writing objects: 100% (50/50), 100.00 KiB | 5.00 MiB/s, done.
Total 50 (delta 5), reused 0 (delta 0), pack-reused 0
To https://github.com/ahmettrading/trading-bot.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **BAŞARILI!**

---

## ADIM 11: GitHub'da Kontrol Et

### 11.1 Tarayıcıda Aç
```
https://github.com/ahmettrading/trading-bot
```

### 11.2 Dosyaları Gör
Görmeli:
- main.py
- database.py
- templates/
- requirements.txt
- README.md (varsa)
- vb.

✅ Tüm dosyalar orada!

---

## 🎉 Tebrikler!

Projen GitHub'da! Artık Render.com'a deploy edebilirsin.

---

## 🔄 Gelecekte Güncelleme

Kod değiştirdiğinde:

```powershell
# 1. Klasöre git
cd C:\Users\ahmet\OneDrive\Masaüstü\trading_bot_project

# 2. Değişiklikleri ekle
git add .

# 3. Commit yap
git commit -m "Güncelleme açıklaması"

# 4. Push et
git push
```

Token tekrar istemez (kaydedildi).

---

## 🐛 Sorun Giderme

### Hata: "git: command not found"
**Çözüm:** Git'i kur (Adım 1)

### Hata: "remote origin already exists"
**Çözüm:**
```powershell
git remote remove origin
git remote add origin https://github.com/KULLANICI_ADIN/trading-bot.git
```

### Hata: "Authentication failed"
**Çözüm:**
- Token'ı doğru kopyaladın mı?
- Token'ın "repo" yetkisi var mı?
- Yeni token oluştur ve tekrar dene

### Hata: "Repository not found"
**Çözüm:**
- GitHub'da repo oluşturdun mu?
- URL doğru mu? (kullanıcı adı ve repo adı)
- Repo public mi?

### Hata: "Permission denied"
**Çözüm:**
- GitHub kullanıcı adın doğru mu?
- Token'ı şifre yerine mi girdin?

---

## ✅ Checklist

Tamamladıysan işaretle:

- [ ] Git kurdum
- [ ] GitHub hesabı oluşturdum
- [ ] GitHub'da repo oluşturdum
- [ ] Personal Access Token oluşturdum
- [ ] Token'ı güvenli yere kaydettim
- [ ] Proje klasörüne gittim
- [ ] `git init` yaptım
- [ ] `git add .` yaptım
- [ ] `git commit` yaptım
- [ ] `git remote add origin` yaptım
- [ ] `git push` yaptım
- [ ] GitHub'da dosyaları gördüm

Hepsi tamam mı? Sonraki adıma geç! 🚀

---

## 📞 Yardım

Bir sorun olursa:
1. Hata mesajını oku
2. "Sorun Giderme" bölümüne bak
3. Google'da ara: "git [hata mesajı]"
4. Bana sor!

---

## 🎯 Sonraki Adım

GitHub'a yükleme tamam! Şimdi:

**Render.com'a Deploy** → `RENDER_DEPLOY.md` dosyasını aç
