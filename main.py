import os, time, threading, hmac, hashlib, urllib.parse
import requests
import pandas as pd
import pandas_ta as ta
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from functools import wraps
from flask_socketio import SocketIO
from dotenv import load_dotenv
from datetime import datetime
import database as db

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")

# SocketIO configuration - simple setup to avoid session issues
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode='threading',
    logger=False,
    engineio_logger=False,
    manage_session=False,
    cookie=None,  # Disable cookie-based sessions
    ping_timeout=60,
    ping_interval=25
)

# Login bilgileri
LOGIN_USERNAME = os.getenv("LOGIN_USERNAME", "admin")
LOGIN_PASSWORD = os.getenv("LOGIN_PASSWORD", "12345")

# ── CONFIG ────────────────────────────────────────────────────────────────────
API_KEY    = os.getenv("BINANCE_API_KEY", "")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")
BASE       = "https://testnet.binance.vision"
COINGECKO  = "https://api.coingecko.com/api/v3"

SYMBOL      = "BTCUSDT"
SMA_FAST    = 5
SMA_SLOW    = 9
USE_OTT     = False  # True yaparsanız OTT kullanır, False ise SMA
AUTO_TRADE  = True
LEVERAGE    = 1

# Veritabanını başlat
db.init_database()

# Bellekteki veriler (hızlı erişim için)
portfolio      = {"USDT": 0.0}  # Dinamik olarak coinler eklenecek
trade_history  = []  # Veritabanından yüklenecek
open_orders    = []  # Veritabanından yüklenecek
signal_history = []  # Veritabanından yüklenecek
last_signal    = ""
starting_value = 0.0  # Veritabanından yüklenecek

# Top 20 coin listesi (CoinGecko id → sembol)
TOP_COINS = [
    {"id": "bitcoin",      "symbol": "BTC",  "pair": "BTCUSDT"},
    {"id": "ethereum",     "symbol": "ETH",  "pair": "ETHUSDT"},
    {"id": "binancecoin",  "symbol": "BNB",  "pair": "BNBUSDT"},
    {"id": "solana",       "symbol": "SOL",  "pair": "SOLUSDT"},
    {"id": "ripple",       "symbol": "XRP",  "pair": "XRPUSDT"},
    {"id": "dogecoin",     "symbol": "DOGE", "pair": "DOGEUSDT"},
    {"id": "cardano",      "symbol": "ADA",  "pair": "ADAUSDT"},
    {"id": "avalanche-2",  "symbol": "AVAX", "pair": "AVAXUSDT"},
    {"id": "chainlink",    "symbol": "LINK", "pair": "LINKUSDT"},
    {"id": "polkadot",     "symbol": "DOT",  "pair": "DOTUSDT"},
    {"id": "tron",         "symbol": "TRX",  "pair": "TRXUSDT"},
    {"id": "litecoin",     "symbol": "LTC",  "pair": "LTCUSDT"},
    {"id": "uniswap",      "symbol": "UNI",  "pair": "UNIUSDT"},
    {"id": "stellar",      "symbol": "XLM",  "pair": "XLMUSDT"},
    {"id": "monero",       "symbol": "XMR",  "pair": "XMRUSDT"},
]


# ── SMA FONKSİYONU ───────────────────────────────────────────────────────────
def safe_sma(df_close, length):
    """Basit Hareketli Ortalama (SMA) hesaplar"""
    try:
        sma = ta.sma(df_close, length=length)
        return round(float(sma.iloc[-1]), 2) if sma is not None else 0
    except Exception as e:
        print(f"[SMA{length} HATA] {e}")
        return 0
# ── LOGIN DECORATOR ───────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ── HTTP HELPERS ──────────────────────────────────────────────────────────────
def _sign(params):
    params["timestamp"] = int(time.time() * 1000)
    qs  = urllib.parse.urlencode(params)
    sig = hmac.new(SECRET_KEY.encode(), qs.encode(), hashlib.sha256).hexdigest()
    return qs + "&signature=" + sig

def api_get(path, params=None):
    try:
        p   = params or {}
        url = f"{BASE}{path}?{_sign(p)}"
        return requests.get(url, headers={"X-MBX-APIKEY": API_KEY}, timeout=10)
    except Exception as e:
        print(f"[GET ERR] {e}"); return None

def api_post(path, params=None):
    try:
        p   = params or {}
        url = f"{BASE}{path}?{_sign(p)}"
        return requests.post(url, headers={"X-MBX-APIKEY": API_KEY}, timeout=10)
    except Exception as e:
        print(f"[POST ERR] {e}"); return None

def pub_get(path, params=None):
    try:
        return requests.get(f"{BASE}{path}", params=params, timeout=10)
    except Exception as e:
        print(f"[PUB ERR] {e}"); return None

def cg_get(path, params=None):
    try:
        return requests.get(f"{COINGECKO}{path}", params=params, timeout=15)
    except Exception as e:
        print(f"[CG ERR] {e}"); return None


# ── BALANCE ───────────────────────────────────────────────────────────────────
def fetch_balance():
    """Bakiyeyi çeker ve tüm coinleri döndürür"""
    r = api_get("/api/v3/account")
    if r and r.status_code == 200:
        bals = {b["asset"]: float(b["free"]) for b in r.json().get("balances", []) if float(b["free"]) > 0}
        # En azından USDT ve aktif SYMBOL'ün coin'ini ekle
        if "USDT" not in bals:
            bals["USDT"] = 0.0
        coin = SYMBOL.replace('USDT', '')
        if coin not in bals:
            bals[coin] = 0.0
        return bals
    print(f"[BAKİYE HATA] {r.status_code if r else 'no resp'}: {r.text if r else ''}")
    return None

def fetch_orderbook(symbol=None):
    """Orderbook'u belirtilen symbol için çeker, yoksa global SYMBOL kullanır"""
    sym = symbol or SYMBOL
    r   = pub_get("/api/v3/depth", {"symbol": sym, "limit": 10})
    return r.json() if r and r.status_code == 200 else {"bids": [], "asks": []}


# ── PLACE ORDER ───────────────────────────────────────────────────────────────
def place_order(side, order_type, quantity, limit_price=None, symbol=None):
    """Emir yerleştirir. Symbol belirtilmezse global SYMBOL kullanılır."""
    sym = symbol or SYMBOL
    quantity = round(round(quantity / 0.001) * 0.001, 3)
    if quantity < 0.001:
        return None, "Miktar çok küçük (min 0.001 BTC)"
    params = {
        "symbol":   sym,
        "side":     side,
        "type":     order_type,
        "quantity": f"{quantity:.3f}",
    }
    if order_type == "LIMIT" and limit_price:
        params["timeInForce"] = "GTC"
        params["price"]       = f"{limit_price:.2f}"
    r = api_post("/api/v3/order", params)
    if r is None:
        return None, "Sunucuya ulaşılamadı"
    if r.status_code == 200:
        return r.json(), None
    try:
        err = r.json().get("msg", r.text)
    except Exception:
        err = r.text
    return None, err


# ── LOG TRADE ─────────────────────────────────────────────────────────────────
def log_trade(side, otype, qty, price, value):
    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "side": side, "type": otype,
        "qty":  qty,  "price": price, "value": value,
        "symbol": SYMBOL
    }
    
    # Veritabanına kaydet
    db.save_trade(entry)
    
    # Belleğe ekle (hızlı erişim için)
    trade_history.insert(0, entry)
    if len(trade_history) > 50:
        trade_history.pop()
    
    icon = "🟢" if side == "BUY" else "🔴"
    msg  = f"{icon} {side} {otype} | {qty:.3f} BTC @ ${price:,.2f} | ${value:,.2f}"
    socketio.emit('order_status',         {"msg": msg, "type": "success"})
    socketio.emit('trade_history_update', trade_history[:20])
    socketio.emit('portfolio_update',     portfolio)


# ── AUTO BUY / SELL (SMA STRATEJİSİ) ─────────────────────────────────────────
def auto_buy(price):
    """Bakiyenin %95'i ile market fiyatından BTC AL"""
    global portfolio
    usdt = portfolio["USDT"] * 0.95   # %95 kullan, %5 komisyon için rezerv
    if usdt < 10:
        socketio.emit('log_update', {"msg": "⚠️ Oto-alım: Yetersiz USDT bakiye"}); return
    qty = round(usdt / price, 6)
    order, err = place_order("BUY", "MARKET", qty)
    if err:
        socketio.emit('log_update', {"msg": f"⚠️ Oto-alım: {err}"}); return
    time.sleep(0.8)
    fresh = fetch_balance()
    if fresh: portfolio.update(fresh)
    log_trade("BUY", "MARKET", qty, price, usdt)
    socketio.emit('log_update', {"msg": f"🟢 SMA AL | {qty:.4f} BTC @ ${price:,.2f} | ${usdt:,.2f} USDT"})

def auto_sell(price):
    """Tüm BTC'yi market fiyatından SAT"""
    global portfolio
    coin = SYMBOL.replace('USDT', '')
    qty = round(portfolio.get(coin, 0) * 0.999, 6)
    if qty < 0.001:
        socketio.emit('log_update', {"msg": f"⚠️ Oto-satım: Satılacak {coin} yok"}); return
    order, err = place_order("SELL", "MARKET", qty)
    if err:
        socketio.emit('log_update', {"msg": f"⚠️ Oto-satım: {err}"}); return
    time.sleep(0.8)
    fresh = fetch_balance()
    if fresh: portfolio.update(fresh)
    value = round(qty * price, 2)
    log_trade("SELL", "MARKET", qty, price, value)
    socketio.emit('log_update', {"msg": f"🔴 SMA SAT | {qty:.4f} {coin} @ ${price:,.2f} → ${value:,.2f} USDT"})


# ── OTT İNDİKATÖRÜ ──────────────────────────────────────────────────────────
def calc_ott(df_high, df_low, df_close, percent=2, coeff=0.5, length=2):
    """
    OTT (Optimized Trend Tracker) indikatörü
    Kaynak: Anıl Özekşi - TradingView
    """
    try:
        n = len(df_close)
        if n < length + 5:
            return [], 'neutral'
        
        closes = df_close.values.astype(float)
        highs = df_high.values.astype(float)
        lows = df_low.values.astype(float)
        
        # VAR (Volatility Adjusted Range) hesapla
        var_array = [0]
        for i in range(1, n):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
            var_array.append(tr)
        
        # Moving Average of VAR
        mav = []
        for i in range(n):
            if i < length:
                mav.append(var_array[i])
            else:
                mav.append(sum(var_array[i-length+1:i+1]) / length)
        
        # Alpha hesapla
        alpha = [coeff * v for v in mav]
        
        # OTT hesapla
        ott_values = []
        long_stop = closes[0] - alpha[0] * percent / 100
        short_stop = closes[0] + alpha[0] * percent / 100
        direction = 1
        
        for i in range(n):
            src = closes[i]
            fark = alpha[i] * percent / 100
            
            if i == 0:
                ott_values.append(src)
            else:
                # Long stop
                new_long_stop = src - fark
                long_stop = max(new_long_stop, long_stop) if src > long_stop else new_long_stop
                
                # Short stop
                new_short_stop = src + fark
                short_stop = min(new_short_stop, short_stop) if src < short_stop else new_short_stop
                
                # Direction
                if src > short_stop:
                    direction = 1
                elif src < long_stop:
                    direction = -1
                
                # OTT value
                mt = long_stop if direction == 1 else short_stop
                ott_values.append(mt)
        
        return ott_values, direction
    except Exception as e:
        print(f"[OTT HATA] {e}")
        return [], 0


# ── OTT CROSSOVER STRATEJİSİ ─────────────────────────────────────────────────
def calc_ott_crossover_signal(df):
    """
    OTT Crossover stratejisi - SADECE KESİŞİM ANINDA SİNYAL ÜRETIR
    
    BULLISH CROSS (AL): Fiyat aşağıdan yukarı keser OTT
    - Önceki mumda: Close < OTT
    - Şimdiki mumda: Close > OTT
    
    BEARISH CROSS (SAT): Fiyat yukarıdan aşağı keser OTT
    - Önceki mumda: Close > OTT
    - Şimdiki mumda: Close < OTT
    """
    try:
        # OTT hesapla
        ott_values, direction = calc_ott(df['high'], df['low'], df['close'], percent=2, coeff=0.5, length=2)
        
        if len(ott_values) < 2:
            return '', 0, 0
        
        closes = df['close'].astype(float).values
        
        # Son iki değeri al
        ott_current = round(ott_values[-1], 2)
        ott_prev = ott_values[-2]
        close_current = closes[-1]
        close_prev = closes[-2]
        
        signal = ''
        
        # BULLISH CROSS - AL sinyali (Fiyat aşağıdan yukarı keser OTT)
        if close_prev < ott_prev and close_current > ott_current:
            signal = 'BUY'
            print(f">>> [🟢 OTT BULLISH CROSS] Fiyat yukarı kesti! Önceki: {close_prev:.2f}<{ott_prev:.2f}, Şimdi: {close_current:.2f}>{ott_current:.2f}")
        
        # BEARISH CROSS - SAT sinyali (Fiyat yukarıdan aşağı keser OTT)
        elif close_prev > ott_prev and close_current < ott_current:
            signal = 'SELL'
            print(f">>> [🔴 OTT BEARISH CROSS] Fiyat aşağı kesti! Önceki: {close_prev:.2f}>{ott_prev:.2f}, Şimdi: {close_current:.2f}<{ott_current:.2f}")
        
        return signal, ott_current, close_current
        
    except Exception as e:
        print(f"[OTT CROSSOVER HATA] {e}")
        import traceback
        traceback.print_exc()
        return '', 0, 0
def calc_sma_crossover_signal(df):
    """
    SMA 5 ve SMA 9 kesişim stratejisi - SADECE KESİŞİM ANINDA SİNYAL ÜRETIR
    
    GOLDEN CROSS (AL): SMA5 aşağıdan yukarı keser SMA9
    - Önceki mumda: SMA5 < SMA9
    - Şimdiki mumda: SMA5 > SMA9
    
    DEATH CROSS (SAT): SMA5 yukarıdan aşağı keser SMA9
    - Önceki mumda: SMA5 > SMA9
    - Şimdiki mumda: SMA5 < SMA9
    
    DİĞER DURUMLAR: Sinyal yok (boş string döner)
    """
    try:
        closes = df['close'].astype(float)
        
        # Tüm SMA değerlerini hesapla
        sma5_series = []
        sma9_series = []
        
        for i in range(len(closes)):
            if i >= SMA_FAST - 1:
                sma5_val = closes[i - SMA_FAST + 1:i + 1].mean()
                sma5_series.append(sma5_val)
            else:
                sma5_series.append(0)
                
            if i >= SMA_SLOW - 1:
                sma9_val = closes[i - SMA_SLOW + 1:i + 1].mean()
                sma9_series.append(sma9_val)
            else:
                sma9_series.append(0)
        
        # Son iki değeri al (şimdiki ve önceki)
        if len(sma5_series) < 2 or len(sma9_series) < 2:
            return '', 0, 0
        
        sma5_current = round(sma5_series[-1], 2)
        sma9_current = round(sma9_series[-1], 2)
        sma5_prev = sma5_series[-2]
        sma9_prev = sma9_series[-2]
        
        if sma5_current == 0 or sma9_current == 0:
            return '', sma5_current, sma9_current
        
        signal = ''
        
        # SADECE KESİŞİM ANINDA SİNYAL ÜRET
        
        # GOLDEN CROSS - AL sinyali (SMA5 aşağıdan yukarı keser SMA9)
        if sma5_prev < sma9_prev and sma5_current > sma9_current:
            signal = 'BUY'
            print(f">>> [🟢 GOLDEN CROSS] SMA5 yukarı kesti! Önceki: {sma5_prev:.2f}<{sma9_prev:.2f}, Şimdi: {sma5_current:.2f}>{sma9_current:.2f}")
        
        # DEATH CROSS - SAT sinyali (SMA5 yukarıdan aşağı keser SMA9)
        elif sma5_prev > sma9_prev and sma5_current < sma9_current:
            signal = 'SELL'
            print(f">>> [🔴 DEATH CROSS] SMA5 aşağı kesti! Önceki: {sma5_prev:.2f}>{sma9_prev:.2f}, Şimdi: {sma5_current:.2f}<{sma9_current:.2f}")
        
        # DİĞER DURUMLAR: Sinyal yok (boş string)
        # - SMA5 hala SMA9'un üstünde ama kesişim yok
        # - SMA5 hala SMA9'un altında ama kesişim yok
        
        return signal, sma5_current, sma9_current
        
    except Exception as e:
        print(f"[SMA CROSSOVER HATA] {e}")
        import traceback
        traceback.print_exc()
        return '', 0, 0


# ── BOT ENGINE (SMA/OTT STRATEJİSİ) ──────────────────────────────────────────
def bot_engine():
    global last_signal, portfolio, starting_value, trade_history, signal_history, open_orders
    
    strategy_name = "OTT Crossover" if USE_OTT else "SMA 5/9 Crossover"
    print(f">>> [BOT] {strategy_name} Stratejisi Başlatıldı.")

    # Veritabanından verileri yükle
    trade_history = db.get_trade_history(limit=50, symbol=SYMBOL)
    signal_history = db.get_signal_history(limit=10, symbol=SYMBOL)
    open_orders = db.get_open_orders(symbol=SYMBOL)
    
    saved_starting_value = db.get_setting("starting_value")
    
    print(f">>> [VERİTABANI] {len(trade_history)} işlem, {len(signal_history)} sinyal, {len(open_orders)} açık emir yüklendi")

    fresh = fetch_balance()
    if fresh:
        portfolio.update(fresh)
        r0 = pub_get("/api/v3/ticker/price", {"symbol": SYMBOL})
        if r0 and r0.status_code == 200:
            init_price     = float(r0.json()["price"])
            coin = SYMBOL.replace('USDT', '')
            coin_balance = portfolio.get(coin, 0)
            current_value = portfolio.get("USDT", 0) + coin_balance * init_price
            
            # Eğer daha önce kaydedilmişse onu kullan, yoksa şimdiki değeri kaydet
            if saved_starting_value is not None:
                starting_value = saved_starting_value
                print(f">>> [BAKİYE] USDT:{portfolio.get('USDT', 0):.2f} {coin}:{coin_balance:.6f} Başlangıç:${starting_value:,.2f} (Kaydedilmiş)")
            else:
                starting_value = current_value
                db.save_setting("starting_value", starting_value)
                print(f">>> [BAKİYE] USDT:{portfolio.get('USDT', 0):.2f} {coin}:{coin_balance:.6f} Başlangıç:${starting_value:,.2f} (Yeni)")
    else:
        print(">>> [UYARI] Bakiye çekilemedi!")

    tick = 0
    while True:
        try:
            tick += 1
            if tick % 10 == 0:
                fresh = fetch_balance()
                if fresh: portfolio.update(fresh)

            r = pub_get("/api/v3/ticker/price", {"symbol": SYMBOL})
            if not r or r.status_code != 200:
                time.sleep(3); continue
            price = float(r.json()["price"])

            r24   = pub_get("/api/v3/ticker/24hr", {"symbol": SYMBOL})
            stats = r24.json() if r24 and r24.status_code == 200 else {}

            # 15 dakikalık mum verisi
            rk = pub_get("/api/v3/klines", {"symbol": SYMBOL, "interval": "15m", "limit": 50})
            if not rk or rk.status_code != 200:
                time.sleep(3); continue

            df = pd.DataFrame(rk.json(), columns=[
                'time','open','high','low','close','vol','ct','qa','tr','tb','tq','ig'
            ])
            df['close'] = df['close'].astype(float)
            df['high']  = df['high'].astype(float)
            df['low']   = df['low'].astype(float)

            # Strateji seçimi
            if USE_OTT:
                # OTT crossover stratejisi
                signal, indicator_val, close_val = calc_ott_crossover_signal(df)
                ind1_name, ind2_name = "OTT", "Close"
                ind1_val, ind2_val = indicator_val, close_val
            else:
                # SMA crossover stratejisi
                signal, sma5, sma9 = calc_sma_crossover_signal(df)
                ind1_name, ind2_name = "SMA5", "SMA9"
                ind1_val, ind2_val = sma5, sma9

            alert = ""
            if signal == 'BUY':
                if USE_OTT:
                    alert = f"⬆️ OTT BULLISH CROSS! Fiyat yukarı kesti OTT (Close:{ind2_val:.2f} > OTT:{ind1_val:.2f})"
                else:
                    alert = f"⬆️ GOLDEN CROSS! SMA5 yukarı kesti SMA9 (SMA5:{ind1_val} > SMA9:{ind2_val})"
            elif signal == 'SELL':
                if USE_OTT:
                    alert = f"⬇️ OTT BEARISH CROSS! Fiyat aşağı kesti OTT (Close:{ind2_val:.2f} < OTT:{ind1_val:.2f})"
                else:
                    alert = f"⬇️ DEATH CROSS! SMA5 aşağı kesti SMA9 (SMA5:{ind1_val} < SMA9:{ind2_val})"

            # Otomatik işlem — sadece sinyal değişince tetiklenir
            if AUTO_TRADE and signal and signal != last_signal:
                if signal == 'BUY':
                    if USE_OTT:
                        print(f">>> [OTT BULLISH CROSS OTO] AL @ ${price:,.2f}  (Close:{ind2_val:.2f} > OTT:{ind1_val:.2f})")
                    else:
                        print(f">>> [GOLDEN CROSS OTO] AL @ ${price:,.2f}  (SMA5:{ind1_val} yukarı kesti SMA9:{ind2_val})")
                    auto_buy(price)
                elif signal == 'SELL':
                    if USE_OTT:
                        print(f">>> [OTT BEARISH CROSS OTO] SAT @ ${price:,.2f}  (Close:{ind2_val:.2f} < OTT:{ind1_val:.2f})")
                    else:
                        print(f">>> [DEATH CROSS OTO] SAT @ ${price:,.2f}  (SMA5:{ind1_val} aşağı kesti SMA9:{ind2_val})")
                    auto_sell(price)
                
                # Sinyal geçmişine ekle
                signal_entry = {
                    "type": signal.lower(),
                    "price": price,
                    "time": int(time.time()),
                    "ind1": ind1_val,
                    "ind2": ind2_val,
                    "ind1_name": ind1_name,
                    "ind2_name": ind2_name,
                    "executed": AUTO_TRADE,
                    "symbol": SYMBOL
                }
                
                # Veritabanına kaydet
                db.save_signal(signal_entry)
                
                # Belleğe ekle (hızlı erişim için)
                signal_history.insert(0, signal_entry)
                if len(signal_history) > 10:
                    signal_history.pop()
                
                socketio.emit('signal_event', signal_entry)
                last_signal = signal
            elif not signal:
                last_signal = ""

            ob = fetch_orderbook()

            socketio.emit('pro_data_stream', {
                "price":      price,
                "sma5":       ind1_val if not USE_OTT else 0,
                "sma9":       ind2_val if not USE_OTT else 0,
                "ott":        ind1_val if USE_OTT else 0,
                "close":      ind2_val if USE_OTT else price,
                "alert":      alert,
                "signal":     signal,
                "portfolio":  portfolio,
                "auto_trade": AUTO_TRADE,
                "use_ott":    USE_OTT,
                "change24":   float(stats.get("priceChangePercent", 0)),
                "high24":     float(stats.get("highPrice", 0)),
                "low24":      float(stats.get("lowPrice", 0)),
                "vol24":      float(stats.get("volume", 0)),
                "orderbook":  ob,
                "starting_value": starting_value,
            })

        except Exception as e:
            print(f"[MOTOR HATA] {e}")
            socketio.emit('log_update', {"msg": f"⚠️ {e}"})

        time.sleep(3)


# ── API ROUTES ────────────────────────────────────────────────────────────────

@app.route('/api/market')
def api_market():
    """Ana sayfa için top coin fiyat verileri — CoinGecko'dan çeker."""
    try:
        ids = ",".join(c["id"] for c in TOP_COINS)
        r   = cg_get("/coins/markets", {
            "vs_currency": "usd",
            "ids": ids,
            "order": "market_cap_desc",
            "per_page": 20,
            "page": 1,
            "sparkline": False,
            "price_change_percentage": "1h,24h,7d"
        })
        if r and r.status_code == 200:
            return jsonify(r.json())
        # Fallback: testnet ticker
        results = []
        for c in TOP_COINS:
            rt = pub_get("/api/v3/ticker/24hr", {"symbol": c["pair"]})
            if rt and rt.status_code == 200:
                d = rt.json()
                results.append({
                    "symbol": c["symbol"],
                    "name":   c["symbol"],
                    "current_price":               float(d.get("lastPrice", 0)),
                    "price_change_percentage_24h": float(d.get("priceChangePercent", 0)),
                    "total_volume": float(d.get("volume", 0)),
                    "high_24h":     float(d.get("highPrice", 0)),
                    "low_24h":      float(d.get("lowPrice", 0)),
                    "image": ""
                })
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/report/<coin_id>')
def api_report(coin_id):
    """Rapor sayfası için coin verisi."""
    try:
        result = {}

        # CoinGecko detay
        r = cg_get(f"/coins/{coin_id}", {
            "localization":     False,
            "tickers":          False,
            "market_data":      True,
            "community_data":   True,
            "developer_data":   False,
            "sparkline":        False
        })
        if r and r.status_code == 200:
            d  = r.json()
            md = d.get("market_data", {})
            result["name"]        = d.get("name", coin_id)
            result["symbol"]      = d.get("symbol", "").upper()
            result["description"] = d.get("description", {}).get("en", "")[:500]
            result["price"]       = md.get("current_price", {}).get("usd", 0)
            result["change_24h"]  = md.get("price_change_percentage_24h", 0)
            result["change_7d"]   = md.get("price_change_percentage_7d", 0)
            result["change_30d"]  = md.get("price_change_percentage_30d", 0)
            result["market_cap"]  = md.get("market_cap", {}).get("usd", 0)
            result["volume_24h"]  = md.get("total_volume", {}).get("usd", 0)
            result["ath"]         = md.get("ath", {}).get("usd", 0)
            result["atl"]         = md.get("atl", {}).get("usd", 0)
            result["rank"]        = d.get("market_cap_rank", 0)
            result["image"]       = d.get("image", {}).get("large", "")
            result["sentiment_up"]   = d.get("sentiment_votes_up_percentage", 0)
            result["sentiment_down"] = d.get("sentiment_votes_down_percentage", 0)

        # Testnet teknik analiz
        sym = coin_id.split("-")[0].upper() + "USDT"
        rk  = pub_get("/api/v3/klines", {"symbol": sym, "interval": "1d", "limit": 200})
        if rk and rk.status_code == 200:
            df = pd.DataFrame(rk.json(), columns=[
                'time','open','high','low','close','vol','ct','qa','tr','tb','tq','ig'
            ])
            df['close'] = df['close'].astype(float)
            df['high']  = df['high'].astype(float)
            df['low']   = df['low'].astype(float)

            result["rsi"]    = safe_rsi(df['close'])
            result["stoch_k"]= safe_stoch(df['high'], df['low'], df['close'])
            result["adx"]    = safe_adx(df['high'], df['low'], df['close'])
            result["ema20"]  = safe_ema(df['close'], 20)
            result["ema50"]  = safe_ema(df['close'], 50)
            result["ema200"] = safe_ema(df['close'], 200) if len(df) >= 200 else 0

            macd_val, macd_sig = safe_macd(df['close'])
            result["macd"]        = macd_val
            result["macd_signal"] = macd_sig

            bb_upper, bb_lower = safe_bb(df['close'])
            result["bb_upper"] = bb_upper
            result["bb_lower"] = bb_lower

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/balance')
def api_balance():
    fresh = fetch_balance()
    if fresh:
        portfolio.update(fresh)
        return jsonify({**portfolio, "starting_value": starting_value})
    return jsonify({"error": "Bakiye alınamadı"}), 500


@app.route('/api/status')
def api_status():
    """Bot durumu ve istatistikler"""
    try:
        # Calculate total balance in USDT
        r = pub_get("/api/v3/ticker/price", {"symbol": SYMBOL})
        coin_price = float(r.json()["price"]) if r and r.status_code == 200 else 0
        coin = SYMBOL.replace('USDT', '')
        coin_balance = portfolio.get(coin, 0)
        total_balance = portfolio.get("USDT", 0) + (coin_balance * coin_price)
        
        # Calculate daily P/L (simplified - using starting value)
        daily_pl = total_balance - starting_value if starting_value > 0 else 0
        
        # Count trades today
        today_trades = len([t for t in trade_history if t.get("time", "").startswith(datetime.now().strftime("%H"))])
        
        return jsonify({
            "is_active": AUTO_TRADE,
            "mode": "testnet",  # Always testnet for now
            "uptime_seconds": 0,  # TODO: Track actual uptime
            "total_balance": round(total_balance, 2),
            "daily_profit_loss": round(daily_pl, 2),
            "total_trades": len(trade_history),
            "successful_trades": len([t for t in trade_history if t.get("side")]),
            "failed_trades": 0,
            "last_signal": last_signal
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/orders/history')
def api_orders_history():
    """İşlem geçmişi"""
    try:
        limit = int(request.args.get('limit', 20))
        # Convert trade_history to API format
        trades = []
        for t in trade_history[:limit]:
            trades.append({
                "timestamp": int(time.time()),  # Simplified
                "symbol": SYMBOL,
                "side": t.get("side", "BUY"),
                "quantity": t.get("qty", 0),
                "price": t.get("price", 0),
                "status": "FILLED",
                "order_type": t.get("type", "MARKET")
            })
        return jsonify(trades)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/signals/history')
def api_signals_history():
    """Son 10 sinyal geçmişi"""
    try:
        # Bellekten değil, veritabanından çek (her zaman güncel)
        signals = db.get_signal_history(limit=10, symbol=SYMBOL)
        return jsonify(signals)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/database/stats')
def api_database_stats():
    """Veritabanı istatistikleri"""
    try:
        stats = db.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/database/clear/<table>', methods=['POST'])
def api_database_clear(table):
    """Veritabanı tablosunu temizle"""
    try:
        if table == 'trades':
            db.clear_trade_history()
            global trade_history
            trade_history = []
            return jsonify({"success": True, "message": "İşlem geçmişi temizlendi"})
        elif table == 'signals':
            db.clear_signal_history()
            global signal_history
            signal_history = []
            return jsonify({"success": True, "message": "Sinyal geçmişi temizlendi"})
        elif table == 'orders':
            db.clear_open_orders()
            global open_orders
            open_orders = []
            return jsonify({"success": True, "message": "Açık emirler temizlendi"})
        elif table == 'all':
            db.clear_trade_history()
            db.clear_signal_history()
            db.clear_open_orders()
            trade_history = []
            signal_history = []
            open_orders = []
            return jsonify({"success": True, "message": "Tüm veriler temizlendi"})
        else:
            return jsonify({"error": "Geçersiz tablo adı"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/database/reset_starting_value', methods=['POST'])
def api_reset_starting_value():
    """Başlangıç bakiyesini sıfırla (şimdiki bakiyeyi başlangıç yap)"""
    try:
        global starting_value
        r = pub_get("/api/v3/ticker/price", {"symbol": SYMBOL})
        if r and r.status_code == 200:
            price = float(r.json()["price"])
            coin = SYMBOL.replace('USDT', '')
            coin_balance = portfolio.get(coin, 0)
            starting_value = portfolio.get("USDT", 0) + coin_balance * price
            db.save_setting("starting_value", starting_value)
            return jsonify({"success": True, "starting_value": starting_value})
        return jsonify({"error": "Fiyat alınamadı"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/settings/chart_colors', methods=['GET', 'POST'])
@login_required
def api_chart_colors():
    """Grafik renk ayarlarını kaydet/getir"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            indicator = data.get('indicator')
            color = data.get('color')
            
            if indicator == 'sma5':
                db.save_setting('sma5_color', color)
            elif indicator == 'sma9':
                db.save_setting('sma9_color', color)
            
            return jsonify({"success": True})
        else:
            # GET - ayarları getir
            sma5_color = db.get_setting('sma5_color', '#0ecb81')
            sma9_color = db.get_setting('sma9_color', '#3861fb')
            line_width = db.get_setting('line_width', 2)
            
            return jsonify({
                "sma5_color": sma5_color,
                "sma9_color": sma9_color,
                "line_width": line_width
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/settings/chart_linewidth', methods=['POST'])
@login_required
def api_chart_linewidth():
    """Çizgi kalınlığını kaydet"""
    try:
        data = request.get_json()
        width = data.get('width', 2)
        db.save_setting('line_width', width)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/signals/active')
def api_signals_active():
    """Aktif sinyaller"""
    try:
        if last_signal:
            return jsonify([{
                "timestamp": int(time.time()),
                "symbol": SYMBOL,
                "signal_type": last_signal,
                "confidence": 1.0,
                "strategy": "SMA 5/9"
            }])
        return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── SOCKET EVENTS ─────────────────────────────────────────────────────────────
@socketio.on('execute_buy')
def handle_buy(data):
    global portfolio
    try:
        print(f">>> [BUY] Alım emri alındı: {data}")
        r     = pub_get("/api/v3/ticker/price", {"symbol": SYMBOL})
        if not r or r.status_code != 200:
            socketio.emit('order_error', {"msg": "❌ Fiyat bilgisi alınamadı"}); return
            
        price = float(r.json()["price"])
        otype = data.get("order_type", "MARKET").upper()
        amount_usdt = float(data.get("amount", 100)) * LEVERAGE
        lp    = float(data.get("limit_price") or price)
        sl    = float(data.get("sl_price") or 0)
        tp    = float(data.get("tp_price") or 0)

        exec_price = lp if otype == "LIMIT" else price
        qty        = round(amount_usdt / exec_price, 6)

        usdt_balance = portfolio.get("USDT", 0)
        print(f">>> [BUY] USDT Bakiye: {usdt_balance}, İstenen: {amount_usdt}, Miktar: {qty}")
        
        if amount_usdt > usdt_balance:
            socketio.emit('order_error', {"msg": f"❌ Yetersiz bakiye! Mevcut: ${usdt_balance:,.2f}"}); return

        order, err = place_order("BUY", otype, qty, limit_price=lp if otype == "LIMIT" else None)
        if err:
            print(f">>> [BUY] Hata: {err}")
            socketio.emit('order_error', {"msg": f"❌ {err}"}); return

        print(f">>> [BUY] Emir başarılı: {order}")
        time.sleep(0.8)
        fresh = fetch_balance()
        if fresh: portfolio.update(fresh)
        log_trade("BUY", otype, qty, exec_price, amount_usdt)

        oid = order.get("orderId", f"local_{int(time.time())}")
        if sl > 0:
            sl_order = {"id": f"{oid}_SL", "type": "STOP_LOSS", "side": "SELL", "qty": qty, "trigger": sl, "time": datetime.now().strftime("%H:%M:%S"), "symbol": SYMBOL}
            open_orders.append(sl_order)
            db.save_open_order(sl_order)
        if tp > 0:
            tp_order = {"id": f"{oid}_TP", "type": "TAKE_PROFIT", "side": "SELL", "qty": qty, "trigger": tp, "time": datetime.now().strftime("%H:%M:%S"), "symbol": SYMBOL}
            open_orders.append(tp_order)
            db.save_open_order(tp_order)
        socketio.emit('open_orders_update', open_orders)
    except Exception as e:
        print(f">>> [BUY] Exception: {e}")
        import traceback
        traceback.print_exc()
        socketio.emit('order_error', {"msg": f"❌ Hata: {e}"})


@socketio.on('execute_sell')
def handle_sell(data):
    global portfolio
    try:
        r     = pub_get("/api/v3/ticker/price", {"symbol": SYMBOL})
        price = float(r.json()["price"])
        otype = data.get("order_type", "MARKET").upper()
        coin  = SYMBOL.replace('USDT', '')
        coin_balance = portfolio.get(coin, 0)
        qty   = float(data.get("amount") or coin_balance)
        lp    = float(data.get("limit_price") or price)

        if qty <= 0:
            socketio.emit('order_error', {"msg": f"❌ Satılacak {coin} miktarı sıfır!"}); return
        if qty > coin_balance:
            socketio.emit('order_error', {"msg": f"❌ Yetersiz {coin}! Mevcut: {coin_balance:.6f}"}); return

        order, err = place_order("SELL", otype, qty, limit_price=lp if otype == "LIMIT" else None)
        if err:
            socketio.emit('order_error', {"msg": f"❌ {err}"}); return

        time.sleep(0.8)
        fresh = fetch_balance()
        if fresh: portfolio.update(fresh)
        exec_price = lp if otype == "LIMIT" else price
        log_trade("SELL", otype, qty, exec_price, round(qty * exec_price, 2))
    except Exception as e:
        socketio.emit('order_error', {"msg": f"❌ Hata: {e}"})


@socketio.on('cancel_order')
def handle_cancel(data):
    global open_orders
    oid = str(data.get("id"))
    
    # Veritabanından sil
    db.delete_open_order(oid)
    
    # Bellekten sil
    open_orders = [o for o in open_orders if str(o["id"]) != oid]
    
    socketio.emit('open_orders_update', open_orders)
    socketio.emit('log_update', {"msg": f"🗑 Emir iptal: {oid}"})


@socketio.on('set_leverage')
def handle_leverage(data):
    global LEVERAGE
    LEVERAGE = max(1, int(data.get("leverage", 1)))
    socketio.emit('log_update', {"msg": f"⚡ Kaldıraç: {LEVERAGE}x"})


@socketio.on('toggle_auto')
def handle_toggle(data):
    global AUTO_TRADE, last_signal
    AUTO_TRADE  = bool(data.get("enabled", True))
    last_signal = ""   # sıfırla → açılınca mevcut sinyale göre hemen işlem yapsın
    socketio.emit('auto_status', {"enabled": AUTO_TRADE})
    state = 'AKTİF ✅' if AUTO_TRADE else 'KAPALI ⛔'
    socketio.emit('log_update', {"msg": f"🤖 Oto Bot: {state}"})


@socketio.on('change_symbol')
def handle_change_symbol(data):
    """Frontend'den gelen symbol değişikliğini işle"""
    global SYMBOL
    new_symbol = data.get('symbol', 'BTCUSDT').upper()
    
    # Geçerli bir symbol olup olmadığını kontrol et
    valid_symbols = [c['pair'] for c in TOP_COINS]
    if new_symbol not in valid_symbols:
        # Eğer listede yoksa ama USDT ile bitiyorsa kabul et
        if not new_symbol.endswith('USDT'):
            socketio.emit('log_update', {"msg": f"⚠️ Geçersiz sembol: {new_symbol}"})
            return
    
    SYMBOL = new_symbol
    symbol_display = new_symbol.replace('USDT', '/USDT')
    socketio.emit('log_update', {"msg": f"📊 Sembol değiştirildi: {symbol_display}"})
    print(f">>> [SYMBOL] Değiştirildi: {SYMBOL}")


@socketio.on('request_history')
def handle_history(data):
    socketio.emit('trade_history_update', trade_history[:20])


# ── FLASK ROUTES ──────────────────────────────────────────────────────────────
# ── FLASK ROUTES ──────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            session['logged_in'] = True
            if remember:
                session.permanent = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Kullanıcı adı veya şifre hatalı!')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/spot')
@login_required
def spot():
    return render_template('spot.html')

@app.route('/portfolio')
@login_required
def portfolio_page():
    return render_template('portfolio.html')

@app.route('/indicators')
@login_required
def indicators():
    return render_template('indicators.html')

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')



if __name__ == '__main__':
    threading.Thread(target=bot_engine, daemon=True).start()
    port = int(os.environ.get('PORT', 5001))
    socketio.run(app, port=port, host='0.0.0.0', allow_unsafe_werkzeug=True)