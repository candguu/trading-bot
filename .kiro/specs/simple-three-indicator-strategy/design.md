# Simple Three Indicator Strategy Bugfix Design

## Overview

Mevcut kripto trading bot sistemi 7 indikatörlü (RSI, MACD, Bollinger Bands, Stochastic, ADX, EMA, SuperTrend) karmaşık bir konsensüs mekanizması kullanmaktadır. Bu sistem 4/7 çoğunluk mantığıyla çalışmakta ancak karmaşık yapısı nedeniyle etkili sinyal üretememektedir.

Bu bugfix, mevcut sistemi tamamen yeniden yapılandırarak basit ve etkili 3 indikatörlü bir sisteme (RSI, OTT, Bollinger Bands) geçiş sağlayacaktır. Yeni sistem 2/3 çoğunluk mantığıyla çalışacak ve otomatik işlem yapacaktır.

## Glossary

- **Bug_Condition (C)**: Sistemin 7 indikatör kullanması ve 4/7 konsensüs araması - bu karmaşıklık etkili sinyal üretimini engellemektedir
- **Property (P)**: Yalnızca 3 indikatör (RSI, OTT, Bollinger Bands) kullanılarak 2/3 çoğunluk mantığıyla basit ve etkili sinyal üretimi
- **Preservation**: Binance API entegrasyonu, bakiye yönetimi, WebSocket iletişimi, işlem logları ve AUTO_TRADE modu kontrolü değişmeden kalmalıdır
- **calc_consensus()**: `main.py` dosyasındaki 7 indikatörü hesaplayan ve konsensüs sinyali üreten fonksiyon
- **bot_engine()**: Ana bot döngüsü - piyasa verilerini çeker, indikatörleri hesaplar ve otomatik işlem yapar
- **OTT (Optimized Trend Tracker)**: Trend takibi için kullanılan yeni indikatör (Period=2, Percent=1.4%, MA Type=VAR)
- **AUTO_TRADE**: Global değişken - True ise otomatik işlem yapar, False ise sadece sinyal gösterir

## Bug Details

### Fault Condition

Bug, bot çalıştırıldığında ve sinyal üretilmeye çalışıldığında ortaya çıkmaktadır. `calc_consensus()` fonksiyonu 7 farklı indikatörü (RSI, MACD, Bollinger Bands, EMA Cross, Stochastic, VWAP, SuperTrend) hesaplamakta ve bunların 4 tanesinin aynı yönde sinyal vermesini beklemektedir. Bu karmaşık yapı etkili sinyal üretimini engellemektedir.

**Formal Specification:**
```
FUNCTION isBugCondition(system_state)
  INPUT: system_state of type BotSystemState
  OUTPUT: boolean
  
  RETURN system_state.indicator_count == 7
         AND system_state.consensus_threshold == 4
         AND system_state.uses_complex_weighted_average == True
         AND system_state.signal_generation_effective == False
END FUNCTION
```

### Examples

- **Örnek 1**: Bot çalıştırıldığında 7 indikatör hesaplanır (RSI, MACD, BB, EMA, Stoch, VWAP, SuperTrend) → Beklenen: Sadece 3 indikatör (RSI, OTT, BB) hesaplanmalı
- **Örnek 2**: RSI=AL, MACD=AL, BB=SAT, EMA=AL, Stoch=NEUTRAL, VWAP=SAT, SuperTrend=NEUTRAL → 4/7 AL sinyali üretilir → Beklenen: Sadece RSI, OTT, BB değerlendirilmeli ve 2/3 çoğunluk aranmalı
- **Örnek 3**: Konsensüs hesaplanırken 7 indikatörün tümü değerlendirilir → Beklenen: Sadece 3 indikatör değerlendirilmeli
- **Edge Case**: AUTO_TRADE=False iken sistem sadece sinyal göstermeli ancak işlem yapmamalı → Bu davranış korunmalı

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- Binance API üzerinden bakiye sorgulama (`fetch_balance()`) aynı şekilde çalışmalı
- Binance API üzerinden piyasa fiyatı çekme (`pub_get("/api/v3/ticker/price")`) aynı şekilde çalışmalı
- Emir verme fonksiyonları (`place_order()`, `auto_buy()`, `auto_sell()`) aynı şekilde çalışmalı
- İşlem geçmişi loglama (`log_trade()`) aynı şekilde çalışmalı
- WebSocket üzerinden frontend'e veri gönderme (`socketio.emit()`) aynı şekilde çalışmalı
- AUTO_TRADE modu kontrolü - False iken sadece sinyal gösterme davranışı korunmalı
- TradingView tarzında grafik üzerinde AL/SAT işaretleri gösterme davranışı korunmalı

**Scope:**
Sadece indikatör hesaplama ve konsensüs mantığı değişecektir. Tüm API entegrasyonları, bakiye yönetimi, emir verme, loglama ve WebSocket iletişimi tamamen değişmeden kalacaktır. Bu şunları içerir:
- Binance API çağrıları ve authentication
- Bakiye sorgulama ve güncelleme
- Emir verme ve iptal etme
- İşlem geçmişi kaydetme
- WebSocket üzerinden gerçek zamanlı veri akışı
- AUTO_TRADE modu kontrolü

## Hypothesized Root Cause

Mevcut bug'ın temel nedenleri:

1. **Aşırı Karmaşık İndikatör Seti**: 7 farklı indikatör kullanılması sistem karmaşıklığını artırmakta ve etkili sinyal üretimini engellemektedir
   - Her indikatör farklı zaman dilimlerinde ve farklı piyasa koşullarında farklı sinyaller üretmekte
   - 4/7 konsensüs eşiği çok yüksek olduğu için nadiren tetiklenmekte

2. **Yüksek Konsensüs Eşiği**: 4/7 çoğunluk gerektiren sistem çok katı bir eşik belirlemekte ve bu nedenle az sinyal üretmekte

3. **Gereksiz İndikatör Çeşitliliği**: VWAP, Stochastic, ADX, EMA Cross gibi indikatörler temel trend ve momentum bilgisini tekrar etmekte

4. **Karmaşık Ağırlıklı Ortalama**: Mevcut sistem her indikatöre eşit ağırlık vermekte ancak bazı indikatörler daha güvenilir olabilir

## Correctness Properties

Property 1: Fault Condition - Three Indicator System

_For any_ bot execution where the system is running, the fixed calc_consensus function SHALL use only 3 indicators (RSI, OTT, Bollinger Bands) and apply 2/3 majority logic to generate BUY/SELL signals, eliminating the complex 7-indicator system.

**Validates: Requirements 2.1, 2.2, 2.3, 2.6, 2.7**

Property 2: Preservation - API and Trading Infrastructure

_For any_ operation that involves Binance API calls, balance management, order placement, trade logging, WebSocket communication, or AUTO_TRADE mode control, the fixed system SHALL produce exactly the same behavior as the original system, preserving all existing infrastructure functionality.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7**

## Fix Implementation

### Changes Required

Assuming our root cause analysis is correct:

**File**: `main.py`

**Function**: `calc_consensus(df, price)`

**Specific Changes**:

1. **Remove Old Indicators**: 7 indikatörlü sistemi tamamen kaldır
   - MACD, EMA Cross, Stochastic, VWAP, SuperTrend hesaplamalarını kaldır
   - Sadece RSI ve Bollinger Bands hesaplamalarını koru

2. **Add OTT Indicator**: Yeni OTT (Optimized Trend Tracker) indikatörünü ekle
   - Period: 2
   - Percent: 1.4%
   - MA Type: VAR (Variance-based Moving Average)
   - OTT hesaplama fonksiyonu: `safe_ott(df_close, period=2, percent=1.4)`

3. **Simplify Consensus Logic**: 2/3 çoğunluk mantığına geç
   - 3 indikatörden 2'si AL → AL sinyali
   - 3 indikatörden 2'si SAT → SAT sinyali
   - Diğer durumlar → BEKLİ (sinyal yok)

4. **Update Return Values**: Fonksiyon dönüş değerlerini güncelle
   - Sadece 3 indikatörün sinyallerini döndür
   - Gereksiz indikatör değerlerini kaldır

5. **Update WebSocket Emission**: Frontend'e gönderilen veriyi güncelle
   - Sadece RSI, OTT, Bollinger Bands değerlerini gönder
   - Eski indikatör değerlerini kaldır

### OTT Indicator Implementation

OTT indikatörü için yeni bir fonksiyon eklenecek:

```python
def safe_ott(df_close, period=2, percent=1.4):
    """
    OTT (Optimized Trend Tracker) indikatörü
    Period: 2, Percent: 1.4%, MA Type: VAR
    """
    try:
        # VAR (Variance-based) Moving Average hesapla
        var_ma = df_close.rolling(window=period).var()
        
        # OTT hesaplama
        ott_value = var_ma * (1 + percent / 100)
        
        # Trend yönü belirleme
        if df_close.iloc[-1] > ott_value.iloc[-1]:
            return 1, ott_value.iloc[-1]  # Uptrend
        else:
            return -1, ott_value.iloc[-1]  # Downtrend
    except:
        return 0, 0.0
```

### Updated calc_consensus Function

```python
def calc_consensus(df, price):
    """
    3 indikatör hesaplar: RSI, OTT, Bollinger Bands
    2/3 çoğunluk mantığıyla sinyal üretir
    """
    signals = {}

    # 1. RSI
    rsi = safe_rsi(df['close'])
    if   rsi < 35: signals['rsi'] = 'buy'
    elif rsi > 65: signals['rsi'] = 'sell'
    else:          signals['rsi'] = 'neutral'

    # 2. OTT
    ott_dir, ott_val = safe_ott(df['close'], period=2, percent=1.4)
    if   ott_dir ==  1: signals['ott'] = 'buy'
    elif ott_dir == -1: signals['ott'] = 'sell'
    else:               signals['ott'] = 'neutral'

    # 3. Bollinger Bands
    bb_upper, bb_lower = safe_bb(df['close'])
    if   price <= bb_lower * 1.002: signals['bb'] = 'buy'
    elif price >= bb_upper * 0.998: signals['bb'] = 'sell'
    else:                            signals['bb'] = 'neutral'

    buy_count  = sum(1 for v in signals.values() if v == 'buy')
    sell_count = sum(1 for v in signals.values() if v == 'sell')

    consensus = ''
    if buy_count >= 2:
        consensus = 'BUY'
    elif sell_count >= 2:
        consensus = 'SELL'

    return consensus, buy_count, sell_count, signals, rsi, ott_val, bb_upper, bb_lower
```

## Testing Strategy

### Validation Approach

Testing stratejisi iki aşamalı bir yaklaşım izler: önce unfixed kod üzerinde bug'ı göstermek için counterexample'lar üretilir, sonra fix'in doğru çalıştığı ve mevcut davranışları koruduğu doğrulanır.

### Exploratory Fault Condition Checking

**Goal**: Fix uygulanmadan ÖNCE bug'ı göstermek için counterexample'lar üretmek. Root cause analizini doğrulamak veya reddetmek. Eğer reddedersek, yeniden hipotez kurmamız gerekecek.

**Test Plan**: Unfixed kod üzerinde 7 indikatörlü sistemin karmaşıklığını ve düşük sinyal üretim oranını gözlemlemek için testler yazmak. Bu testler unfixed kod üzerinde çalıştırılarak sistemin ne kadar az sinyal ürettiğini gösterecek.

**Test Cases**:
1. **Seven Indicator Complexity Test**: Sistemin 7 indikatör hesapladığını doğrula (unfixed kod üzerinde başarılı olacak)
2. **High Threshold Test**: 4/7 konsensüs eşiğinin çok yüksek olduğunu ve az sinyal ürettiğini göster (unfixed kod üzerinde başarısız olacak)
3. **Signal Generation Rate Test**: 100 farklı piyasa durumunda kaç sinyal üretildiğini ölç (unfixed kod üzerinde düşük oran gösterecek)
4. **Indicator Conflict Test**: 7 indikatörün çelişkili sinyaller verdiği durumları göster (unfixed kod üzerinde konsensüs üretemeyecek)

**Expected Counterexamples**:
- 7 indikatör hesaplanıyor ancak 4/7 konsensüs nadiren sağlanıyor
- Possible causes: Aşırı karmaşık sistem, yüksek konsensüs eşiği, gereksiz indikatör çeşitliliği

### Fix Checking

**Goal**: Bug condition'ın geçerli olduğu tüm inputlar için fixed fonksiyonun beklenen davranışı ürettiğini doğrulamak.

**Pseudocode:**
```
FOR ALL system_state WHERE isBugCondition(system_state) DO
  result := calc_consensus_fixed(df, price)
  ASSERT result.indicator_count == 3
  ASSERT result.uses_only_rsi_ott_bb == True
  ASSERT result.consensus_threshold == 2
END FOR
```

### Preservation Checking

**Goal**: Bug condition'ın geçerli OLMADIĞI tüm inputlar için fixed fonksiyonun original fonksiyonla aynı sonucu ürettiğini doğrulamak.

**Pseudocode:**
```
FOR ALL operation WHERE NOT isBugCondition(operation) DO
  ASSERT api_operations_original(operation) = api_operations_fixed(operation)
  ASSERT balance_management_original(operation) = balance_management_fixed(operation)
  ASSERT order_placement_original(operation) = order_placement_fixed(operation)
END FOR
```

**Testing Approach**: Property-based testing preservation checking için önerilir çünkü:
- Input domain'i boyunca otomatik olarak birçok test case üretir
- Manuel unit testlerin kaçırabileceği edge case'leri yakalar
- Tüm non-buggy inputlar için davranışın değişmediğine dair güçlü garantiler sağlar

**Test Plan**: Önce unfixed kod üzerinde API çağrıları, bakiye yönetimi, emir verme davranışlarını gözlemle, sonra bu davranışları yakalayan property-based testler yaz.

**Test Cases**:
1. **API Call Preservation**: Binance API çağrılarının aynı şekilde çalıştığını doğrula (unfixed kod üzerinde gözlemle, sonra test yaz)
2. **Balance Management Preservation**: Bakiye sorgulama ve güncelleme davranışının korunduğunu doğrula
3. **Order Placement Preservation**: Emir verme fonksiyonlarının aynı şekilde çalıştığını doğrula
4. **WebSocket Preservation**: WebSocket iletişiminin korunduğunu doğrula (sadece gönderilen veri formatı değişecek)
5. **AUTO_TRADE Mode Preservation**: AUTO_TRADE=False iken sadece sinyal gösterme davranışının korunduğunu doğrula

### Unit Tests

- 3 indikatörün (RSI, OTT, Bollinger Bands) doğru hesaplandığını test et
- 2/3 çoğunluk mantığının doğru çalıştığını test et
- Edge case'leri test et (tüm indikatörler neutral, 1 buy + 1 sell + 1 neutral)
- OTT indikatörünün doğru parametrelerle (period=2, percent=1.4) hesaplandığını test et

### Property-Based Tests

- Rastgele piyasa verileri üret ve 3 indikatörlü sistemin sinyal ürettiğini doğrula
- Rastgele fiyat hareketleri üret ve 2/3 çoğunluk mantığının doğru çalıştığını doğrula
- Birçok farklı senaryoda API çağrılarının, bakiye yönetiminin ve emir verme davranışının korunduğunu test et

### Integration Tests

- Bot'u başlat ve 3 indikatörlü sistemin çalıştığını doğrula
- AUTO_TRADE=True ile otomatik işlem yapıldığını doğrula
- AUTO_TRADE=False ile sadece sinyal gösterildiğini doğrula
- WebSocket üzerinden frontend'e doğru verilerin gönderildiğini doğrula
- Grafik üzerinde AL/SAT işaretlerinin doğru gösterildiğini doğrula
