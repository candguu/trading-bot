# Bugfix Requirements Document

## Introduction

Mevcut kripto trading bot sistemi 7 indikatörlü (RSI, MACD, Bollinger Bands, Stochastic, ADX, EMA, SuperTrend) konsensüs tabanlı bir strateji kullanmaktadır. Bu sistem 4/7 çoğunluk mantığıyla çalışmakta ancak karmaşık yapısı nedeniyle etkili sinyal üretememektedir. 

Bu bugfix, mevcut karmaşık sistemi tamamen kaldırıp, basit ve etkili 3 indikatörlü bir sisteme (RSI, OTT, Bollinger Bands) geçişi sağlayacaktır. Yeni sistem 2/3 çoğunluk mantığıyla çalışacak ve otomatik işlem yapacaktır.

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN bot çalıştırıldığında THEN sistem 7 indikatör (RSI, MACD, Bollinger Bands, Stochastic, ADX, EMA, SuperTrend, VWAP) hesaplar ve 4/7 çoğunluk konsensüsü arar

1.2 WHEN konsensüs hesaplanırken THEN sistem karmaşık ağırlıklı ortalama ve çoklu koşul kontrolü yapar

1.3 WHEN sinyal üretilmeye çalışıldığında THEN sistem 7 farklı indikatörün tümünü değerlendirmek zorunda kalır ve bu karmaşıklık etkili sinyal üretimini engeller

1.4 WHEN otomatik işlem yapılırken THEN sistem mevcut 7 indikatörlü konsensüs skoruna göre karar verir

### Expected Behavior (Correct)

2.1 WHEN bot çalıştırıldığında THEN sistem yalnızca 3 indikatör (RSI, OTT, Bollinger Bands) hesaplamalıdır

2.2 WHEN RSI, OTT ve Bollinger Bands indikatörlerinden 2 tanesi AL sinyali verdiğinde THEN sistem otomatik olarak mevcut piyasa fiyatından AL emri vermelidir

2.3 WHEN RSI, OTT ve Bollinger Bands indikatörlerinden 2 tanesi SAT sinyali verdiğinde THEN sistem otomatik olarak mevcut piyasa fiyatından SAT emri vermelidir

2.4 WHEN AL emri verilirken THEN sistem bakiyenin %95'ini kullanmalıdır (%5 komisyon ve güvenlik için rezervde tutulur)

2.5 WHEN SAT emri verilirken THEN sistem mevcut coin'in tamamını satmalıdır

2.6 WHEN 3 indikatörden 2'si aynı yönde sinyal vermediğinde THEN sistem hiçbir işlem yapmamalıdır (BEKLİ durumu)

2.7 WHEN OTT indikatörü hesaplanırken THEN sistem şu parametreleri kullanmalıdır: Period=2, Percent=1.4%, MA Type=VAR

### Unchanged Behavior (Regression Prevention)

3.1 WHEN bakiye sorgulandığında THEN sistem mevcut USDT ve BTC bakiyelerini doğru şekilde göstermeye devam etmelidir

3.2 WHEN piyasa fiyatı çekildiğinde THEN sistem Binance API'den gerçek zamanlı fiyat verilerini almaya devam etmelidir

3.3 WHEN emir verildiğinde THEN sistem Binance API üzerinden güvenli şekilde emir göndermeye devam etmelidir

3.4 WHEN işlem geçmişi kaydedildiğinde THEN sistem tüm işlemleri log dosyasına yazmaya devam etmelidir

3.5 WHEN WebSocket üzerinden veri gönderildiğinde THEN sistem frontend'e gerçek zamanlı veri akışı sağlamaya devam etmelidir

3.6 WHEN AUTO_TRADE modu kapalıyken THEN sistem yalnızca sinyal göstermeli ancak otomatik işlem yapmamalıdır

3.7 WHEN grafik üzerinde sinyal gösterildiğinde THEN sistem TradingView tarzında AL/SAT işaretlerini ilgili mumda göstermeye devam etmelidir
