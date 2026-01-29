# FLO RFM Müşteri Segmentasyonu

RFM (Recency, Frequency, Monetary) analiziyle müşterileri segmentlere ayıran ve hedefli pazarlama stratejileri geliştiren bir proje.

## Proje Tanımı

FLO, müşteri davranışlarını analiz ederek pazarlama stratejileri belirlemek istemektedir. Bu projede, müşteri segmentasyonu yapılarak her segment için özelleştirilmiş marketing kampanyaları oluşturulmaktadır.

2020-2021 yıllarında OmniChannel (online ve offline) alışveriş yapan 20.000 müşterinin verisi kullanılarak RFM analizi gerçekleştirilmektedir.

## Veri Seti

**Kaynak:** FLO müşteri verisi (20.000 müşteri)

### Veri Seti Özellikleri

- **master_id:** Eşsiz müşteri numarası
- **order_channel:** Alışveriş yapılan platform kanalı (Android, iOS, Desktop, Mobile, Offline)
- **last_order_channel:** En son alışverişin yapıldığı kanal
- **first_order_date:** İlk alışveriş tarihi
- **last_order_date:** Son alışveriş tarihi
- **last_order_date_online:** Online platformda son alışveriş tarihi
- **last_order_date_offline:** Offline platformda son alışveriş tarihi
- **order_num_total_ever_online:** Online platformda toplam alışveriş sayısı
- **order_num_total_ever_offline:** Offline platformda toplam alışveriş sayısı
- **customer_value_total_ever_online:** Online alışverişlerde ödenen toplam tutar
- **customer_value_total_ever_offline:** Offline alışverişlerde ödenen toplam tutar
- **interested_in_categories_12:** Son 12 ayda alışveriş yapılan kategoriler

## Metodoloji

### 1. Veri Hazırlama
- Omnichannel müşterilerin online ve offline verilerinin birleştirilmesi
- Tarih formatının düzeltilmesi
- Toplam alışveriş sayısı ve harcamalarının hesaplanması

### 2. RFM Metriklerinin Hesaplanması

**Recency (R):** Müşterinin son alışverişten bu yana geçen süre (gün cinsinden)
- Daha düşük değer = Daha aktif/yakın tarihte alışveriş yapan müşteri

**Frequency (F):** Belirli dönemde müşterinin yaptığı alışveriş sayısı
- Daha yüksek = Daha sık alışveriş yapan müşteri

**Monetary (M):** Belirli dönemde müşterinin toplam harcaması
- Daha yüksek = Daha yüksek değerli müşteri

### 3. RFM Skorlama
Recency, Frequency ve Monetary metrikleri 5 seviyeli skorlara dönüştürülür:
- Recency: 5 (en yakın) → 1 (en uzak)
- Frequency: 1 (en az) → 5 (en çok)
- Monetary: 1 (en düşük) → 5 (en yüksek)

### 4. Müşteri Segmentleri

Oluşturulan 10 segment ve özellikleri:

| Segment | Özellik | Aksiyon |
|---------|---------|--------|
| **Champions** | Yüksek Recency, Frequency, Monetary | VIP muamele, özel teklifler |
| **Loyal Customers** | Yüksek Frequency ve Monetary | Loyalty programı, ekstra faydalar |
| **Potential Loyalists** | Yüksek Monetary, orta Frequency | Upsell, cross-sell fırsatları |
| **Promising** | Yüksek Recency, düşük Frequency | Teşvik kampanyaları |
| **New Customers** | Yüksek Recency | Hoş geldin bonusu, onboarding |
| **Need Attention** | Orta metrikler | Personalized offers, engagement |
| **About to Sleep** | Düşük Frequency, düşük Recency | Re-engagement kampanyaları |
| **At Risk** | Düşük Recency, orta/yüksek Frequency | Geri kazanma kampanyaları |
| **Can't Loose** | Düşük Recency, yüksek Frequency/Monetary | Acil müşteri geri kazanma |
| **Hibernating** | Çok düşük metrikler | Win-back kampanyaları |

### 5. Hedefli Marketing Uygulamaları

#### Case 1: Yeni Marka Tanıtımı (Kadın Ayakkabı)
Hedef Segment Özellikleri:
- Monetary > 250 ₺
- KADIN kategorisinden alışveriş yapan
- Champions veya Loyal Customers segmentinde

**Aksiyon:** Özel müşteri id'leri `yeni_marka_hedef_müşteri_id.csv` dosyasında kaydedilir

#### Case 2: İndirim Kampanyası (Erkek & Çocuk)
Hedef Segment Özellikleri:
- Can't Loose, About to Sleep veya New Customers segmentinde
- %40'a yakın indirim sunulacak

**Aksiyon:** Hedef müşteri id'leri `indirim_hedef_müşteri_ids.csv` dosyasında kaydedilir

## Dosya Yapısı

```
├── FLO_RFM.py                          # Ana analiz kodu
├── flo_data_20k.csv                   # İnput veri seti
├── yeni_marka_hedef_müşteri_id.csv    # Case 1: Yeni marka hedef müşterileri
├── indirim_hedef_müşteri_ids.csv      # Case 2: İndirim hedef müşterileri
└── README.md                          # Bu dosya
```


## Örnek Çıktılar

### Segment Özeti
```
Segment                  Recency (ort) | Frequency (ort) | Monetary (ort)
champions                        10.5  |           8.3   |    1,250 ₺
loyal_customers                  15.2  |           6.8   |     950 ₺
potential_loyalists              20.1  |           4.2   |     800 ₺
...
```

### Hedef Müşteri Sayıları
```
Case 1 (Yeni Marka):      ~2,500 müşteri
Case 2 (İndirim):         ~5,800 müşteri
```

## Iş Önerileri

### Champions ve Loyal Customers için
- Özel VIP programı oluşturun
- Erken erişim (early access) önerimleri yapın
- Kişiselleştirilmiş ürün tavsiyesi verin
- Yüksek değerli işbirlik fırsatları sunun

### At Risk ve Can't Loose Müşteriler için
- Acil geri kazanma kampanyaları başlatın
- Özel indirim ve promosyon kodları gönderip
- Satın alma nedenlerini anlamak için anketler yapın
- Müşteri hizmeti ile doğrudan iletişim kurun

### New Customers için
- Hoş geldin bonusu ve special offer'lar sunun
- Onboarding email serileri gönderin
- İlk alışverişte teşvik sağlayın
- Ürün önerileri ve ipuçları sunun

### About to Sleep Müşteriler için
- Nostalji-tabanlı marketing yapın
- Yeni ürünleri tanıtarak ilgi uyandırın
- Flash sale ve limited-time offers kullanın

## Başarı Metrikleri

Uygulanacak kampanyaların başarısını ölçmek için:
- Segment başına conversion rate
- Müşteri yeniden aktivasyon oranı
- Ortalama sepet tutarındaki değişim
- Müşteri yaşam süresi (customer lifetime value)

## İletişim

Sorularınız ve önerileriniz için lütfen iletişime geçin.

## Lisans

Bu proje eğitim amaçlıdır.
