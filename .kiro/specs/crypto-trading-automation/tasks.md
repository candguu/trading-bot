# Implementation Plan: Crypto Trading Automation - Professional Web Interface

## Overview

Bu görev listesi, kripto ticaret otomasyon sistemine profesyonel web arayüzü iyileştirmelerini eklemek için gerekli implementasyon adımlarını içerir. Mevcut temel HTML template'leri modernize edilecek, CSS tasarım sistemi uygulanacak, interaktif grafikler eklenecek ve gerçek zamanlı veri güncellemeleri için WebSocket entegrasyonu yapılacaktır.

Sistem Python backend (Flask/FastAPI) ve modern frontend teknolojileri (HTML5, CSS3, JavaScript ES6+) kullanmaktadır.

## Tasks

- [x] 1. CSS Tasarım Sistemi ve Temel Stil Altyapısı
  - [x] 1.1 CSS değişkenleri ve renk paleti oluştur
    - Dark ve light theme için renk değişkenleri tanımla
    - Tipografi sistemi (font-family, font-size, font-weight) oluştur
    - Spacing sistemi (margins, paddings) tanımla
    - `static/css/variables.css` dosyası oluştur
    - _Requirements: 16.2, 16.3, 16.4_
  
  - [x] 1.2 Temel bileşen stilleri oluştur
    - Card, button, input, table bileşen stillerini yaz
    - Hover effects ve transition animasyonları ekle
    - Loading spinner ve skeleton loader stilleri ekle
    - `static/css/components.css` dosyası oluştur
    - _Requirements: 16.1, 16.6, 16.7_
  
  - [x] 1.3 Responsive layout sistemi oluştur
    - Mobile, tablet, desktop breakpoint'leri tanımla
    - Flexbox/Grid layout yapıları oluştur
    - Media query'ler ile responsive davranışlar ekle
    - `static/css/layout.css` dosyası oluştur
    - _Requirements: 16.5, 16.8_

- [x] 2. Navigasyon ve Sayfa Düzeni İyileştirmeleri
  - [x] 2.1 Sticky navigation bar implementasyonu
    - Tüm sayfalarda tutarlı navbar yapısı oluştur
    - Aktif sayfa vurgulama özelliği ekle
    - Logo ve sistem adı ekle
    - Responsive hamburger menü (mobil için) ekle
    - _Requirements: 22.1, 22.2, 22.3, 22.4_
  
  - [x] 2.2 Tutarlı sayfa layout yapısı oluştur
    - Container, header, main, footer yapısını standartlaştır
    - Maksimum genişlik ve merkezleme uygula
    - Sayfa başlıkları ve alt başlıklar için hiyerarşi oluştur
    - Footer bileşeni ekle (telif hakkı, versiyon)
    - _Requirements: 22.5, 22.6, 22.7, 22.8_

- [x] 3. Theme Switcher (Dark/Light Mode) Sistemi
  - [x] 3.1 Theme toggle mekanizması implementasyonu
    - JavaScript ile theme değiştirme fonksiyonu yaz
    - LocalStorage ile theme tercihini kaydet
    - Sayfa yüklendiğinde kaydedilmiş theme'i uygula
    - Toggle butonu ekle (navbar'da)
    - _Requirements: 16.2_
  
  - [x] 3.2 CSS theme değişkenleri dinamik güncelleme
    - Dark ve light theme için tüm renk değişkenlerini tanımla
    - JavaScript ile CSS değişkenlerini dinamik değiştir
    - Smooth transition animasyonu ekle
    - _Requirements: 16.2, 16.7_

- [x] 4. Dashboard Sayfası Modernizasyonu (index.html)
  - [x] 4.1 Dashboard layout ve kartlar oluştur
    - Grid layout ile kart yapısı oluştur
    - Bot durumu kartı (aktif/pasif, mod göstergesi)
    - Hızlı istatistikler kartları (toplam bakiye, günlük P/L, işlem sayısı)
    - Son işlemler listesi kartı
    - Aktif sinyaller kartı
    - _Requirements: 16.1, 18.2, 18.5_
  
  - [x] 4.2 Mini fiyat trendi grafiği ekle
    - Chart.js veya TradingView Lightweight Charts entegrasyonu
    - Basit çizgi grafik ile fiyat trendi göster
    - Responsive grafik boyutlandırma
    - _Requirements: 19.1_
  
  - [ ]* 4.3 Dashboard bileşenleri için unit testler
    - Kart render testleri
    - Veri güncelleme testleri
    - _Requirements: 16.1_

- [x] 5. Gelişmiş Portföy Görünümü (portfolio.html)
  - [x] 5.1 Portföy özet paneli oluştur
    - Toplam portföy değeri büyük gösterge
    - Günlük, haftalık, aylık kar/zarar istatistikleri
    - Renk kodlu performans göstergeleri (yeşil/kırmızı)
    - _Requirements: 17.3, 17.4, 17.5_
  
  - [x] 5.2 Coin listesi tablosu implementasyonu
    - Her coin için: sembol, miktar, fiyat, toplam değer, değişim yüzdesi
    - Sıralama (sorting) özelliği ekle
    - Hızlı işlem butonları (AL/SAT) ekle
    - Responsive tablo tasarımı
    - _Requirements: 17.1, 17.7_
  
  - [x] 5.3 Portföy dağılımı grafiği ekle
    - Pasta grafik veya halka grafik (donut chart) implementasyonu
    - Her coin için renk kodlama
    - Hover ile detay gösterme (tooltip)
    - _Requirements: 17.2_
  
  - [x] 5.4 Portföy performans çizgi grafiği ekle
    - Zaman içinde portföy değeri değişimi grafiği
    - Zaman aralığı seçici (1D, 1W, 1M, 3M, 1Y)
    - _Requirements: 17.6_
  
  - [ ]* 5.5 Portföy hesaplama için property test
    - **Property 28: Portföy değeri hesaplama**
    - **Validates: Requirements 17.1**
    - Her coin için fiyat × miktar = toplam değer doğrulaması
  
  - [ ]* 5.6 Portföy bileşenleri için unit testler
    - Toplam değer hesaplama testleri
    - Grafik render testleri
    - _Requirements: 17.1, 17.2_

- [x] 6. Hesap Bilgileri Paneli Geliştirme
  - [x] 6.1 Hesap özet kartları oluştur
    - Toplam bakiye, kullanılabilir bakiye, kilitli bakiye kartları
    - API bağlantı durumu göstergesi (gerçek zamanlı)
    - Bot durumu göstergesi (aktif/pasif, görsel vurgu)
    - Hesap modu göstergesi (Testnet/Live Trading, belirgin)
    - _Requirements: 18.1, 18.2, 18.3, 18.5_
  
  - [x] 6.2 İstatistik kartları implementasyonu
    - Günlük işlem sayısı ve toplam işlem hacmi
    - Son işlem zamanı ve bir sonraki analiz zamanı
    - Hesap güvenlik durumu ve API izinleri
    - _Requirements: 18.4, 18.6, 18.7_
  
  - [x] 6.3 Kart bileşenleri stil ve layout
    - Grid layout ile düzenli yerleşim
    - İkon entegrasyonu (Font Awesome veya Material Icons)
    - Responsive tasarım
    - _Requirements: 18.8_

- [x] 7. İnteraktif Grafik Sistemi (indicators.html)
  - [x] 7.1 Ana fiyat grafiği implementasyonu
    - TradingView Lightweight Charts veya Chart.js entegrasyonu
    - Candlestick ve çizgi grafik desteği
    - Zaman aralığı seçici (1m, 5m, 15m, 1h, 4h, 1d)
    - Zoom ve pan (kaydırma) işlevleri
    - _Requirements: 19.1, 19.3, 19.4_
  
  - [x] 7.2 Teknik indikatör overlay'leri ekle
    - RSI, MACD, Bollinger Bands göstergeleri
    - Ana grafik üzerinde veya alt panellerde gösterim
    - İndikatör açma/kapama toggle'ları
    - _Requirements: 19.2_
  
  - [x] 7.3 Grafik interaktivite özellikleri
    - Tooltip ile detaylı bilgi gösterme
    - AL/SAT sinyallerini grafik üzerinde işaretleme
    - Crosshair cursor
    - _Requirements: 19.5, 19.6_
  
  - [x] 7.4 Gerçek zamanlı grafik güncelleme
    - WebSocket ile canlı veri akışı entegrasyonu
    - Otomatik grafik güncelleme
    - Performans optimizasyonu (debouncing)
    - _Requirements: 19.7_
  
  - [ ]* 7.5 Grafik güncelleme için property test
    - **Property 31: Grafik veri güncellemesi**
    - **Validates: Requirements 19.7**
    - Yeni piyasa verisi geldiğinde grafik güncelleme doğrulaması

- [x] 8. Gelişmiş İşlem Geçmişi ve Log Görünümü
  - [x] 8.1 İşlem tablosu implementasyonu
    - Tablo yapısı: tarih, saat, tip, coin, miktar, fiyat, durum
    - Başarılı/başarısız işlemler için renk kodlama
    - Sayfalama (pagination) özelliği
    - _Requirements: 20.1, 20.3, 20.4_
  
  - [x] 8.2 Filtreleme ve arama sistemi
    - Tarih, tip, coin filtreleri
    - Arama (search) özelliği
    - Filtre uygulama ve temizleme butonları
    - _Requirements: 20.2, 20.8_
  
  - [x] 8.3 İşlem detay modal ve özet
    - Her işlem için detay görüntüleme modal'ı
    - Toplam kar/zarar özet kartı
    - Dışa aktarma butonu (CSV/JSON)
    - _Requirements: 20.5, 20.6, 20.7_
  
  - [ ]* 8.4 İşlem filtreleme için property test
    - **Property 32: İşlem filtreleme**
    - **Validates: Requirements 20.2**
    - Filtre kriterlerine uygun işlem gösterimi doğrulaması

- [x] 9. Bildirim ve Uyarı Sistemi (Toast Notifications)
  - [x] 9.1 Toast notification bileşeni oluştur
    - Toast container ve toast item HTML/CSS yapısı
    - Başarı, hata, uyarı, bilgi tipleri için stiller
    - Ekranın sağ üst köşesinde konumlandırma
    - Kapatma butonu
    - _Requirements: 21.5, 21.7_
  
  - [x] 9.2 Notification manager JavaScript sınıfı
    - Toast gösterme fonksiyonu (show)
    - Otomatik kapanma mekanizması (5 saniye)
    - Maksimum 3 bildirim sınırlaması
    - Queue yönetimi
    - _Requirements: 21.6, 21.8_
  
  - [x] 9.3 Olay bazlı bildirim tetikleyicileri
    - İşlem başarılı → başarı bildirimi
    - İşlem başarısız → hata bildirimi
    - API bağlantı kesildi → uyarı bildirimi
    - Bot durumu değişti → bilgi bildirimi
    - _Requirements: 21.1, 21.2, 21.3, 21.4_
  
  - [ ]* 9.4 Bildirim sistemi için property testler
    - **Property 33: Bildirim görüntüleme**
    - **Validates: Requirements 21.1**
    - **Property 34: Bildirim otomatik kapanma**
    - **Validates: Requirements 21.6**
    - **Property 35: Maksimum bildirim sayısı**
    - **Validates: Requirements 21.8**

- [x] 10. WebSocket Gerçek Zamanlı Veri Akışı
  - [x] 10.1 Backend WebSocket server implementasyonu
    - Flask-SocketIO veya FastAPI WebSocket kurulumu
    - WebSocket event handler'ları oluştur
    - Broadcast mekanizması (tüm client'lara gönderme)
    - _Requirements: 16.1_
  
  - [x] 10.2 Frontend WebSocket client implementasyonu
    - Socket.IO client veya native WebSocket bağlantısı
    - Event listener'lar (market_update, indicator_update, vb.)
    - Otomatik yeniden bağlanma mekanizması
    - _Requirements: 16.1_
  
  - [x] 10.3 Gerçek zamanlı veri güncelleme entegrasyonu
    - Piyasa verisi güncellemelerini frontend'e ilet
    - İndikatör güncellemelerini frontend'e ilet
    - Bakiye güncellemelerini frontend'e ilet
    - Bot durumu değişikliklerini frontend'e ilet
    - _Requirements: 16.1, 18.3_

- [x] 11. Manuel Kontrol Paneli İyileştirmeleri (spot.html)
  - [x] 11.1 Kontrol paneli layout modernizasyonu
    - Bot aktif/pasif toggle butonu (büyük ve belirgin)
    - Manuel AL/SAT butonları (renk kodlu, büyük)
    - Miktar girişi (input validation ile)
    - Acil durdurma butonu (kırmızı, belirgin)
    - Mod seçici (Testnet/Live Trading)
    - _Requirements: 6.3, 6.4, 6.5, 6.6_
  
  - [x] 11.2 Anlık bilgi göstergeleri
    - Mevcut bakiye göstergesi
    - Anlık piyasa fiyatı göstergesi
    - Son işlem bilgisi
    - _Requirements: 6.1, 6.2_
  
  - [x] 11.3 Manuel işlem onay ve geri bildirim
    - İşlem öncesi onay modal'ı
    - İşlem sonrası bildirim (toast)
    - Loading state göstergeleri
    - _Requirements: 6.5, 6.6_

- [x] 12. Responsive Tasarım ve Mobil Optimizasyon
  - [x] 12.1 Mobil görünüm optimizasyonları
    - Tüm sayfalar için mobil layout'lar
    - Touch-friendly buton boyutları
    - Hamburger menü implementasyonu
    - Mobil grafik optimizasyonları
    - _Requirements: 16.5_
  
  - [x] 12.2 Tablet görünüm optimizasyonları
    - Orta ekran boyutları için layout ayarları
    - Grid column sayısı ayarlamaları
    - _Requirements: 16.5_
  
  - [ ]* 12.3 Responsive tasarım için property test
    - **Property 26: Responsive tasarım**
    - **Validates: Requirements 16.5**
    - Farklı ekran boyutlarında kullanılabilirlik doğrulaması

- [x] 13. Erişilebilirlik ve Kullanıcı Deneyimi İyileştirmeleri
  - [x] 13.1 Erişilebilirlik standartları uygulama
    - WCAG 2.1 uyumlu kontrast oranları
    - ARIA etiketleri ekle
    - Klavye navigasyonu desteği
    - Screen reader uyumluluğu
    - _Requirements: 16.8_
  
  - [x] 13.2 Loading ve skeleton state'ler
    - Veri yüklenirken skeleton loader'lar göster
    - Loading spinner'lar ekle
    - Smooth transition animasyonları
    - _Requirements: 16.6, 16.7_

- [x] 14. Checkpoint - Temel UI İyileştirmeleri Tamamlandı
  - Tüm sayfaların modern tasarımla güncellendiğini doğrula
  - Dark/light mode'un tüm sayfalarda çalıştığını test et
  - Responsive tasarımın mobil, tablet, desktop'ta çalıştığını doğrula
  - WebSocket bağlantısının gerçek zamanlı veri ilettiğini test et
  - Ensure all tests pass, ask the user if questions arise.

- [x] 15. Performans Optimizasyonları
  - [x] 15.1 Frontend performans iyileştirmeleri
    - Debouncing ile gereksiz render'ları önle
    - Virtual scrolling için büyük listeler (işlem geçmişi)
    - Lazy loading için görsel varlıklar
    - CSS ve JavaScript minification
    - _Requirements: 15.1, 15.2, 15.3, 15.4_
  
  - [x] 15.2 Grafik performans optimizasyonları
    - Canvas rendering optimizasyonu
    - Veri noktası sınırlaması (max 1000 nokta)
    - Grafik güncelleme throttling
    - _Requirements: 15.2_

- [x] 16. Entegrasyon ve Wiring
  - [x] 16.1 Backend API endpoint'leri ile frontend entegrasyonu
    - Tüm REST API endpoint'lerini frontend'e bağla
    - Error handling ve retry mekanizmaları ekle
    - API response validation
    - _Requirements: 16.1_
  
  - [x] 16.2 WebSocket event'leri ile UI bileşenleri entegrasyonu
    - Market update event'i → grafik güncelleme
    - Indicator update event'i → indikatör paneli güncelleme
    - Balance update event'i → bakiye göstergesi güncelleme
    - Order executed event'i → bildirim gösterme
    - _Requirements: 16.1_
  
  - [x] 16.3 Theme persistence ve state management
    - LocalStorage ile kullanıcı tercihlerini kaydet
    - Sayfa yenilendiğinde state'i geri yükle
    - _Requirements: 16.2_

- [x] 17. Final Checkpoint - Tüm Özellikler Entegre
  - Tüm sayfaların birbirine bağlı çalıştığını doğrula
  - Gerçek zamanlı veri akışının tüm bileşenlerde çalıştığını test et
  - Manuel işlemlerin baştan sona çalıştığını doğrula
  - Bildirimlerin doğru zamanlarda gösterildiğini test et
  - Tüm responsive breakpoint'lerde test et
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Mevcut template dosyaları (index.html, indicators.html, portfolio.html, spot.html) modernize edilecek
- CSS dosyaları `static/css/` dizininde organize edilecek
- JavaScript dosyaları `static/js/` dizininde organize edilecek
- Grafik kütüphanesi olarak TradingView Lightweight Charts veya Chart.js kullanılacak
- WebSocket için Flask-SocketIO veya FastAPI WebSocket kullanılacak
- Tüm implementasyon Python backend ve vanilla JavaScript frontend ile yapılacak
