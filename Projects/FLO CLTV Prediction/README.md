# FLO CLTV Prediction

Customer Lifetime Value (CLTV) tahminlemesi için BG-NBD ve Gamma-Gamma probabilistik modellerini kullanan bir proje.

## Proje Tanımı

FLO, satış ve pazarlama faaliyetleri için orta-uzun vadeli bir roadmap oluşturmak istemektedir. Bu amaçla, mevcut müşterilerin gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.

Bu proje, 2020-2021 yıllarında OmniChannel (online ve offline) alışveriş yapan müşterilerin geçmiş davranışlarını analiz ederek, 6 aylık dönem için CLTV değerlerini hesaplamaktadır.

## Veri Seti

**Kaynak:** FLO müşteri verisi (20.000 müşteri)

### Veri Seti Özelliği

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
- Aykırı değerlerin (outlier) tespiti ve baskılanması
- Online ve offline verilerinin birleştirilmesi
- Tarih formatının düzeltilmesi

### 2. CLTV Veri Yapısı Oluşturma
Aşağıdaki metriklerin hesaplanması:
- **Recency (R):** Son alışverişten bu yana geçen süre (hafta cinsinden)
- **Frequency (F):** Tekrarlama alışveriş sayısı
- **T:** Müşteri yaşı (ilk alışverişten bu yana geçen süre)
- **Monetary (M):** Alışveriş başına ortalama harcama

### 3. BG/NBD Modeli
**Beta Geometric/Negative Binomial Distribution** modeli:
- Müşteri davranışının olasılık dağılımını öğrenir
- 3 ay ve 6 ay içindeki beklenen satın alma sayısını tahminler

### 4. Gamma-Gamma Modeli
- Müşterilerin ortalama bırakacakları değeri tahminler
- Satın alma miktarının dağılımını modellendirir

### 5. CLTV Hesaplaması
6 aylık müşteri yaşam değeri:
```
CLTV = Expected Transaction Count × Expected Average Value
```

### 6. Segmentasyon
Müşteriler CLTV değerine göre 4 segmente ayrılır:
- **A Segmenti:** En yüksek değerli müşteriler
- **B Segmenti:** Yüksek değerli müşteriler
- **C Segmenti:** Orta değerli müşteriler
- **D Segmenti:** Düşük değerli müşteriler

## Çıktılar

### Temel Metrikleri
- 3 aylık beklenen satın alma sayısı
- 6 aylık beklenen satın alma sayısı
- Beklenen ortalama satın alma değeri
- 6 aylık CLTV değeri
- Müşteri segmenti

### Dosyalar
- **FLO_CLTV_Prediction.py:** Ana analiz kodları
- **cltv_prediction.csv:** Tahmin sonuçları ve segmentasyonu içeren çıktı dosyası

## Kullanılan Kütüphaneler

```python
- pandas: Veri manipülasyonu
- lifetimes: BG/NBD ve Gamma-Gamma modelleri
- scikit-learn: Veri ölçeklendirmesi
- matplotlib: Görselleştirme
```

## Kurulum

```bash
# Gerekli kütüphaneleri yükleyin
pip install pandas lifetimes scikit-learn matplotlib

# Projeyi çalıştırın
python FLO_CLTV_Prediction.py
```

## İş Öneriler

### A Segmenti (En Değerli Müşteriler)
- Personalized marketing kampanyaları yapın
- VIP müşteri programı oluşturun
- Ürün ve hizmet geliştirmelerinde feedback alın
- Özel indirim ve tekliflerle bağlılığı artırın

### B Segmenti (Yüksek Değerli Müşteriler)
- A segmentine yükseltme potansiyeli vardır
- Ürün cross-selling ve upselling fırsatları değerlendirin
- Düzenli iletişim kurarak ilişkiyi güçlendirin
- Loyalty programlarıyla katılımı teşvik edin

## Sonuçlar Örneği

```
En Değerli 20 Müşteri:
Sıra    Müşteri ID    CLTV Değeri
1       12345         5.432,50 ₺
2       67890         4.891,25 ₺
...
```

## Lisans

Bu proje eğitim amaçlıdır.

## İletişim

Sorularınız için lütfen iletişime geçin.
