# 💾 Veritabanı Sistemi

## Genel Bakış

Trading bot artık tüm verileri **SQLite veritabanında** kalıcı olarak saklıyor. Sistemi yeniden başlattığınızda:

✅ İşlem geçmişi korunur
✅ Sinyal geçmişi korunur  
✅ Başlangıç bakiyesi korunur
✅ Açık emirler (SL/TP) korunur

## Veritabanı Dosyası

**Dosya:** `trading_bot.db`
**Konum:** Proje ana dizini
**Tip:** SQLite3 (dosya tabanlı, kurulum gerektirmez)

## Tablolar

### 1. trade_history
İşlem geçmişi - Tüm alım/satım işlemleri

| Sütun | Tip | Açıklama |
|-------|-----|----------|
| id | INTEGER | Otomatik artan ID |
| timestamp | TEXT | ISO format zaman damgası |
| time | TEXT | Görüntüleme zamanı (HH:MM:SS) |
| side | TEXT | BUY veya SELL |
| type | TEXT | MARKET veya LIMIT |
| qty | REAL | Miktar (BTC) |
| price | REAL | Fiyat (USDT) |
| value | REAL | Toplam değer (USDT) |
| symbol | TEXT | İşlem çifti (BTCUSDT) |

### 2. signal_history
Sinyal geçmişi - Golden Cross / Death Cross sinyalleri

| Sütun | Tip | Açıklama |
|-------|-----|----------|
| id | INTEGER | Otomatik artan ID |
| timestamp | INTEGER | Unix timestamp |
| type | TEXT | buy veya sell |
| price | REAL | Sinyal anındaki fiyat |
| ind1 | REAL | SMA5 veya OTT değeri |
| ind2 | REAL | SMA9 veya Close değeri |
| ind1_name | TEXT | İndikatör adı |
| ind2_name | TEXT | İndikatör adı |
| executed | INTEGER | Otomatik işlem yapıldı mı (0/1) |
| symbol | TEXT | İşlem çifti |

### 3. bot_settings
Bot ayarları - Başlangıç bakiyesi vb.

| Sütun | Tip | Açıklama |
|-------|-----|----------|
| key | TEXT | Ayar anahtarı (PRIMARY KEY) |
| value | TEXT | JSON formatında değer |
| updated_at | TEXT | Son güncelleme zamanı |

**Önemli ayarlar:**
- `starting_value`: Başlangıç bakiyesi (kar/zarar hesabı için)

### 4. open_orders
Açık emirler - Stop Loss ve Take Profit emirleri

| Sütun | Tip | Açıklama |
|-------|-----|----------|
| id | TEXT | Emir ID (PRIMARY KEY) |
| type | TEXT | STOP_LOSS veya TAKE_PROFIT |
| side | TEXT | BUY veya SELL |
| qty | REAL | Miktar |
| trigger | REAL | Tetikleme fiyatı |
| time | TEXT | Oluşturulma zamanı |
| symbol | TEXT | İşlem çifti |

## Kullanım

### Python'dan Erişim

```python
import database as db

# Veritabanını başlat
db.init_database()

# İşlem kaydet
db.save_trade({
    "time": "14:30:45",
    "side": "BUY",
    "type": "MARKET",
    "qty": 0.001,
    "price": 65000,
    "value": 65,
    "symbol": "BTCUSDT"
})

# İşlem geçmişini getir
trades = db.get_trade_history(limit=50)

# Sinyal kaydet
db.save_signal({
    "type": "buy",
    "price": 65000,
    "time": 1234567890,
    "ind1": 64800,
    "ind2": 64900,
    "ind1_name": "SMA5",
    "ind2_name": "SMA9",
    "executed": True,
    "symbol": "BTCUSDT"
})

# Sinyal geçmişini getir
signals = db.get_signal_history(limit=10)

# Ayar kaydet
db.save_setting("starting_value", 75000.0)

# Ayar getir
starting_value = db.get_setting("starting_value", default=0.0)

# İstatistikler
stats = db.get_stats()
print(stats)  # {'total_trades': 42, 'total_signals': 15, 'open_orders': 2}
```

### Web API'den Erişim

#### Veritabanı İstatistikleri
```
GET /api/database/stats
```

Yanıt:
```json
{
  "total_trades": 42,
  "total_signals": 15,
  "open_orders": 2
}
```

#### Tablo Temizleme
```
POST /api/database/clear/<table>
```

Tablolar:
- `trades` - İşlem geçmişini temizle
- `signals` - Sinyal geçmişini temizle
- `orders` - Açık emirleri temizle
- `all` - Tüm veritabanını temizle

#### Başlangıç Bakiyesini Sıfırla
```
POST /api/database/reset_starting_value
```

Şimdiki bakiyeyi başlangıç bakiyesi olarak ayarlar (kar/zarar hesabını sıfırlar).

## Ayarlar Sayfası

**Konum:** http://localhost:5001/settings

Ayarlar sayfasından:
- Veritabanı istatistiklerini görüntüleyebilirsiniz
- İşlem/sinyal geçmişini temizleyebilirsiniz
- Başlangıç bakiyesini sıfırlayabilirsiniz
- Tüm veritabanını temizleyebilirsiniz

## Yedekleme

Veritabanını yedeklemek için `trading_bot.db` dosyasını kopyalayın:

```bash
# Windows
copy trading_bot.db trading_bot_backup.db

# Linux/Mac
cp trading_bot.db trading_bot_backup.db
```

## Veritabanını Sıfırlama

Tüm verileri silmek ve sıfırdan başlamak için:

```bash
# Veritabanı dosyasını sil
rm trading_bot.db  # Linux/Mac
del trading_bot.db  # Windows

# Bot'u yeniden başlat - yeni veritabanı oluşturulacak
python main.py
```

## Performans

- SQLite hafif ve hızlıdır
- Dosya boyutu: ~100KB (boş), ~1-5MB (1000 işlem)
- Okuma/yazma hızı: Milisaniyeler
- Eşzamanlı erişim: Thread-safe

## Notlar

⚠️ **Önemli:** `trading_bot.db` dosyasını silmeyin veya taşımayın!

✅ **Otomatik:** Bot başlatıldığında veritabanı otomatik oluşturulur

✅ **Güvenli:** Tüm işlemler transaction içinde yapılır

✅ **Taşınabilir:** Veritabanı dosyasını başka bir bilgisayara kopyalayabilirsiniz
