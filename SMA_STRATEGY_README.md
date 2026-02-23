# 🚀 SMA 5/9 Otomatik Trading Stratejisi

## 📋 Yapılan Değişiklikler

### ✅ Temizlik İşlemleri
- ❌ 7 indikatörlü (RSI, MACD, OTT, BB, Stoch, ADX, Supertrend) karmaşık sistem kaldırıldı
- ❌ 3 botlu konsensüs mekanizması kaldırıldı
- ❌ Gereksiz indikatör fonksiyonları temizlendi
- ✅ Kod tabanı basitleştirildi ve optimize edildi

### 🎯 Yeni SMA 5/9 Crossover Stratejisi

#### Strateji Kuralları:
1. **GOLDEN CROSS (AL)**: SMA 5 aşağıdan yukarı keser SMA 9
   - Önceki mumda: SMA5 <= SMA9
   - Şimdiki mumda: SMA5 > SMA9
   - Bakiyenin %95'i ile market fiyatından BTC alımı yapılır
   - %5 komisyon rezervi bırakılır

2. **DEATH CROSS (SAT)**: SMA 5 yukarıdan aşağı keser SMA 9
   - Önceki mumda: SMA5 >= SMA9
   - Şimdiki mumda: SMA5 < SMA9
   - Tüm BTC market fiyatından satılır
   - USDT'ye geçilir

#### Teknik Detaylar:
- **SMA 5**: 5 periyotluk Basit Hareketli Ortalama
- **SMA 9**: 9 periyotluk Basit Hareketli Ortalama
- **Zaman Dilimi**: 15 dakikalık mumlar
- **Sinyal Kontrolü**: Her 3 saniyede bir
- **Otomatik İşlem**: Sinyal değiştiğinde tetiklenir

### 🔧 Backend Değişiklikleri (main.py)

#### Yeni Fonksiyonlar:
```python
# SMA hesaplama
safe_sma(df_close, length)

# Crossover stratejisi (YENİ!)
calc_sma_crossover_signal(df)  # Returns: signal, sma5, sma9
# - Golden Cross algılar (SMA5 yukarı keser SMA9) → BUY
# - Death Cross algılar (SMA5 aşağı keser SMA9) → SELL
# - Önceki ve şimdiki değerleri karşılaştırır

# Otomatik alım/satım
auto_buy(price)   # %95 bakiye ile AL
auto_sell(price)  # Tüm BTC'yi SAT
```

#### Kaldırılan Fonksiyonlar:
- `safe_bb()` - Bollinger Bands
- `safe_macd()` - MACD
- `safe_stoch()` - Stochastic
- `safe_adx()` - ADX
- `safe_rsi()` - RSI
- `safe_ott()` - OTT
- `safe_ema()` - EMA
- `safe_supertrend()` - Supertrend
- `calc_consensus()` - 3 bot konsensüs

#### Bot Engine:
```python
def bot_engine():
    # Her 3 saniyede:
    # 1. Fiyat ve 15m mum verisi çek
    # 2. SMA 5 ve SMA 9 hesapla (tüm seriler)
    # 3. Önceki ve şimdiki değerleri karşılaştır
    # 4. Kesişim var mı kontrol et:
    #    - Golden Cross (yukarı kesişim) → BUY
    #    - Death Cross (aşağı kesişim) → SELL
    # 5. Kesişim anında otomatik işlem yap
    # 6. Frontend'e veri gönder
```

### 🎨 Frontend Değişiklikleri (spot.html)

#### Kaldırılan UI Elemanları:
- ❌ RSI göstergesi ve mini widget
- ❌ EMA20/EMA50 göstergeleri
- ❌ Konsensüs slider (2/3 bot seçimi)
- ❌ 7 indikatör paneli

#### Yeni UI Elemanları:
- ✅ SMA 5 göstergesi (yeşil)
- ✅ SMA 9 göstergesi (mavi)
- ✅ SMA mini widget (sidebar)
- ✅ Sinyal durumu göstergesi

#### Yeni JavaScript Fonksiyonları:
```javascript
updateSMA(sma5, sma9, signal)  // SMA değerlerini güncelle
```

### 📊 Veri Akışı

```
Backend (main.py)
    ↓
bot_engine() her 3 saniyede
    ↓
SMA 5 ve SMA 9 hesapla
    ↓
Sinyal üret (BUY/SELL/null)
    ↓
Sinyal değiştiyse → Otomatik işlem
    ↓
SocketIO ile frontend'e gönder
    ↓
Frontend (spot.html)
    ↓
SMA değerlerini göster
    ↓
Sinyal durumunu göster
```

### 🎮 Kullanım

1. **Otomatik Mod**: 
   - Sağ üstteki "🤖 Oto: AKTİF" butonu ile açık/kapalı
   - Açıkken SMA sinyallerine göre otomatik işlem yapar

2. **Manuel Mod**:
   - Oto modu kapatarak manuel işlem yapabilirsiniz
   - SMA sinyalleri yine de görünür

3. **Görsel Göstergeler**:
   - Header'da: SMA 5 ve SMA 9 değerleri
   - Sidebar'da: Mini SMA widget ve sinyal durumu
   - Alert banner: Aktif sinyal varsa gösterir

### ⚙️ Konfigürasyon

```python
# main.py içinde
SYMBOL      = "BTCUSDT"  # Trading çifti
SMA_FAST    = 5          # Hızlı SMA periyodu
SMA_SLOW    = 9          # Yavaş SMA periyodu
AUTO_TRADE  = True       # Otomatik işlem
LEVERAGE    = 1          # Kaldıraç (spot için 1x)
```

### 🔒 Güvenlik

- %95 bakiye kullanımı (%5 komisyon rezervi)
- Minimum işlem limitleri kontrol edilir
- Hata durumunda bildirim gönderilir
- Socket bağlantısı koptuğunda uyarı verir

### 📈 Performans

- Hafif ve hızlı strateji
- Gereksiz hesaplamalar kaldırıldı
- 3 saniyede bir güncelleme
- Düşük CPU kullanımı

### 🚀 Başlatma

```bash
python main.py
```

Tarayıcıda: `http://localhost:5001`

### 📝 Notlar

- Testnet üzerinde çalışır (Binance Testnet)
- Gerçek para riski yoktur
- Strateji eğitim amaçlıdır
- Canlı kullanım öncesinde test edilmelidir

---

**Strateji Özeti**: Klasik SMA Crossover stratejisi. Golden Cross (SMA5 yukarı keser SMA9) alım, Death Cross (SMA5 aşağı keser SMA9) satım sinyali üretir. Kesişim anlarını yakalayarak trend değişimlerinde pozisyon alır.
