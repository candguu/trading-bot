# Kripto Ticaret Otomasyon Sistemi - Teknik Tasarım

## Genel Bakış

Kripto Ticaret Otomasyon Sistemi, Binance kripto para borsasında 7/24 otomatik alım-satım yapabilen, matematiksel verilere ve teknik analiz stratejilerine dayalı çalışan bir web tabanlı yazılım sistemidir. Sistem, modern web teknolojileri kullanarak profesyonel bir kullanıcı arayüzü sunar ve üç ana katmandan oluşur:

1. **Veri Toplama Katmanı**: Binance API üzerinden gerçek zamanlı piyasa verilerini toplama
2. **Strateji ve Karar Katmanı**: Teknik indikatör hesaplama ve alım-satım sinyali üretme
3. **İşlem Yürütme Katmanı**: Otomatik emir iletimi ve portföy yönetimi
4. **Sunum Katmanı**: Modern web arayüzü ile kullanıcı etkileşimi

Sistem, manuel kontrol panelinden başlayarak testnet simülasyonuna, ardından canlı piyasada tam otonom çalışmaya doğru ilerleyen bir geliştirme yolu izler.

### Temel Özellikler

- Gerçek zamanlı piyasa verisi toplama ve analiz
- 7 farklı teknik indikatör (RSI, MACD, Bollinger Bands, Stochastic, ADX, EMA, SuperTrend)
- Konsensüs tabanlı sinyal üretimi
- Otomatik ve manuel işlem yürütme
- Testnet ve canlı işlem modu desteği
- Profesyonel web arayüzü (dark/light mode)
- İnteraktif grafikler ve veri görselleştirme
- Gelişmiş portföy ve hesap yönetimi
- Gerçek zamanlı bildirim sistemi

## Mimari

### Sistem Mimarisi

Sistem, katmanlı mimari (layered architecture) prensiplerine göre tasarlanmıştır:

```
┌─────────────────────────────────────────────────────────────┐
│                    Sunum Katmanı (Web UI)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │Portfolio │  │ Charts   │  │ History  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                    Uygulama Katmanı (Backend)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   API        │  │  WebSocket   │  │   Auth       │     │
│  │   Routes     │  │   Handler    │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    İş Mantığı Katmanı                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Strategy   │  │    Order     │  │  Portfolio   │     │
│  │   Engine     │  │   Executor   │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Veri Erişim Katmanı                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Market     │  │   Database   │  │    Cache     │     │
│  │   Data       │  │   Access     │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Dış Servisler                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  Binance API │  │   Database   │                        │
│  │ (REST/WS)    │  │  (SQLite)    │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Teknoloji Yığını

**Backend:**
- **Dil**: Python 3.10+
- **Web Framework**: Flask veya FastAPI
- **WebSocket**: Socket.IO veya FastAPI WebSocket
- **Binance Entegrasyonu**: python-binance kütüphanesi
- **Teknik Analiz**: TA-Lib veya pandas-ta
- **Veritabanı**: SQLite (geliştirme), PostgreSQL (production opsiyonel)
- **Önbellekleme**: Redis (opsiyonel)

**Frontend:**
- **HTML5**: Semantik yapı
- **CSS3**: Modern styling, Flexbox/Grid layout
- **JavaScript (ES6+)**: Vanilla JS veya minimal framework
- **Grafik Kütüphanesi**: Chart.js veya TradingView Lightweight Charts
- **UI Framework**: Bootstrap 5 veya Tailwind CSS (opsiyonel)
- **İkonlar**: Font Awesome veya Material Icons

**Deployment:**
- **Konteynerizasyon**: Docker
- **Process Manager**: PM2 veya systemd
- **Reverse Proxy**: Nginx (opsiyonel)

### Veri Akışı

1. **Piyasa Verisi Akışı**:
   ```
   Binance API → Market Data Collector → Cache → Strategy Engine
                                        ↓
                                   Database (historical)
   ```

2. **Sinyal Üretimi Akışı**:
   ```
   Market Data → Technical Indicators → Consensus Score → Trading Signal
                                                              ↓
                                                         Trade Log
   ```

3. **Emir Yürütme Akışı**:
   ```
   Trading Signal → Order Executor → Binance API → Order Confirmation
                         ↓                              ↓
                    Trade Log  ←─────────────────────────
   ```

4. **Web Arayüzü Veri Akışı**:
   ```
   Backend State → WebSocket → Frontend Components → User Display
        ↑                                                  ↓
        └──────────────── User Actions ───────────────────
   ```

## Bileşenler ve Arayüzler

### 1. Market Data Collector

**Sorumluluklar:**
- Binance API'den gerçek zamanlı piyasa verisi toplama
- WebSocket bağlantısı yönetimi
- Veri normalizasyonu ve doğrulama
- Rate limiting kontrolü

**Arayüz:**
```python
class MarketDataCollector:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False)
    def connect() -> bool
    def disconnect() -> None
    def get_ticker_price(symbol: str) -> float
    def get_klines(symbol: str, interval: str, limit: int) -> List[Kline]
    def get_order_book(symbol: str, limit: int) -> OrderBook
    def subscribe_ticker(symbol: str, callback: Callable) -> None
    def get_account_balance() -> Dict[str, float]
```

**Veri Modelleri:**
```python
@dataclass
class Kline:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass
class OrderBook:
    bids: List[Tuple[float, float]]  # (price, quantity)
    asks: List[Tuple[float, float]]
    timestamp: int
```

### 2. Strategy Engine

**Sorumluluklar:**
- Teknik indikatör hesaplama
- Konsensüs skoru üretimi
- Alım-satım sinyali oluşturma
- Sinyal güven seviyesi hesaplama

**Arayüz:**
```python
class StrategyEngine:
    def __init__(self, config: StrategyConfig)
    def calculate_indicators(data: List[Kline]) -> IndicatorValues
    def generate_signal(indicators: IndicatorValues) -> TradingSignal
    def get_consensus_score(indicators: IndicatorValues) -> float
    def update_strategy_weights(performance_data: List[Trade]) -> None
```

**Teknik İndikatörler:**
```python
@dataclass
class IndicatorValues:
    rsi: float  # Relative Strength Index (0-100)
    macd: Tuple[float, float, float]  # (macd, signal, histogram)
    bollinger: Tuple[float, float, float]  # (upper, middle, lower)
    stochastic: Tuple[float, float]  # (%K, %D)
    adx: float  # Average Directional Index
    ema: Dict[int, float]  # {period: value}
    supertrend: Tuple[float, str]  # (value, trend: 'up'/'down')
    timestamp: int

@dataclass
class TradingSignal:
    signal_type: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float  # 0.0 - 1.0
    consensus_score: float
    indicators: IndicatorValues
    timestamp: int
    reason: str
```

**Konsensüs Skoru Hesaplama:**
- Her indikatör -1 (güçlü sat) ile +1 (güçlü al) arasında normalize edilir
- Ağırlıklı ortalama ile konsensüs skoru hesaplanır
- Eşik değerleri: consensus_score > 0.6 → AL, < -0.6 → SAT, diğer → BEKLİ

### 3. Order Executor

**Sorumluluklar:**
- Emir oluşturma ve gönderme
- Bakiye kontrolü
- Emir durumu takibi
- Hata yönetimi

**Arayüz:**
```python
class OrderExecutor:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = False)
    def execute_signal(signal: TradingSignal, symbol: str, amount: float) -> Order
    def place_market_order(symbol: str, side: str, quantity: float) -> Order
    def place_limit_order(symbol: str, side: str, quantity: float, price: float) -> Order
    def cancel_order(symbol: str, order_id: str) -> bool
    def get_order_status(symbol: str, order_id: str) -> OrderStatus
    def calculate_order_size(balance: float, risk_percent: float) -> float
```

**Veri Modelleri:**
```python
@dataclass
class Order:
    order_id: str
    symbol: str
    side: str  # 'BUY' or 'SELL'
    order_type: str  # 'MARKET' or 'LIMIT'
    quantity: float
    price: Optional[float]
    status: str  # 'NEW', 'FILLED', 'CANCELED', 'REJECTED'
    timestamp: int
    filled_quantity: float
    average_price: float
```

### 4. Trading Bot Controller

**Sorumluluklar:**
- Ana işlem döngüsü yönetimi
- Bot durumu kontrolü (aktif/pasif)
- Bileşenler arası koordinasyon
- Hata yönetimi ve kurtarma

**Arayüz:**
```python
class TradingBot:
    def __init__(self, config: BotConfig)
    def start() -> None
    def stop() -> None
    def set_active(active: bool) -> None
    def is_active() -> bool
    def get_status() -> BotStatus
    def run_cycle() -> None  # Tek bir işlem döngüsü
    def emergency_stop() -> None
```

**Ana İşlem Döngüsü:**
```python
def run_cycle():
    # 1. Piyasa verisi toplama
    market_data = collector.get_klines(symbol, interval, limit)
    
    # 2. Teknik analiz
    indicators = strategy.calculate_indicators(market_data)
    
    # 3. Sinyal üretimi
    signal = strategy.generate_signal(indicators)
    
    # 4. Emir yürütme (bot aktifse)
    if bot.is_active() and signal.signal_type != 'HOLD':
        order = executor.execute_signal(signal, symbol, amount)
        log_trade(order, signal)
    
    # 5. WebSocket ile frontend güncelleme
    websocket.broadcast_update({
        'indicators': indicators,
        'signal': signal,
        'balance': collector.get_account_balance()
    })
```

### 5. Web Backend (API Server)

**Sorumluluklar:**
- REST API endpoint'leri sağlama
- WebSocket bağlantı yönetimi
- Kimlik doğrulama ve yetkilendirme
- Frontend ile backend arası veri köprüsü

**REST API Endpoints:**
```python
# Hesap ve Durum
GET  /api/status              # Bot durumu
POST /api/bot/start           # Bot'u başlat
POST /api/bot/stop            # Bot'u durdur
GET  /api/balance             # Hesap bakiyesi
GET  /api/account             # Hesap detayları

# Piyasa Verisi
GET  /api/market/price/:symbol        # Anlık fiyat
GET  /api/market/klines/:symbol       # Mum verileri
GET  /api/market/orderbook/:symbol    # Emir defteri

# İşlemler
POST /api/orders/manual       # Manuel emir
GET  /api/orders/history      # İşlem geçmişi
GET  /api/orders/:id          # Emir detayı

# Teknik Analiz
GET  /api/indicators/:symbol  # Güncel indikatörler
GET  /api/signals/history     # Sinyal geçmişi

# Ayarlar
GET  /api/config              # Mevcut ayarlar
PUT  /api/config              # Ayarları güncelle
```

**WebSocket Events:**
```python
# Server → Client
'market_update'     # Piyasa verisi güncelleme
'indicator_update'  # İndikatör güncelleme
'signal_generated'  # Yeni sinyal
'order_executed'    # Emir gerçekleşti
'balance_update'    # Bakiye güncelleme
'bot_status_change' # Bot durumu değişti
'error'             # Hata bildirimi

# Client → Server
'subscribe_symbol'   # Sembol takibine başla
'unsubscribe_symbol' # Sembol takibini durdur
'manual_order'       # Manuel emir gönder
'bot_control'        # Bot kontrolü (start/stop)
```

### 6. Web Frontend Components

**Ana Bileşenler:**

#### 6.1 Dashboard Component
```javascript
class Dashboard {
    // Genel bakış sayfası
    - Bot durumu kartı
    - Hızlı istatistikler (toplam bakiye, günlük P/L, işlem sayısı)
    - Mini grafik (fiyat trendi)
    - Son işlemler listesi
    - Aktif sinyaller
}
```

#### 6.2 Portfolio Component
```javascript
class Portfolio {
    // Portföy görünümü
    - Toplam portföy değeri (büyük gösterge)
    - Coin listesi (tablo)
    - Portföy dağılımı (pasta/halka grafik)
    - Performans grafikleri (çizgi grafik)
    - Hızlı işlem butonları
}
```

#### 6.3 Chart Component
```javascript
class ChartComponent {
    // İnteraktif grafik
    - Candlestick/çizgi grafik
    - Teknik indikatör overlay'leri
    - Zaman aralığı seçici
    - Zoom ve pan kontrolleri
    - Sinyal işaretleyicileri
    - Tooltip bilgileri
}
```

#### 6.4 Indicators Panel
```javascript
class IndicatorsPanel {
    // Teknik indikatörler paneli
    - RSI göstergesi (gauge)
    - MACD grafik
    - Bollinger Bands gösterge
    - Diğer indikatörler (kart formatında)
    - Konsensüs skoru göstergesi
}
```

#### 6.5 Trade History Component
```javascript
class TradeHistory {
    // İşlem geçmişi
    - İşlem tablosu (sayfalama ile)
    - Filtreleme (tarih, tip, coin)
    - Arama
    - Detay modal
    - Dışa aktarma butonu
    - Özet istatistikler
}
```

#### 6.6 Control Panel Component
```javascript
class ControlPanel {
    // Manuel kontrol paneli
    - Bot aktif/pasif toggle
    - Manuel AL/SAT butonları
    - Miktar girişi
    - Acil durdurma butonu
    - Mod seçici (Testnet/Live)
}
```

#### 6.7 Notification System
```javascript
class NotificationSystem {
    // Toast bildirimleri
    - Başarı bildirimleri (yeşil)
    - Hata bildirimleri (kırmızı)
    - Uyarı bildirimleri (sarı)
    - Bilgi bildirimleri (mavi)
    - Otomatik kapanma (5 saniye)
    - Manuel kapatma butonu
    - Maksimum 3 bildirim
}
```

**Frontend Veri Yönetimi:**
```javascript
// State Management (Vanilla JS)
class AppState {
    constructor() {
        this.botStatus = null;
        this.balance = null;
        this.currentPrice = null;
        this.indicators = null;
        this.trades = [];
        this.notifications = [];
    }
    
    update(key, value) {
        this[key] = value;
        this.notifySubscribers(key, value);
    }
    
    subscribe(key, callback) {
        // Observer pattern
    }
}
```

### 7. Database Schema

**Trades Table:**
```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(4) NOT NULL,  -- 'BUY' or 'SELL'
    order_type VARCHAR(10) NOT NULL,
    quantity REAL NOT NULL,
    price REAL NOT NULL,
    total_value REAL NOT NULL,
    status VARCHAR(20) NOT NULL,
    order_id VARCHAR(50),
    signal_confidence REAL,
    consensus_score REAL,
    error_message TEXT
);
```

**Signals Table:**
```sql
CREATE TABLE signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    signal_type VARCHAR(4) NOT NULL,  -- 'BUY', 'SELL', 'HOLD'
    confidence REAL NOT NULL,
    consensus_score REAL NOT NULL,
    rsi REAL,
    macd REAL,
    macd_signal REAL,
    macd_histogram REAL,
    bb_upper REAL,
    bb_middle REAL,
    bb_lower REAL,
    stoch_k REAL,
    stoch_d REAL,
    adx REAL,
    ema_20 REAL,
    ema_50 REAL,
    supertrend REAL,
    supertrend_direction VARCHAR(4),
    reason TEXT
);
```

**Bot Logs Table:**
```sql
CREATE TABLE bot_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    level VARCHAR(10) NOT NULL,  -- 'INFO', 'WARNING', 'ERROR'
    category VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    details TEXT
);
```

**Config Table:**
```sql
CREATE TABLE config (
    key VARCHAR(50) PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at INTEGER NOT NULL
);
```

## Veri Modelleri

### Backend Veri Modelleri

**BotConfig:**
```python
@dataclass
class BotConfig:
    # API Ayarları
    api_key: str
    api_secret: str
    testnet: bool = True
    
    # İşlem Ayarları
    symbol: str = 'BTCUSDT'
    interval: str = '5m'  # 1m, 5m, 15m, 1h, 4h, 1d
    trade_amount: float = 100.0  # USDT
    risk_percent: float = 2.0  # Portföyün %2'si
    
    # Strateji Ayarları
    rsi_period: int = 14
    rsi_overbought: float = 70.0
    rsi_oversold: float = 30.0
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    bb_period: int = 20
    bb_std: float = 2.0
    consensus_buy_threshold: float = 0.6
    consensus_sell_threshold: float = -0.6
    
    # İndikatör Ağırlıkları
    indicator_weights: Dict[str, float] = field(default_factory=lambda: {
        'rsi': 0.20,
        'macd': 0.20,
        'bollinger': 0.15,
        'stochastic': 0.15,
        'adx': 0.10,
        'ema': 0.10,
        'supertrend': 0.10
    })
    
    # Bot Ayarları
    cycle_interval: int = 5  # saniye
    max_api_requests_per_minute: int = 1000
    enable_auto_trading: bool = False
    
    # Risk Yönetimi (Gelecek)
    enable_stop_loss: bool = False
    stop_loss_percent: float = 2.0
    max_position_size: float = 1000.0
```

**BotStatus:**
```python
@dataclass
class BotStatus:
    is_running: bool
    is_active: bool  # Otomatik işlem aktif mi
    mode: str  # 'testnet' or 'live'
    current_symbol: str
    uptime_seconds: int
    last_cycle_time: int
    total_trades: int
    successful_trades: int
    failed_trades: int
    total_profit_loss: float
    api_connected: bool
    last_error: Optional[str]
```

### Frontend Veri Modelleri

**UI State:**
```javascript
const UIState = {
    theme: 'dark',  // 'dark' or 'light'
    activePage: 'dashboard',
    selectedSymbol: 'BTCUSDT',
    selectedTimeframe: '5m',
    chartType: 'candlestick',  // 'candlestick' or 'line'
    showIndicators: {
        rsi: true,
        macd: true,
        bollinger: true,
        ema: true
    },
    filters: {
        tradeType: 'all',  // 'all', 'buy', 'sell'
        dateRange: 'today'  // 'today', 'week', 'month', 'all'
    }
};
```

**Chart Data:**
```javascript
const ChartData = {
    klines: [
        {
            timestamp: 1234567890,
            open: 50000,
            high: 51000,
            low: 49500,
            close: 50500,
            volume: 1000
        }
    ],
    indicators: {
        rsi: [65.5, 64.2, ...],
        macd: {
            macd: [100, 105, ...],
            signal: [98, 102, ...],
            histogram: [2, 3, ...]
        },
        bollinger: {
            upper: [51000, 51200, ...],
            middle: [50000, 50100, ...],
            lower: [49000, 49000, ...]
        }
    },
    signals: [
        {
            timestamp: 1234567890,
            type: 'BUY',
            price: 50000
        }
    ]
};
```

### CSS Tasarım Sistemi

**Renk Paleti:**
```css
:root {
    /* Dark Theme */
    --bg-primary: #0b0e11;
    --bg-secondary: #161a1e;
    --bg-tertiary: #1e2329;
    --text-primary: #eaecef;
    --text-secondary: #b7bdc6;
    --text-tertiary: #848e9c;
    
    --color-success: #0ecb81;
    --color-danger: #f6465d;
    --color-warning: #f0b90b;
    --color-info: #3861fb;
    
    --border-color: #2b3139;
    --hover-bg: #2b3139;
    
    /* Light Theme */
    --bg-primary-light: #ffffff;
    --bg-secondary-light: #fafafa;
    --bg-tertiary-light: #f5f5f5;
    --text-primary-light: #1e2329;
    --text-secondary-light: #474d57;
    --text-tertiary-light: #848e9c;
    
    --border-color-light: #e6e8ea;
    --hover-bg-light: #f5f5f5;
}
```

**Tipografi:**
```css
:root {
    --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
                   'Helvetica Neue', Arial, sans-serif;
    --font-mono: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', 
                 Consolas, monospace;
    
    --font-size-xs: 0.75rem;    /* 12px */
    --font-size-sm: 0.875rem;   /* 14px */
    --font-size-base: 1rem;     /* 16px */
    --font-size-lg: 1.125rem;   /* 18px */
    --font-size-xl: 1.25rem;    /* 20px */
    --font-size-2xl: 1.5rem;    /* 24px */
    --font-size-3xl: 2rem;      /* 32px */
    
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
}
```

**Spacing:**
```css
:root {
    --spacing-xs: 0.25rem;   /* 4px */
    --spacing-sm: 0.5rem;    /* 8px */
    --spacing-md: 1rem;      /* 16px */
    --spacing-lg: 1.5rem;    /* 24px */
    --spacing-xl: 2rem;      /* 32px */
    --spacing-2xl: 3rem;     /* 48px */
}
```

**Bileşen Stilleri:**
```css
/* Card Component */
.card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: var(--spacing-lg);
    transition: all 0.2s ease;
}

.card:hover {
    border-color: var(--color-info);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Button Component */
.btn {
    padding: var(--spacing-sm) var(--spacing-lg);
    border-radius: 4px;
    font-weight: var(--font-weight-medium);
    transition: all 0.2s ease;
    cursor: pointer;
}

.btn-success {
    background: var(--color-success);
    color: white;
}

.btn-danger {
    background: var(--color-danger);
    color: white;
}

/* Toast Notification */
.toast {
    position: fixed;
    top: var(--spacing-lg);
    right: var(--spacing-lg);
    min-width: 300px;
    padding: var(--spacing-md);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        transform: translateX(400px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
```


## Araştırma Bulguları

### Binance API Entegrasyonu

Binance, REST API ve WebSocket API olmak üzere iki ana API türü sunar:

- **REST API**: Hesap bilgileri, emir gönderme, geçmiş veriler için kullanılır
- **WebSocket API**: Gerçek zamanlı fiyat akışı, emir defteri güncellemeleri için kullanılır
- **Rate Limits**: Saniyede 1200 istek (weight bazlı), IP bazlı kısıtlamalar
- **Testnet**: https://testnet.binance.vision/ - Gerçek para kullanmadan test ortamı

**Önerilen Kütüphane**: `python-binance` - Resmi olmayan ama yaygın kullanılan Python wrapper

### Teknik Analiz Kütüphaneleri

**TA-Lib** (Technical Analysis Library):
- C tabanlı, hızlı hesaplama
- 150+ teknik indikatör
- Kurulum biraz karmaşık (C bağımlılıkları)

**pandas-ta**:
- Pure Python, kolay kurulum
- 130+ indikatör
- Pandas DataFrame ile entegrasyon
- Daha yavaş ama yeterli performans

**Öneri**: Başlangıç için `pandas-ta`, performans kritikse `TA-Lib`

### Grafik Kütüphaneleri

**Chart.js**:
- Hafif (60KB minified)
- Kolay kullanım
- Candlestick için ek plugin gerekli
- Responsive ve animasyonlu

**TradingView Lightweight Charts**:
- Kripto/finans için özel tasarlanmış
- Yüksek performans
- Profesyonel görünüm
- Ücretsiz ve açık kaynak

**Plotly.js**:
- Çok özellikli
- İnteraktif
- Büyük dosya boyutu (3MB+)
- Candlestick desteği built-in

**Öneri**: TradingView Lightweight Charts - Kripto trading için en uygun

### WebSocket vs Polling

**WebSocket Avantajları**:
- Gerçek zamanlı veri akışı
- Düşük latency
- Sunucu kaynaklarını verimli kullanım
- Binance WebSocket API desteği

**Polling Dezavantajları**:
- Rate limit sorunları
- Yüksek latency
- Gereksiz API çağrıları

**Öneri**: WebSocket kullanımı (Binance WebSocket + Socket.IO frontend için)

### Güvenlik Önerileri

1. **API Anahtarları**: Çevre değişkenlerinde saklanmalı, asla kod içinde olmamalı
2. **IP Whitelist**: Binance'te IP kısıtlaması aktif edilmeli
3. **Withdrawal Disable**: API anahtarı oluştururken çekim izni verilmemeli
4. **HTTPS**: Tüm iletişim şifreli olmalı
5. **Rate Limiting**: Client-side rate limiting implementasyonu


## Doğruluk Özellikleri (Correctness Properties)

*Bir özellik (property), bir sistemin tüm geçerli yürütmelerinde doğru olması gereken bir karakteristik veya davranıştır - esasen, sistemin ne yapması gerektiği hakkında resmi bir ifadedir. Özellikler, insan tarafından okunabilir spesifikasyonlar ile makine tarafından doğrulanabilir doğruluk garantileri arasında köprü görevi görür.*

### Özellik 1: API Bağlantı Doğrulama

*Her* geçersiz API anahtarı çifti için, Market Data Collector bağlantı girişimi başarısız olmalı ve hata mesajı döndürmelidir.

**Doğrular: Gereksinim 1.2**

### Özellik 2: API Rate Limiting

*Her* API istek dizisi için, saniye başına gönderilen toplam istek sayısı 1200'ü aşmamalıdır.

**Doğrular: Gereksinim 1.4**

### Özellik 3: Piyasa Verisi Zaman Damgası

*Her* toplanan piyasa verisi için, veri mutlaka geçerli bir zaman damgası içermelidir.

**Doğrular: Gereksinim 2.5**

### Özellik 4: Teknik İndikatör Hesaplama

*Her* yeterli uzunlukta fiyat verisi dizisi için, Strategy Engine tüm yapılandırılmış teknik indikatörleri hesaplayabilmelidir.

**Doğrular: Gereksinim 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7**

### Özellik 5: Yetersiz Veri Durumu

*Her* yetersiz uzunlukta veri dizisi için, Strategy Engine hata vermeden indikatör hesaplamasını atlamalıdır.

**Doğrular: Gereksinim 3.8**

### Özellik 6: Konsensüs Skoru Aralığı

*Her* hesaplanan konsensüs skoru, -1.0 ile +1.0 arasında bir değer olmalıdır.

**Doğrular: Gereksinim 4.1**

### Özellik 7: Sinyal Üretimi - AL Sinyali

*Her* pozitif eşik değerini aşan konsensüs skoru için, Strategy Engine AL sinyali üretmelidir.

**Doğrular: Gereksinim 4.2**

### Özellik 8: Sinyal Üretimi - SAT Sinyali

*Her* negatif eşik değerini aşan konsensüs skoru için, Strategy Engine SAT sinyali üretmelidir.

**Doğrular: Gereksinim 4.3**

### Özellik 9: Sinyal Üretimi - BEKLİ Sinyali

*Her* eşik değerleri arasında kalan konsensüs skoru için, Strategy Engine BEKLİ sinyali üretmelidir.

**Doğrular: Gereksinim 4.4**

### Özellik 10: Sinyal Loglama

*Her* üretilen sinyal için, sistem sinyali zaman damgası ile birlikte Trade Log'a kaydetmelidir.

**Doğrular: Gereksinim 4.6**

### Özellik 11: Otomatik Emir - AL

*Her* AL sinyali ve aktif bot durumu için, Order Executor alım emri göndermelidir.

**Doğrular: Gereksinim 5.1**

### Özellik 12: Otomatik Emir - SAT

*Her* SAT sinyali ve aktif bot durumu için, Order Executor satım emri göndermelidir.

**Doğrular: Gereksinim 5.2**

### Özellik 13: Emir Loglama

*Her* gönderilen emir için, sistem emri Trade Log'a kaydetmelidir.

**Doğrular: Gereksinim 5.4**

### Özellik 14: Hata Loglama

*Her* başarısız emir için, sistem hata detaylarını Trade Log'a kaydetmelidir.

**Doğrular: Gereksinim 5.5**

### Özellik 15: Manuel Emir Yürütme

*Her* manuel AL veya SAT butonu tıklaması için, sistem belirtilen miktarda emir göndermelidir.

**Doğrular: Gereksinim 6.5, 6.6**

### Özellik 16: Pasif Bot Durumu

*Her* pasif bot durumunda, Order Executor otomatik emir göndermemelidir.

**Doğrular: Gereksinim 7.2**

### Özellik 17: Aktif Bot Durumu

*Her* aktif bot durumu ve geçerli sinyal için, Order Executor otomatik emir gönderebilmelidir.

**Doğrular: Gereksinim 7.3**

### Özellik 18: Bot Durum Değişikliği Loglama

*Her* bot durum değişikliği için, sistem değişikliği Trade Log'a kaydetmelidir.

**Doğrular: Gereksinim 7.5**

### Özellik 19: Testnet İzolasyonu

*Her* Testnet modunda çalışma durumunda, sistem gerçek bakiyeyi etkilememeli ve sadece Testnet API'yi kullanmalıdır.

**Doğrular: Gereksinim 8.2**

### Özellik 20: İşlem Geçmişi Kaydı

*Her* gerçekleştirilen işlem için, sistem tarih, saat, işlem türü, miktar, fiyat ve toplam değeri Trade Log'a kaydetmelidir.

**Doğrular: Gereksinim 9.1**

### Özellik 21: Sinyal Geçmişi Kaydı

*Her* üretilen sinyal için, sistem sinyali Trade Log'a kaydetmelidir.

**Doğrular: Gereksinim 9.2**

### Özellik 22: API Hata Kaydı

*Her* API hatası için, sistem hatayı Trade Log'a kaydetmelidir.

**Doğrular: Gereksinim 9.3**

### Özellik 23: Bakiye Güncellemesi

*Her* 5 saniyelik döngüde, sistem Binance API'den güncel bakiye bilgisini almalıdır.

**Doğrular: Gereksinim 10.4**

### Özellik 24: Yetersiz Bakiye Kontrolü

*Her* yetersiz bakiye durumunda, Order Executor emir göndermemeli ve uyarı vermelidir.

**Doğrular: Gereksinim 11.2**

### Özellik 25: Kritik İşlem Öncesi Doğrulama

*Her* kritik işlem öncesinde, sistem bakiye doğrulaması yapmalıdır.

**Doğrular: Gereksinim 11.5**


### Özellik 26: Responsive Tasarım

*Her* farklı ekran boyutu (mobil, tablet, masaüstü) için, Web Interface uygun şekilde görüntülenmeli ve kullanılabilir olmalıdır.

**Doğrular: Gereksinim 16.5**

### Özellik 27: Tema Değişimi

*Her* tema değişikliği (dark/light mode) için, tüm UI bileşenleri yeni temaya uygun renk paletini kullanmalıdır.

**Doğrular: Gereksinim 16.2**

### Özellik 28: Portföy Değeri Hesaplama

*Her* coin için, Portfolio View güncel fiyat × miktar formülü ile toplam değeri doğru hesaplamalıdır.

**Doğrular: Gereksinim 17.1**

### Özellik 29: Portföy Güncellemesi Animasyonu

*Her* portföy verisi güncellemesinde, Portfolio View yumuşak geçiş animasyonları ile güncellenmelidir.

**Doğrular: Gereksinim 17.8**

### Özellik 30: Hesap Durumu Görünürlüğü

*Her* zaman, Account Panel bot durumunu (Testnet/Live Trading) ve API bağlantı durumunu görünür şekilde göstermelidir.

**Doğrular: Gereksinim 18.2, 18.3**

### Özellik 31: Grafik Veri Güncellemesi

*Her* yeni piyasa verisi geldiğinde, Chart Component grafiği otomatik olarak güncellenmelidir.

**Doğrular: Gereksinim 19.7**

### Özellik 32: İşlem Filtreleme

*Her* uygulanan filtre için, Trade History View sadece filtre kriterlerine uyan işlemleri göstermelidir.

**Doğrular: Gereksinim 20.2**

### Özellik 33: Bildirim Görüntüleme

*Her* başarılı işlem için, Notification System başarı bildirimi göstermelidir.

**Doğrular: Gereksinim 21.1**

### Özellik 34: Bildirim Otomatik Kapanma

*Her* gösterilen bildirim için, sistem bildirimi 5 saniye sonra otomatik olarak kapatmalıdır.

**Doğrular: Gereksinim 21.6**

### Özellik 35: Maksimum Bildirim Sayısı

*Her* zaman, ekranda maksimum 3 bildirim gösterilmelidir.

**Doğrular: Gereksinim 21.8**

### Özellik 36: Aktif Sayfa Vurgulama

*Her* sayfa değişikliğinde, Navigation Bar aktif sayfayı görsel olarak vurgulamalıdır.

**Doğrular: Gereksinim 22.3**


## Hata Yönetimi

### Hata Kategorileri

**1. API Hataları**
- Bağlantı hataları (network timeout, connection refused)
- Kimlik doğrulama hataları (invalid API key, signature mismatch)
- Rate limiting hataları (429 Too Many Requests)
- Binance sunucu hataları (5xx errors)

**Yönetim Stratejisi:**
```python
def handle_api_error(error):
    if isinstance(error, ConnectionError):
        # Exponential backoff ile yeniden deneme
        retry_with_backoff(max_retries=3, base_delay=1)
    elif isinstance(error, AuthenticationError):
        # Bot'u durdur, kullanıcıyı bilgilendir
        bot.emergency_stop()
        notify_user("API anahtarları geçersiz")
    elif isinstance(error, RateLimitError):
        # Rate limit süresi kadar bekle
        wait_for_rate_limit_reset()
    else:
        # Genel hata, logla ve devam et
        log_error(error)
```

**2. Veri Doğrulama Hataları**
- Eksik veya bozuk piyasa verisi
- Geçersiz indikatör değerleri
- Beklenmeyen veri formatı

**Yönetim Stratejisi:**
```python
def validate_market_data(data):
    if not data or len(data) < MIN_DATA_POINTS:
        log_warning("Yetersiz veri, döngü atlanıyor")
        return False
    
    if any(d.close <= 0 for d in data):
        log_error("Geçersiz fiyat verisi")
        return False
    
    return True
```

**3. İşlem Hataları**
- Yetersiz bakiye
- Minimum emir miktarı altında
- Piyasa kapalı
- Emir reddedildi

**Yönetim Stratejisi:**
```python
def handle_order_error(error, order):
    if error.code == 'INSUFFICIENT_BALANCE':
        log_warning("Yetersiz bakiye")
        notify_user("Yetersiz bakiye", level='warning')
        return None
    elif error.code == 'MIN_NOTIONAL':
        log_warning("Minimum emir miktarı altında")
        return None
    else:
        log_error(f"Emir hatası: {error}")
        trade_log.record_failed_order(order, error)
        return None
```

**4. Sistem Hataları**
- Veritabanı hataları
- Bellek yetersizliği
- Beklenmeyen exception'lar

**Yönetim Stratejisi:**
```python
def handle_system_error(error):
    log_critical(f"Kritik sistem hatası: {error}")
    bot.emergency_stop()
    notify_admin("Sistem hatası, bot durduruldu")
    
    # Graceful shutdown
    cleanup_resources()
    save_state()
```

### Hata Loglama

**Log Seviyeleri:**
- **DEBUG**: Detaylı debug bilgileri
- **INFO**: Normal işlem bilgileri
- **WARNING**: Uyarılar (işlem devam eder)
- **ERROR**: Hatalar (işlem başarısız)
- **CRITICAL**: Kritik hatalar (sistem durdurulur)

**Log Formatı:**
```python
{
    "timestamp": 1234567890,
    "level": "ERROR",
    "category": "API",
    "message": "Binance API bağlantı hatası",
    "details": {
        "error_code": "ECONNREFUSED",
        "endpoint": "/api/v3/ticker/price",
        "retry_count": 2
    }
}
```

### Güvenlik Önlemleri

**1. API Anahtarı Güvenliği**
```python
# Çevre değişkenlerinden oku
API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')

# Asla logla
def log_request(request):
    safe_request = request.copy()
    safe_request.pop('api_key', None)
    safe_request.pop('signature', None)
    logger.info(safe_request)
```

**2. Input Validation**
```python
def validate_order_input(symbol, quantity, price=None):
    # Symbol validation
    if not re.match(r'^[A-Z]{6,10}$', symbol):
        raise ValueError("Geçersiz sembol")
    
    # Quantity validation
    if quantity <= 0:
        raise ValueError("Miktar pozitif olmalı")
    
    # Price validation (limit order için)
    if price is not None and price <= 0:
        raise ValueError("Fiyat pozitif olmalı")
```

**3. Rate Limiting**
```python
class RateLimiter:
    def __init__(self, max_requests_per_minute=1000):
        self.max_requests = max_requests_per_minute
        self.requests = []
    
    def check_limit(self):
        now = time.time()
        # Son 1 dakikadaki istekleri filtrele
        self.requests = [r for r in self.requests if now - r < 60]
        
        if len(self.requests) >= self.max_requests:
            raise RateLimitError("Rate limit aşıldı")
        
        self.requests.append(now)
```

**4. Emergency Stop**
```python
def emergency_stop():
    """Acil durum durdurma - tüm işlemleri durdur"""
    bot.set_active(False)
    bot.stop()
    
    # Açık pozisyonları kapat (opsiyonel)
    if config.close_positions_on_emergency:
        close_all_positions()
    
    # Durumu kaydet
    save_bot_state()
    
    # Bildirimleri gönder
    notify_user("Acil durdurma aktif", level='critical')
    notify_admin("Bot acil durdurma yapıldı")
```


## Test Stratejisi

### Test Yaklaşımı

Sistem, hem birim testleri (unit tests) hem de özellik tabanlı testler (property-based tests) kullanarak kapsamlı bir şekilde test edilecektir. Bu iki yaklaşım birbirini tamamlar:

- **Birim Testleri**: Belirli örnekler, kenar durumları ve hata koşullarını doğrular
- **Özellik Tabanlı Testler**: Tüm girdiler için evrensel özellikleri doğrular

### Özellik Tabanlı Test Konfigürasyonu

**Test Kütüphanesi**: Hypothesis (Python için)

**Konfigürasyon:**
```python
from hypothesis import given, settings, strategies as st

# Her test minimum 100 iterasyon çalıştırılacak
@settings(max_examples=100)
@given(
    api_key=st.text(min_size=32, max_size=64),
    api_secret=st.text(min_size=32, max_size=64)
)
def test_property_1_invalid_api_keys(api_key, api_secret):
    """
    Feature: crypto-trading-automation, Property 1:
    Her geçersiz API anahtarı çifti için, Market Data Collector 
    bağlantı girişimi başarısız olmalı ve hata mesajı döndürmelidir.
    """
    # Geçersiz anahtarlar kullan
    collector = MarketDataCollector(api_key, api_secret, testnet=True)
    
    result = collector.connect()
    
    assert result is False
    assert collector.last_error is not None
```

**Test Etiketleme:**
Her özellik tabanlı test, tasarım dokümanındaki özelliğe referans verecek şekilde etiketlenecektir:

```python
# Feature: crypto-trading-automation, Property {number}: {property_text}
```

### Birim Test Stratejisi

**Test Kütüphanesi**: pytest

**Test Organizasyonu:**
```
tests/
├── unit/
│   ├── test_market_data_collector.py
│   ├── test_strategy_engine.py
│   ├── test_order_executor.py
│   ├── test_trading_bot.py
│   └── test_indicators.py
├── integration/
│   ├── test_api_integration.py
│   ├── test_database.py
│   └── test_websocket.py
├── property/
│   ├── test_properties_api.py
│   ├── test_properties_signals.py
│   ├── test_properties_orders.py
│   └── test_properties_ui.py
└── e2e/
    ├── test_full_cycle.py
    └── test_ui_workflow.py
```

**Örnek Birim Testleri:**

```python
# tests/unit/test_strategy_engine.py
import pytest
from strategy_engine import StrategyEngine, IndicatorValues

def test_consensus_score_buy_signal():
    """AL sinyali üretimi - pozitif konsensüs skoru"""
    engine = StrategyEngine(config)
    
    # Güçlü AL sinyali veren indikatörler
    indicators = IndicatorValues(
        rsi=25.0,  # Oversold
        macd=(100, 80, 20),  # Pozitif histogram
        bollinger=(51000, 50000, 49000),
        stochastic=(20, 25),
        adx=30,
        ema={20: 49500, 50: 49000},
        supertrend=(49000, 'up'),
        timestamp=1234567890
    )
    
    signal = engine.generate_signal(indicators)
    
    assert signal.signal_type == 'BUY'
    assert signal.consensus_score > 0.6
    assert signal.confidence > 0.5

def test_consensus_score_sell_signal():
    """SAT sinyali üretimi - negatif konsensüs skoru"""
    engine = StrategyEngine(config)
    
    # Güçlü SAT sinyali veren indikatörler
    indicators = IndicatorValues(
        rsi=75.0,  # Overbought
        macd=(-100, -80, -20),  # Negatif histogram
        bollinger=(51000, 50000, 49000),
        stochastic=(80, 75),
        adx=30,
        ema={20: 50500, 50: 51000},
        supertrend=(51000, 'down'),
        timestamp=1234567890
    )
    
    signal = engine.generate_signal(indicators)
    
    assert signal.signal_type == 'SELL'
    assert signal.consensus_score < -0.6
    assert signal.confidence > 0.5

def test_insufficient_data_handling():
    """Yetersiz veri durumunda hata vermeme"""
    engine = StrategyEngine(config)
    
    # Çok az veri
    short_data = [Kline(...) for _ in range(5)]
    
    # Hata vermemeli
    indicators = engine.calculate_indicators(short_data)
    
    # İndikatörler None veya varsayılan değer olmalı
    assert indicators is None or indicators.rsi is None
```

**Örnek Entegrasyon Testleri:**

```python
# tests/integration/test_api_integration.py
import pytest
from market_data_collector import MarketDataCollector

@pytest.fixture
def testnet_collector():
    """Testnet API bağlantısı"""
    api_key = os.getenv('TESTNET_API_KEY')
    api_secret = os.getenv('TESTNET_API_SECRET')
    return MarketDataCollector(api_key, api_secret, testnet=True)

def test_get_ticker_price(testnet_collector):
    """Anlık fiyat alma"""
    price = testnet_collector.get_ticker_price('BTCUSDT')
    
    assert price > 0
    assert isinstance(price, float)

def test_get_klines(testnet_collector):
    """Mum verisi alma"""
    klines = testnet_collector.get_klines('BTCUSDT', '5m', 100)
    
    assert len(klines) == 100
    assert all(k.close > 0 for k in klines)
    assert all(k.high >= k.low for k in klines)

def test_rate_limiting(testnet_collector):
    """Rate limiting kontrolü"""
    # 1200'den fazla istek göndermeye çalış
    with pytest.raises(RateLimitError):
        for _ in range(1300):
            testnet_collector.get_ticker_price('BTCUSDT')
```

**Örnek Özellik Tabanlı Testler:**

```python
# tests/property/test_properties_signals.py
from hypothesis import given, settings, strategies as st
from hypothesis.strategies import floats, lists

@settings(max_examples=100)
@given(
    rsi=floats(min_value=0, max_value=100),
    macd=floats(min_value=-1000, max_value=1000),
    price=floats(min_value=1, max_value=100000)
)
def test_property_6_consensus_score_range(rsi, macd, price):
    """
    Feature: crypto-trading-automation, Property 6:
    Her hesaplanan konsensüs skoru, -1.0 ile +1.0 arasında bir değer olmalıdır.
    """
    engine = StrategyEngine(config)
    
    indicators = create_indicators(rsi=rsi, macd=macd, price=price)
    consensus_score = engine.get_consensus_score(indicators)
    
    assert -1.0 <= consensus_score <= 1.0

@settings(max_examples=100)
@given(
    data=lists(
        st.builds(Kline,
            timestamp=st.integers(min_value=1000000000, max_value=2000000000),
            open=floats(min_value=1, max_value=100000),
            high=floats(min_value=1, max_value=100000),
            low=floats(min_value=1, max_value=100000),
            close=floats(min_value=1, max_value=100000),
            volume=floats(min_value=0, max_value=1000000)
        ),
        min_size=50,
        max_size=200
    )
)
def test_property_4_indicator_calculation(data):
    """
    Feature: crypto-trading-automation, Property 4:
    Her yeterli uzunlukta fiyat verisi dizisi için, Strategy Engine 
    tüm yapılandırılmış teknik indikatörleri hesaplayabilmelidir.
    """
    engine = StrategyEngine(config)
    
    indicators = engine.calculate_indicators(data)
    
    assert indicators is not None
    assert indicators.rsi is not None
    assert indicators.macd is not None
    assert indicators.bollinger is not None

@settings(max_examples=100)
@given(
    balance=floats(min_value=0, max_value=10),
    order_amount=floats(min_value=10, max_value=1000)
)
def test_property_24_insufficient_balance(balance, order_amount):
    """
    Feature: crypto-trading-automation, Property 24:
    Her yetersiz bakiye durumunda, Order Executor emir göndermemeli 
    ve uyarı vermelidir.
    """
    executor = OrderExecutor(api_key, api_secret, testnet=True)
    
    # Bakiye yetersizse
    if balance < order_amount:
        result = executor.place_market_order('BTCUSDT', 'BUY', order_amount)
        
        assert result is None
        assert executor.last_warning == 'INSUFFICIENT_BALANCE'
```

### Frontend Test Stratejisi

**Test Kütüphaneleri:**
- Jest (JavaScript test framework)
- Testing Library (DOM testing)
- Cypress (E2E testing)

**Örnek Frontend Testleri:**

```javascript
// tests/frontend/test_portfolio.test.js
describe('Portfolio Component', () => {
    test('Property 28: Portföy değeri hesaplama', () => {
        const coins = [
            { symbol: 'BTC', amount: 0.5, price: 50000 },
            { symbol: 'ETH', amount: 2.0, price: 3000 }
        ];
        
        const portfolio = new Portfolio(coins);
        const totalValue = portfolio.calculateTotalValue();
        
        expect(totalValue).toBe(31000); // 0.5*50000 + 2.0*3000
    });
    
    test('Property 26: Responsive tasarım', () => {
        const viewports = [
            { width: 375, height: 667 },   // Mobile
            { width: 768, height: 1024 },  // Tablet
            { width: 1920, height: 1080 }  // Desktop
        ];
        
        viewports.forEach(viewport => {
            cy.viewport(viewport.width, viewport.height);
            cy.visit('/portfolio');
            
            // Sayfa kullanılabilir olmalı
            cy.get('.portfolio-container').should('be.visible');
            cy.get('.coin-list').should('be.visible');
        });
    });
});

// tests/frontend/test_notifications.test.js
describe('Notification System', () => {
    test('Property 34: Bildirim otomatik kapanma', (done) => {
        const notification = new Notification('Test', 'success');
        notification.show();
        
        expect(document.querySelector('.toast')).toBeInTheDocument();
        
        // 5 saniye sonra kapanmalı
        setTimeout(() => {
            expect(document.querySelector('.toast')).not.toBeInTheDocument();
            done();
        }, 5100);
    });
    
    test('Property 35: Maksimum bildirim sayısı', () => {
        // 5 bildirim göstermeye çalış
        for (let i = 0; i < 5; i++) {
            new Notification(`Test ${i}`, 'info').show();
        }
        
        // Sadece 3 bildirim görünmeli
        const toasts = document.querySelectorAll('.toast');
        expect(toasts.length).toBe(3);
    });
});
```

### Test Coverage Hedefleri

- **Birim Test Coverage**: Minimum %80
- **Entegrasyon Test Coverage**: Minimum %70
- **Özellik Tabanlı Test**: Tüm kritik özellikler için 100 iterasyon
- **E2E Test**: Ana kullanıcı akışları için tam coverage

### Continuous Integration

**CI Pipeline:**
```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest hypothesis pytest-cov
      
      - name: Run unit tests
        run: pytest tests/unit --cov=src --cov-report=xml
      
      - name: Run property tests
        run: pytest tests/property --hypothesis-show-statistics
      
      - name: Run integration tests
        run: pytest tests/integration
        env:
          TESTNET_API_KEY: ${{ secrets.TESTNET_API_KEY }}
          TESTNET_API_SECRET: ${{ secrets.TESTNET_API_SECRET }}
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

### Manuel Test Senaryoları

**Senaryo 1: Tam İşlem Döngüsü**
1. Bot'u başlat (Testnet modunda)
2. Piyasa verilerinin geldiğini doğrula
3. İndikatörlerin hesaplandığını doğrula
4. Sinyal üretildiğini doğrula
5. Emir gönderildiğini doğrula
6. Trade log'a kaydedildiğini doğrula

**Senaryo 2: Manuel İşlem**
1. Manuel kontrol paneline git
2. Miktar gir
3. AL butonuna tıkla
4. Emrin gönderildiğini doğrula
5. Bakiyenin güncellendiğini doğrula
6. Bildirim gösterildiğini doğrula

**Senaryo 3: Hata Durumları**
1. API anahtarlarını geçersiz yap
2. Bot'u başlatmaya çalış
3. Hata mesajının gösterildiğini doğrula
4. Bot'un durduğunu doğrula
5. Log'a kaydedildiğini doğrula

**Senaryo 4: UI Responsive Test**
1. Farklı cihazlardan eriş (mobil, tablet, desktop)
2. Tüm sayfaların düzgün göründüğünü doğrula
3. Grafiklerin responsive olduğunu doğrula
4. Navigasyonun çalıştığını doğrula


## Uygulama Notları

### Geliştirme Aşamaları

**Faz 1: Temel Altyapı (1-2 hafta)**
- Binance API entegrasyonu
- Market data collector implementasyonu
- Veritabanı şeması oluşturma
- Temel logging sistemi

**Faz 2: Strateji Motoru (2-3 hafta)**
- Teknik indikatör hesaplama
- Konsensüs skoru algoritması
- Sinyal üretimi
- Birim testler

**Faz 3: İşlem Yürütme (1-2 hafta)**
- Order executor implementasyonu
- Bakiye yönetimi
- Hata yönetimi
- Testnet entegrasyonu

**Faz 4: Backend API (1-2 hafta)**
- REST API endpoints
- WebSocket implementasyonu
- Kimlik doğrulama
- API testleri

**Faz 5: Frontend Geliştirme (3-4 hafta)**
- Temel layout ve navigasyon
- Dashboard ve portföy görünümü
- Grafik entegrasyonu
- İndikatör panelleri
- İşlem geçmişi
- Bildirim sistemi
- Responsive tasarım

**Faz 6: Entegrasyon ve Test (1-2 hafta)**
- End-to-end testler
- Performans optimizasyonu
- Güvenlik testleri
- Kullanıcı kabul testleri

**Faz 7: Deployment ve İzleme (1 hafta)**
- Production deployment
- Monitoring kurulumu
- Dokümantasyon
- Kullanıcı eğitimi

### Performans Optimizasyonları

**1. Veri Önbellekleme**
```python
from functools import lru_cache
import redis

# Redis cache
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_price(symbol, ttl=5):
    """Fiyatı cache'den al, yoksa API'den çek"""
    cache_key = f"price:{symbol}"
    cached = cache.get(cache_key)
    
    if cached:
        return float(cached)
    
    price = api.get_ticker_price(symbol)
    cache.setex(cache_key, ttl, price)
    return price
```

**2. Asenkron İşlemler**
```python
import asyncio
import aiohttp

async def fetch_multiple_symbols(symbols):
    """Birden fazla sembol için paralel veri çekme"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_symbol(session, symbol) for symbol in symbols]
        return await asyncio.gather(*tasks)

async def fetch_symbol(session, symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    async with session.get(url) as response:
        return await response.json()
```

**3. Veritabanı İndeksleme**
```sql
-- Sık sorgulanan alanlar için indeksler
CREATE INDEX idx_trades_timestamp ON trades(timestamp);
CREATE INDEX idx_trades_symbol ON trades(symbol);
CREATE INDEX idx_signals_timestamp ON signals(timestamp);
CREATE INDEX idx_signals_symbol ON signals(symbol);

-- Composite index
CREATE INDEX idx_trades_symbol_timestamp ON trades(symbol, timestamp);
```

**4. Frontend Optimizasyonu**
```javascript
// Debounce ile gereksiz render'ları önleme
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Grafik güncellemelerini debounce et
const updateChart = debounce((data) => {
    chart.update(data);
}, 500);

// Virtual scrolling için büyük listeler
class VirtualList {
    constructor(items, itemHeight, containerHeight) {
        this.items = items;
        this.itemHeight = itemHeight;
        this.visibleCount = Math.ceil(containerHeight / itemHeight);
    }
    
    getVisibleItems(scrollTop) {
        const startIndex = Math.floor(scrollTop / this.itemHeight);
        return this.items.slice(startIndex, startIndex + this.visibleCount);
    }
}
```

### Deployment

**Docker Compose Yapılandırması:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - BINANCE_API_KEY=${BINANCE_API_KEY}
      - BINANCE_API_SECRET=${BINANCE_API_SECRET}
      - DATABASE_URL=postgresql://user:pass@db:5432/trading
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
  
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
  
  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=trading
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
  
  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

**Nginx Konfigürasyonu:**
```nginx
server {
    listen 80;
    server_name trading-bot.example.com;
    
    # Frontend
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
    
    # WebSocket
    location /socket.io {
        proxy_pass http://backend:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Monitoring ve Logging

**Prometheus Metrics:**
```python
from prometheus_client import Counter, Histogram, Gauge

# Metrikler
api_requests_total = Counter('api_requests_total', 'Total API requests', ['endpoint', 'status'])
order_execution_time = Histogram('order_execution_seconds', 'Order execution time')
active_positions = Gauge('active_positions', 'Number of active positions')
bot_status = Gauge('bot_status', 'Bot status (1=active, 0=inactive)')

# Kullanım
@api_requests_total.labels(endpoint='/api/orders', status='success').inc()
with order_execution_time.time():
    execute_order()
```

**Structured Logging:**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "order_executed",
    order_id="12345",
    symbol="BTCUSDT",
    side="BUY",
    quantity=0.001,
    price=50000,
    total_value=50
)
```

### Güvenlik Kontrol Listesi

- [ ] API anahtarları çevre değişkenlerinde
- [ ] HTTPS kullanımı
- [ ] Rate limiting implementasyonu
- [ ] Input validation
- [ ] SQL injection koruması
- [ ] XSS koruması
- [ ] CSRF token kullanımı
- [ ] Güvenli session yönetimi
- [ ] Düzenli güvenlik güncellemeleri
- [ ] Penetrasyon testleri

### Bakım ve İzleme

**Günlük Kontroller:**
- Bot durumu kontrolü
- API bağlantı durumu
- Hata logları incelemesi
- Performans metrikleri

**Haftalık Kontroller:**
- Veritabanı boyutu
- Log dosyası temizliği
- Backup kontrolü
- Güvenlik güncellemeleri

**Aylık Kontroller:**
- Strateji performans analizi
- Sistem kaynak kullanımı
- Maliyet analizi
- Kullanıcı geri bildirimleri

## Sonuç

Bu tasarım dokümanı, Kripto Ticaret Otomasyon Sistemi'nin teknik mimarisini, bileşenlerini, veri modellerini ve test stratejisini detaylı olarak açıklamaktadır. Sistem, modern web teknolojileri kullanarak profesyonel bir kullanıcı arayüzü sunarken, güvenilir ve performanslı bir backend altyapısı üzerine inşa edilmiştir.

Özellik tabanlı testler ve kapsamlı birim testler ile desteklenen bu tasarım, sistemin doğruluğunu ve güvenilirliğini garanti altına alır. Aşamalı geliştirme yaklaşımı, testnet'ten canlı işleme geçişi güvenli bir şekilde yönetir.

