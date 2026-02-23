# Gereksinimler Dökümanı

## Giriş

Kripto Ticaret Otomasyon Sistemi, Binance kripto para borsasında 7/24 otomatik alım-satım yapabilen, duygulardan arınmış, tamamen matematiksel verilere ve stratejilere dayalı çalışan bir yazılım sistemidir. Sistem üç ana katmandan oluşur: Veri Toplama (piyasa verilerini okuma), Strateji ve Karar (teknik analiz ve sinyal üretimi), ve İşlem Yürütme (otomatik emir iletimi). Geliştirme süreci manuel kontrol panelinden başlayarak testnet simülasyonuna, ardından canlı piyasada tam otonom çalışmaya doğru ilerler.

## Sözlük

- **Trading_Bot**: Otomatik alım-satım kararları veren ve işlemleri yürüten yazılım sistemi
- **Binance_API**: Binance kripto para borsasının programatik erişim arayüzü
- **Market_Data_Collector**: Binance'ten fiyat, hacim ve piyasa verilerini toplayan bileşen
- **Strategy_Engine**: Teknik indikatörleri hesaplayarak alım-satım sinyalleri üreten bileşen
- **Order_Executor**: Borsa hesabına emir gönderen ve işlemleri yürüten bileşen
- **Technical_Indicator**: Fiyat ve hacim verilerinden matematiksel formüllerle hesaplanan sinyal (RSI, MACD, Bollinger Bands, vb.)
- **Trading_Signal**: Strategy_Engine tarafından üretilen AL, SAT veya BEKLİ kararı
- **Testnet**: Binance'in gerçek para kullanmadan test yapılabilen simülasyon ortamı
- **Live_Trading**: Gerçek para ile canlı piyasada işlem yapma modu
- **Manual_Control_Panel**: Kullanıcının web arayüzü üzerinden manuel işlem yapabildiği kontrol paneli
- **Stop_Loss**: Kayıpları sınırlamak için belirlenen otomatik satış seviyesi
- **Trade_Log**: Gerçekleştirilen işlemlerin kaydını tutan veri deposu
- **Balance**: Kullanıcının borsa hesabındaki kripto para ve fiat para bakiyeleri
- **Order_Book**: Borsadaki alım-satım emirlerinin anlık durumu
- **Consensus_Score**: Birden fazla teknik indikatörün birleştirilmesiyle elde edilen toplam sinyal skoru
- **Bot_State**: Trading_Bot'un aktif veya pasif durumu
- **Web_Interface**: Kullanıcının sisteme eriştiği web tabanlı arayüz
- **Portfolio_View**: Kullanıcının varlıklarını ve portföy durumunu gösteren görünüm
- **Account_Panel**: Hesap bilgilerini ve önemli metrikleri gösteren panel
- **Chart_Component**: Fiyat hareketlerini ve teknik indikatörleri görselleştiren grafik bileşeni
- **Trade_History_View**: Geçmiş işlemleri ve logları gösteren görünüm
- **Notification_System**: Kullanıcıya önemli olayları bildiren sistem
- **Navigation_Bar**: Sayfalar arası geçiş için kullanılan navigasyon çubuğu
- **Page_Layout**: Sayfa düzeni ve içerik organizasyonu
- **Footer**: Sayfa alt bilgi bölümü

## Gereksinimler

### Gereksinim 1: Binance API Bağlantısı

**Kullanıcı Hikayesi:** Bir trader olarak, sistemin Binance borsasına güvenli şekilde bağlanmasını istiyorum, böylece piyasa verilerine erişebilir ve işlem yapabilirim.

#### Kabul Kriterleri

1. THE Market_Data_Collector SHALL Binance_API kullanarak kimlik doğrulaması yapabilmeli
2. WHEN API anahtarları geçersiz olduğunda, THE Trading_Bot SHALL hata mesajı döndürmeli ve işlem yapmamalı
3. THE Trading_Bot SHALL Binance Testnet ve Live_Trading ortamları arasında geçiş yapabilmeli
4. THE Binance_API SHALL saniye başına maksimum 1200 istek sınırını aşmamalı
5. WHEN API bağlantısı kesildiğinde, THE Trading_Bot SHALL otomatik yeniden bağlanma denemesi yapmalı

### Gereksinim 2: Piyasa Verisi Toplama

**Kullanıcı Hikayesi:** Bir trader olarak, sistemin gerçek zamanlı piyasa verilerini toplamasını istiyorum, böylece güncel bilgilere dayalı kararlar alınabilir.

#### Kabul Kriterleri

1. THE Market_Data_Collector SHALL seçilen kripto para çifti için anlık fiyat verilerini toplamalı
2. THE Market_Data_Collector SHALL en az 1 saniyelik aralıklarla piyasa verilerini güncellemeli
3. WHEN piyasa verisi alındığında, THE Market_Data_Collector SHALL fiyat, hacim, yüksek ve düşük değerlerini kaydetmeli
4. THE Market_Data_Collector SHALL Order_Book verilerini alabilmeli
5. THE Market_Data_Collector SHALL toplanan verileri zaman damgasıyla birlikte saklamalı

### Gereksinim 3: Teknik İndikatör Hesaplama

**Kullanıcı Hikayesi:** Bir trader olarak, sistemin teknik analiz indikatörlerini hesaplamasını istiyorum, böylece matematiksel sinyallere dayalı kararlar alınabilir.

#### Kabul Kriterleri

1. THE Strategy_Engine SHALL RSI (Relative Strength Index) indikatörünü hesaplamalı
2. THE Strategy_Engine SHALL MACD (Moving Average Convergence Divergence) indikatörünü hesaplamalı
3. THE Strategy_Engine SHALL Bollinger Bands indikatörünü hesaplamalı
4. THE Strategy_Engine SHALL Stochastic Oscillator indikatörünü hesaplamalı
5. THE Strategy_Engine SHALL ADX (Average Directional Index) indikatörünü hesaplamalı
6. THE Strategy_Engine SHALL EMA (Exponential Moving Average) indikatörünü hesaplamalı
7. THE Strategy_Engine SHALL SuperTrend indikatörünü hesaplamalı
8. WHEN yetersiz veri olduğunda, THE Strategy_Engine SHALL indikatör hesaplamasını atlayarak hata vermemeli

### Gereksinim 4: Ticaret Sinyali Üretimi

**Kullanıcı Hikayesi:** Bir trader olarak, sistemin teknik indikatörlerden alım-satım sinyalleri üretmesini istiyorum, böylece otomatik işlem kararları alınabilir.

#### Kabul Kriterleri

1. THE Strategy_Engine SHALL hesaplanan Technical_Indicator değerlerinden Consensus_Score üretmeli
2. WHEN Consensus_Score pozitif eşik değerini aştığında, THE Strategy_Engine SHALL AL sinyali üretmeli
3. WHEN Consensus_Score negatif eşik değerini aştığında, THE Strategy_Engine SHALL SAT sinyali üretmeli
4. WHEN Consensus_Score eşik değerleri arasında olduğunda, THE Strategy_Engine SHALL BEKLİ sinyali üretmeli
5. THE Strategy_Engine SHALL her sinyal için güven seviyesi (confidence score) hesaplamalı
6. THE Strategy_Engine SHALL üretilen sinyalleri zaman damgasıyla birlikte Trade_Log'a kaydetmeli

### Gereksinim 5: Otomatik Emir İletimi

**Kullanıcı Hikayesi:** Bir trader olarak, sistemin üretilen sinyallere göre otomatik emir göndermesini istiyorum, böylece hızlı ve disiplinli işlem yapılabilir.

#### Kabul Kriterleri

1. WHEN AL sinyali üretildiğinde ve Bot_State aktif olduğunda, THE Order_Executor SHALL Binance_API üzerinden alım emri göndermeli
2. WHEN SAT sinyali üretildiğinde ve Bot_State aktif olduğunda, THE Order_Executor SHALL Binance_API üzerinden satım emri göndermeli
3. THE Order_Executor SHALL emir miktarını Balance'a göre hesaplamalı
4. THE Order_Executor SHALL gönderilen her emri Trade_Log'a kaydetmeli
5. WHEN emir başarısız olduğunda, THE Order_Executor SHALL hata detaylarını Trade_Log'a kaydetmeli
6. THE Order_Executor SHALL piyasa emri (market order) ve limit emri (limit order) türlerini desteklemeli

### Gereksinim 6: Manuel Kontrol Paneli

**Kullanıcı Hikayesi:** Bir trader olarak, web arayüzü üzerinden sistemi kontrol edebilmek istiyorum, böylece gerektiğinde manuel müdahale yapabilirim.

#### Kabul Kriterleri

1. THE Manual_Control_Panel SHALL kullanıcıya mevcut Balance bilgisini göstermeli
2. THE Manual_Control_Panel SHALL kullanıcıya anlık piyasa fiyatını göstermeli
3. THE Manual_Control_Panel SHALL kullanıcıya manuel AL butonu sunmalı
4. THE Manual_Control_Panel SHALL kullanıcıya manuel SAT butonu sunmalı
5. WHEN manuel AL butonuna basıldığında, THE Order_Executor SHALL belirtilen miktarda alım emri göndermeli
6. WHEN manuel SAT butonuna basıldığında, THE Order_Executor SHALL belirtilen miktarda satım emri göndermeli
7. THE Manual_Control_Panel SHALL hesaplanan Technical_Indicator değerlerini görselleştirmeli
8. THE Manual_Control_Panel SHALL Trade_Log geçmişini göstermeli

### Gereksinim 7: Bot Aktif/Pasif Kontrolü

**Kullanıcı Hikayesi:** Bir trader olarak, botun otomatik işlemlerini açıp kapayabilmek istiyorum, böylece tam kontrolü elimde tutabilirim.

#### Kabul Kriterleri

1. THE Trading_Bot SHALL Bot_State'i aktif veya pasif olarak ayarlayabilmeli
2. WHEN Bot_State pasif olduğunda, THE Order_Executor SHALL otomatik emir göndermemeli
3. WHEN Bot_State aktif olduğunda, THE Order_Executor SHALL Trading_Signal'lere göre otomatik emir gönderebilmeli
4. THE Manual_Control_Panel SHALL Bot_State'i değiştirmek için toggle butonu sunmalı
5. THE Trading_Bot SHALL Bot_State değişikliklerini Trade_Log'a kaydetmeli

### Gereksinim 8: Testnet Simülasyon Modu

**Kullanıcı Hikayesi:** Bir trader olarak, gerçek para riske atmadan stratejimi test edebilmek istiyorum, böylece güvenle geliştirme yapabilirim.

#### Kabul Kriterleri

1. THE Trading_Bot SHALL Binance Testnet ortamına bağlanabilmeli
2. WHEN Testnet modunda çalışırken, THE Trading_Bot SHALL gerçek Balance'ı etkilememeli
3. THE Trading_Bot SHALL Testnet ve Live_Trading modları arasında konfigürasyon ile geçiş yapabilmeli
4. THE Trading_Bot SHALL Testnet modunda tüm işlevleri Live_Trading moduyla aynı şekilde çalıştırmalı
5. THE Manual_Control_Panel SHALL aktif modu (Testnet veya Live_Trading) kullanıcıya göstermeli

### Gereksinim 9: İşlem Geçmişi ve Loglama

**Kullanıcı Hikayesi:** Bir trader olarak, geçmiş işlemleri ve bot aktivitelerini görebilmek istiyorum, böylece performansı analiz edebilirim.

#### Kabul Kriterleri

1. THE Trading_Bot SHALL her işlemi Trade_Log'a tarih, saat, işlem türü, miktar, fiyat ve toplam değer ile kaydetmeli
2. THE Trading_Bot SHALL üretilen Trading_Signal'leri Trade_Log'a kaydetmeli
3. THE Trading_Bot SHALL API hatalarını Trade_Log'a kaydetmeli
4. THE Manual_Control_Panel SHALL Trade_Log kayıtlarını kronolojik sırayla göstermeli
5. THE Trading_Bot SHALL Trade_Log verilerini kalıcı olarak saklamalı

### Gereksinim 10: Bakiye ve Portföy Yönetimi

**Kullanıcı Hikayesi:** Bir trader olarak, mevcut bakiyemi ve portföy durumumu görebilmek istiyorum, böylece varlıklarımı takip edebilirim.

#### Kabul Kriterleri

1. THE Trading_Bot SHALL Binance_API üzerinden güncel Balance bilgisini alabilmeli
2. THE Manual_Control_Panel SHALL kripto para ve fiat para bakiyelerini ayrı ayrı göstermeli
3. THE Manual_Control_Panel SHALL portföy toplam değerini hesaplayarak göstermeli
4. THE Trading_Bot SHALL Balance bilgisini en az 5 saniyelik aralıklarla güncellemeli
5. THE Manual_Control_Panel SHALL her coin için mevcut miktar ve değerini göstermeli

### Gereksinim 11: Hata Yönetimi ve Güvenlik

**Kullanıcı Hikayesi:** Bir trader olarak, sistemin hataları güvenli şekilde yönetmesini istiyorum, böylece beklenmedik kayıplar yaşamam.

#### Kabul Kriterleri

1. WHEN API hatası oluştuğunda, THE Trading_Bot SHALL işlemi iptal etmeli ve hata mesajını Trade_Log'a kaydetmeli
2. WHEN yetersiz Balance olduğunda, THE Order_Executor SHALL emir göndermemeli ve uyarı vermelidir
3. THE Trading_Bot SHALL API anahtarlarını güvenli şekilde saklamalı ve loglamamamalı
4. WHEN beklenmedik bir hata oluştuğunda, THE Trading_Bot SHALL Bot_State'i pasif konuma almalı
5. THE Trading_Bot SHALL her kritik işlem öncesi Balance doğrulaması yapmalı

### Gereksinim 12: Çoklu Coin Desteği (Gelecek Vizyon)

**Kullanıcı Hikayesi:** Bir trader olarak, birden fazla kripto para çiftinde aynı anda işlem yapabilmek istiyorum, böylece daha fazla fırsat değerlendirebilirim.

#### Kabul Kriterleri

1. WHERE çoklu coin özelliği aktif olduğunda, THE Trading_Bot SHALL birden fazla kripto para çifti için piyasa verisi toplayabilmeli
2. WHERE çoklu coin özelliği aktif olduğunda, THE Strategy_Engine SHALL her coin için bağımsız Trading_Signal üretmeli
3. WHERE çoklu coin özelliği aktif olduğunda, THE Order_Executor SHALL her coin için bağımsız emir gönderebilmeli
4. WHERE çoklu coin özelliği aktif olduğunda, THE Trading_Bot SHALL Balance'ı coinler arasında dağıtabilmeli
5. WHERE çoklu coin özelliği aktif olduğunda, THE Manual_Control_Panel SHALL tüm coinlerin durumunu ayrı ayrı göstermeli

### Gereksinim 13: Risk Yönetimi ve Stop Loss (Gelecek Vizyon)

**Kullanıcı Hikayesi:** Bir trader olarak, kayıplarımı sınırlamak için otomatik stop loss mekanizması istiyorum, böylece büyük kayıplardan korunabilirim.

#### Kabul Kriterleri

1. WHERE stop loss özelliği aktif olduğunda, THE Trading_Bot SHALL her pozisyon için Stop_Loss seviyesi belirlemeli
2. WHERE stop loss özelliği aktif olduğunda, WHEN fiyat Stop_Loss seviyesine ulaştığında, THE Order_Executor SHALL otomatik satış emri göndermeli
3. WHERE stop loss özelliği aktif olduğunda, THE Manual_Control_Panel SHALL kullanıcıya Stop_Loss yüzdesini ayarlama imkanı sunmalı
4. WHERE stop loss özelliği aktif olduğunda, THE Trading_Bot SHALL Stop_Loss tetiklenmelerini Trade_Log'a kaydetmeli
5. WHERE stop loss özelliği aktif olduğunda, THE Trading_Bot SHALL maksimum pozisyon büyüklüğünü Balance'ın belirli bir yüzdesiyle sınırlamalı

### Gereksinim 14: Adaptif Strateji Geliştirme (Gelecek Vizyon)

**Kullanıcı Hikayesi:** Bir trader olarak, botun geçmiş performansından öğrenerek stratejisini geliştirmesini istiyorum, böylece zamanla daha iyi sonuçlar elde edebilirim.

#### Kabul Kriterleri

1. WHERE adaptif strateji özelliği aktif olduğunda, THE Strategy_Engine SHALL geçmiş Trade_Log verilerini analiz edebilmeli
2. WHERE adaptif strateji özelliği aktif olduğunda, THE Strategy_Engine SHALL başarılı ve başarısız işlemleri karşılaştırabilmeli
3. WHERE adaptif strateji özelliği aktif olduğunda, THE Strategy_Engine SHALL Technical_Indicator ağırlıklarını performansa göre ayarlayabilmeli
4. WHERE adaptif strateji özelliği aktif olduğunda, THE Strategy_Engine SHALL Consensus_Score eşik değerlerini optimize edebilmeli
5. WHERE adaptif strateji özelliği aktif olduğunda, THE Trading_Bot SHALL strateji değişikliklerini Trade_Log'a kaydetmeli

### Gereksinim 15: Performans ve Hız Optimizasyonu

**Kullanıcı Hikayesi:** Bir trader olarak, sistemin milisaniyeler içinde işlem yapabilmesini istiyorum, böylece piyasa fırsatlarını kaçırmam.

#### Kabul Kriterleri

1. THE Market_Data_Collector SHALL piyasa verisini 1 saniyeden kısa sürede alabilmeli
2. THE Strategy_Engine SHALL Technical_Indicator hesaplamalarını 500 milisaniyeden kısa sürede tamamlamalı
3. THE Order_Executor SHALL emir iletimini 1 saniyeden kısa sürede gerçekleştirmeli
4. THE Trading_Bot SHALL veri toplama, analiz ve emir iletimi döngüsünü toplam 3 saniyeden kısa sürede tamamlamalı
5. THE Trading_Bot SHALL 7/24 kesintisiz çalışabilmeli

### Gereksinim 16: Profesyonel Web Arayüzü ve Kullanıcı Deneyimi

**Kullanıcı Hikayesi:** Bir trader olarak, modern ve profesyonel bir web arayüzü kullanmak istiyorum, böylece bilgilere hızlıca erişebilir ve rahat bir şekilde işlem yapabilirim.

#### Kabul Kriterleri

1. THE Web_Interface SHALL modern ve responsive tasarım prensiplerine uygun olarak görüntülenmeli
2. THE Web_Interface SHALL koyu tema (dark mode) ve açık tema (light mode) seçenekleri sunmalı
3. THE Web_Interface SHALL profesyonel kripto borsalarının (Binance, Coinbase Pro) tasarım standartlarına uygun renk paleti kullanmalı
4. THE Web_Interface SHALL tüm sayfalarda tutarlı tipografi ve görsel hiyerarşi sağlamalı
5. WHEN kullanıcı farklı cihazlardan eriştiğinde, THE Web_Interface SHALL mobil, tablet ve masaüstü ekranlara uyumlu görüntülenmeli
6. THE Web_Interface SHALL yükleme durumları için animasyonlu göstergeler (loading spinners) sunmalı
7. THE Web_Interface SHALL kullanıcı etkileşimleri için görsel geri bildirim (hover effects, transitions) sağlamalı
8. THE Web_Interface SHALL erişilebilirlik standartlarına (WCAG 2.1) uygun kontrast oranları kullanmalı

### Gereksinim 17: Gelişmiş Portföy Görünümü

**Kullanıcı Hikayesi:** Bir trader olarak, portföyümü detaylı ve görsel olarak çekici bir şekilde görmek istiyorum, böylece varlıklarımı daha iyi takip edebilirim.

#### Kabul Kriterleri

1. THE Portfolio_View SHALL her coin için güncel fiyat, miktar, toplam değer ve yüzde değişimi göstermeli
2. THE Portfolio_View SHALL portföy dağılımını pasta grafik (pie chart) veya halka grafik (donut chart) ile görselleştirmeli
3. THE Portfolio_View SHALL toplam portföy değerini büyük ve belirgin şekilde göstermeli
4. THE Portfolio_View SHALL günlük, haftalık ve aylık kar/zarar istatistiklerini göstermeli
5. THE Portfolio_View SHALL her coin için renk kodlu performans göstergeleri (yeşil: artış, kırmızı: düşüş) kullanmalı
6. THE Portfolio_View SHALL portföy değerinin zaman içindeki değişimini çizgi grafik ile göstermeli
7. THE Portfolio_View SHALL her coin için hızlı işlem butonları (AL/SAT) sunmalı
8. WHEN portföy verisi güncellendiğinde, THE Portfolio_View SHALL yumuşak geçiş animasyonları ile güncellemeli

### Gereksinim 18: Gelişmiş Hesap Bilgileri Paneli

**Kullanıcı Hikayesi:** Bir trader olarak, hesap bilgilerimi ve önemli metrikleri tek bakışta görmek istiyorum, böylece durumu hızlıca değerlendirebilirim.

#### Kabul Kriterleri

1. THE Account_Panel SHALL toplam bakiye, kullanılabilir bakiye ve kilitli bakiye bilgilerini ayrı ayrı göstermeli
2. THE Account_Panel SHALL hesap durumunu (Testnet/Live Trading) belirgin şekilde göstermeli
3. THE Account_Panel SHALL API bağlantı durumunu gerçek zamanlı olarak göstermeli
4. THE Account_Panel SHALL günlük işlem sayısı ve toplam işlem hacmi istatistiklerini göstermeli
5. THE Account_Panel SHALL Bot_State durumunu (Aktif/Pasif) görsel olarak belirgin şekilde göstermeli
6. THE Account_Panel SHALL son işlem zamanını ve bir sonraki analiz zamanını göstermeli
7. THE Account_Panel SHALL hesap güvenlik durumu ve API izinlerini göstermeli
8. THE Account_Panel SHALL önemli bilgileri kart (card) bileşenleri ile düzenli şekilde gruplandırmalı

### Gereksinim 19: İnteraktif Grafik ve Veri Görselleştirme

**Kullanıcı Hikayesi:** Bir trader olarak, fiyat hareketlerini ve teknik indikatörleri interaktif grafiklerle görmek istiyorum, böylece piyasayı daha iyi analiz edebilirim.

#### Kabul Kriterleri

1. THE Chart_Component SHALL gerçek zamanlı fiyat hareketlerini çizgi grafik veya mum grafik (candlestick) ile göstermeli
2. THE Chart_Component SHALL Technical_Indicator değerlerini ana grafik üzerinde veya alt panellerde göstermeli
3. THE Chart_Component SHALL kullanıcının zaman aralığını (1m, 5m, 15m, 1h, 4h, 1d) seçmesine izin vermeli
4. THE Chart_Component SHALL grafik üzerinde zoom ve pan (kaydırma) işlevlerini desteklemeli
5. THE Chart_Component SHALL fare ile grafik üzerinde gezinirken detaylı bilgi (tooltip) göstermeli
6. THE Chart_Component SHALL AL ve SAT sinyallerini grafik üzerinde işaretlemeli
7. THE Chart_Component SHALL grafik verilerini otomatik olarak güncellemeli
8. THE Chart_Component SHALL profesyonel grafik kütüphanesi (Chart.js, Plotly, TradingView) kullanmalı

### Gereksinim 20: Gelişmiş İşlem Geçmişi ve Log Görünümü

**Kullanıcı Hikayesi:** Bir trader olarak, işlem geçmişimi ve sistem loglarını düzenli ve filtrelenebilir şekilde görmek istiyorum, böylece performansı analiz edebilirim.

#### Kabul Kriterleri

1. THE Trade_History_View SHALL işlemleri tablo formatında tarih, saat, tip, coin, miktar, fiyat ve durum sütunları ile göstermeli
2. THE Trade_History_View SHALL işlemleri tarihe, tipe veya coin'e göre filtreleme imkanı sunmalı
3. THE Trade_History_View SHALL başarılı ve başarısız işlemleri farklı renklerle göstermeli
4. THE Trade_History_View SHALL sayfalama (pagination) özelliği sunmalı
5. THE Trade_History_View SHALL her işlem için detay görüntüleme seçeneği sunmalı
6. THE Trade_History_View SHALL işlem geçmişini CSV veya JSON formatında dışa aktarma imkanı sunmalı
7. THE Trade_History_View SHALL toplam kar/zarar özetini göstermeli
8. THE Trade_History_View SHALL arama (search) özelliği sunmalı

### Gereksinim 21: Bildirim ve Uyarı Sistemi

**Kullanıcı Hikayesi:** Bir trader olarak, önemli olaylar hakkında görsel bildirimler almak istiyorum, böylece kritik durumlardan haberdar olabilirim.

#### Kabul Kriterleri

1. WHEN işlem başarıyla tamamlandığında, THE Notification_System SHALL başarı bildirimi (success toast) göstermeli
2. WHEN işlem başarısız olduğunda, THE Notification_System SHALL hata bildirimi (error toast) göstermeli
3. WHEN API bağlantısı kesildiğinde, THE Notification_System SHALL uyarı bildirimi (warning toast) göstermeli
4. WHEN Bot_State değiştiğinde, THE Notification_System SHALL bilgi bildirimi (info toast) göstermeli
5. THE Notification_System SHALL bildirimleri ekranın sağ üst köşesinde göstermeli
6. THE Notification_System SHALL bildirimleri 5 saniye sonra otomatik olarak kapatmalı
7. THE Notification_System SHALL kullanıcının bildirimi manuel olarak kapatmasına izin vermeli
8. THE Notification_System SHALL aynı anda maksimum 3 bildirim göstermeli

### Gereksinim 22: Navigasyon ve Sayfa Düzeni

**Kullanıcı Hikayesi:** Bir trader olarak, sayfalar arasında kolay geçiş yapabilmek ve tutarlı bir düzen görmek istiyorum, böylece sistemi rahatça kullanabilirim.

#### Kabul Kriterleri

1. THE Navigation_Bar SHALL tüm sayfalarda sabit (sticky) konumda kalmalı
2. THE Navigation_Bar SHALL ana sayfa, portföy, indikatörler ve spot işlemler bağlantılarını içermeli
3. THE Navigation_Bar SHALL aktif sayfayı görsel olarak vurgulamalı
4. THE Navigation_Bar SHALL sistem logosunu ve adını göstermeli
5. THE Page_Layout SHALL tutarlı kenar boşlukları (margins) ve iç boşluklar (padding) kullanmalı
6. THE Page_Layout SHALL içeriği maksimum genişlik sınırı ile merkezde konumlandırmalı
7. THE Page_Layout SHALL sayfa başlıklarını ve alt başlıkları hiyerarşik olarak göstermeli
8. THE Footer SHALL telif hakkı bilgisi ve versiyon numarasını göstermeli
