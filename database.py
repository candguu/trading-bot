"""
SQLite veritabanı yönetimi
Tüm işlem geçmişi, sinyal geçmişi ve bot verilerini saklar
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

DB_FILE = "trading_bot.db"

def init_database():
    """Veritabanını başlat ve tabloları oluştur"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # İşlem geçmişi tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            time TEXT NOT NULL,
            side TEXT NOT NULL,
            type TEXT NOT NULL,
            qty REAL NOT NULL,
            price REAL NOT NULL,
            value REAL NOT NULL,
            symbol TEXT DEFAULT 'BTCUSDT'
        )
    """)
    
    # Sinyal geçmişi tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signal_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            type TEXT NOT NULL,
            price REAL NOT NULL,
            ind1 REAL,
            ind2 REAL,
            ind1_name TEXT,
            ind2_name TEXT,
            executed INTEGER DEFAULT 0,
            symbol TEXT DEFAULT 'BTCUSDT'
        )
    """)
    
    # Bot ayarları tablosu (başlangıç bakiyesi, leverage vb.)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bot_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    # Açık emirler tablosu
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS open_orders (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            side TEXT NOT NULL,
            qty REAL NOT NULL,
            trigger REAL NOT NULL,
            time TEXT NOT NULL,
            symbol TEXT DEFAULT 'BTCUSDT'
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Veritabanı başlatıldı: trading_bot.db")


# ── İŞLEM GEÇMİŞİ ────────────────────────────────────────────────────────────

def save_trade(trade: Dict):
    """Yeni işlemi kaydet"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO trade_history (timestamp, time, side, type, qty, price, value, symbol)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        trade.get("time", ""),
        trade.get("side", ""),
        trade.get("type", ""),
        trade.get("qty", 0),
        trade.get("price", 0),
        trade.get("value", 0),
        trade.get("symbol", "BTCUSDT")
    ))
    
    conn.commit()
    conn.close()


def get_trade_history(limit: int = 50, symbol: Optional[str] = None) -> List[Dict]:
    """İşlem geçmişini getir"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if symbol:
        cursor.execute("""
            SELECT time, side, type, qty, price, value, symbol
            FROM trade_history
            WHERE symbol = ?
            ORDER BY id DESC
            LIMIT ?
        """, (symbol, limit))
    else:
        cursor.execute("""
            SELECT time, side, type, qty, price, value, symbol
            FROM trade_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "time": row[0],
            "side": row[1],
            "type": row[2],
            "qty": row[3],
            "price": row[4],
            "value": row[5],
            "symbol": row[6]
        }
        for row in rows
    ]


def clear_trade_history():
    """Tüm işlem geçmişini sil"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM trade_history")
    conn.commit()
    conn.close()


# ── SİNYAL GEÇMİŞİ ───────────────────────────────────────────────────────────

def save_signal(signal: Dict):
    """Yeni sinyali kaydet"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO signal_history (timestamp, type, price, ind1, ind2, ind1_name, ind2_name, executed, symbol)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        signal.get("time", int(datetime.now().timestamp())),
        signal.get("type", ""),
        signal.get("price", 0),
        signal.get("ind1", 0),
        signal.get("ind2", 0),
        signal.get("ind1_name", ""),
        signal.get("ind2_name", ""),
        1 if signal.get("executed", False) else 0,
        signal.get("symbol", "BTCUSDT")
    ))
    
    conn.commit()
    conn.close()


def get_signal_history(limit: int = 10, symbol: Optional[str] = None) -> List[Dict]:
    """Sinyal geçmişini getir"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if symbol:
        cursor.execute("""
            SELECT timestamp, type, price, ind1, ind2, ind1_name, ind2_name, executed
            FROM signal_history
            WHERE symbol = ?
            ORDER BY id DESC
            LIMIT ?
        """, (symbol, limit))
    else:
        cursor.execute("""
            SELECT timestamp, type, price, ind1, ind2, ind1_name, ind2_name, executed
            FROM signal_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "time": row[0],
            "type": row[1],
            "price": row[2],
            "ind1": row[3],
            "ind2": row[4],
            "ind1_name": row[5],
            "ind2_name": row[6],
            "executed": bool(row[7])
        }
        for row in rows
    ]


def clear_signal_history():
    """Tüm sinyal geçmişini sil"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM signal_history")
    conn.commit()
    conn.close()


# ── BOT AYARLARI ──────────────────────────────────────────────────────────────

def save_setting(key: str, value):
    """Bot ayarını kaydet"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO bot_settings (key, value, updated_at)
        VALUES (?, ?, ?)
    """, (key, json.dumps(value), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()


def get_setting(key: str, default=None):
    """Bot ayarını getir"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT value FROM bot_settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return json.loads(row[0])
    return default


# ── AÇIK EMİRLER ──────────────────────────────────────────────────────────────

def save_open_order(order: Dict):
    """Açık emri kaydet"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO open_orders (id, type, side, qty, trigger, time, symbol)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        order.get("id", ""),
        order.get("type", ""),
        order.get("side", ""),
        order.get("qty", 0),
        order.get("trigger", 0),
        order.get("time", ""),
        order.get("symbol", "BTCUSDT")
    ))
    
    conn.commit()
    conn.close()


def get_open_orders(symbol: Optional[str] = None) -> List[Dict]:
    """Açık emirleri getir"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if symbol:
        cursor.execute("""
            SELECT id, type, side, qty, trigger, time, symbol
            FROM open_orders
            WHERE symbol = ?
        """, (symbol,))
    else:
        cursor.execute("""
            SELECT id, type, side, qty, trigger, time, symbol
            FROM open_orders
        """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "type": row[1],
            "side": row[2],
            "qty": row[3],
            "trigger": row[4],
            "time": row[5],
            "symbol": row[6]
        }
        for row in rows
    ]


def delete_open_order(order_id: str):
    """Açık emri sil"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM open_orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()


def clear_open_orders():
    """Tüm açık emirleri sil"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM open_orders")
    conn.commit()
    conn.close()


# ── YARDIMCI FONKSİYONLAR ─────────────────────────────────────────────────────

def get_stats() -> Dict:
    """Veritabanı istatistiklerini getir"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM trade_history")
    trade_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM signal_history")
    signal_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM open_orders")
    order_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_trades": trade_count,
        "total_signals": signal_count,
        "open_orders": order_count
    }


if __name__ == "__main__":
    # Test
    init_database()
    print("Veritabanı test edildi!")
    print("İstatistikler:", get_stats())
