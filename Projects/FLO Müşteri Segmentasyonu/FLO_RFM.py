
###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

##############################################################################################################################

###############################################################
# AŞAMA 1: Veriyi  Hazırlama ve Anlama (Data Understanding)
###############################################################

# 1. flo_data_20K.csv verisini okutalım.

import datetime as dt
import pandas as pd
from pandas import DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)

df_ = pd.read_csv("Projects/FLO Müşteri Segmentasyonu/flo_data_20k.csv")
df = df_.copy()

# 2. Veri setinde
        # a. İlk 10 gözlem,
df.head(10)

        # b. Değişken isimleri,
df.columns

        # c. Boyut,
df.shape

        # d. Betimsel istatistik,
df.describe()

        # e. Boş değer,
df.isnull().sum()

        # f. Değişken tiplerinin incelenmesi
df.dtypes


# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturuyoruz.
df["orner_num_total_ever_omnichannel"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total_ever_omnichannel"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]


# 4. Değişken tiplerini inceleyip, tarih ifade eden değişkenlerin tipini date'e çeviriyoruz.
df.dtypes
date_columns = [col for col in df.columns if "date" in col]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
# veya
# df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)


# 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısı ve toplam harcamaların dağılımını incelemek için.
df.groupby("order_channel").agg({"order_num_total_ever_online" : ["sum","mean"],
                                            "order_num_total_ever_offline" : ["sum","mean"],
                                            "orner_num_total_ever_omnichannel" : ["sum","mean"],
                                            "customer_value_total_ever_offline" : ["sum","mean"],
                                            "customer_value_total_ever_online" : ["sum","mean"],
                                            "customer_value_total_ever_omnichannel" : ["sum","mean"]
                                            })


# 6. En fazla kazancı getiren ilk 10 müşteri.
top10_omni_value = df.sort_values(by="customer_value_total_ever_omnichannel", ascending=False).head(10)



# 7. En fazla siparişi veren ilk 10 müşteri.
top10_omni_order = df.sort_values(by="orner_num_total_ever_omnichannel", ascending=False).head(10)



# 8. Veri ön hazırlık sürecini fonksiyonlaştırıyoruz.
def predata(df):
    df["orner_num_total_ever_omnichannel"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["customer_value_total_ever_omnichannel"] = df["customer_value_total_ever_online"] + df[
        "customer_value_total_ever_offline"]
    date_columns = [col for col in df.columns if "date" in col]
    df[date_columns] = df[date_columns].apply(pd.to_datetime)

###############################################################
# AŞAMA 2: RFM Metriklerinin Hesaplanması
###############################################################

# Recency, Frequency ve Monetary tanımları.

# Recency (R): Müşterinin son satın alma işleminden analiz tarihine kadar geçen süre (genelde gün). Daha küçük = daha yeni/aktif
# Frequency (F): Belirli bir dönemde müşterinin yaptığı satın alma işlem sayısı (sipariş/adet). Daha yüksek = daha sık
# Monetary (M): Belirli bir dönemde müşterinin yaptığı toplam harcama (ciro) ya da bazen ortalama sepet tutarı. Daha yüksek = daha değerli

# Analiz tarihi, veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrası olarak kabul edilecektir.

today_date = df["last_order_date"].max() + pd.Timedelta(days=2)
type(today_date)

# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframei oluşturalım.

rfm = df.groupby('master_id').agg({'last_order_date': lambda last_order_date: (today_date - last_order_date.max()).days,
                                    'orner_num_total_ever_omnichannel': "first",
                                    'customer_value_total_ever_omnichannel': "first"})
rfm.columns = ["recency", "frequency", "monetary"]
rfm.describe().T


###############################################################
# AŞAMA 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
###############################################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi

rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
# 0-100, 0-20, 20-40, 40-60, 60-80, 80-100

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi

rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) +
                    rfm["monetary_score"].astype(str) +
                    rfm["frequency_score"].astype(str))

###############################################################
# AŞAMA 4: RF Skorlarının Segment Olarak Tanımlanması
###############################################################

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve  tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['RF_segment'] = rfm['RF_SCORE'].replace(seg_map,regex=True)

###############################################################
# AŞAMA 5: Aksiyon zamanı!
###############################################################

# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyelim.

rfm.groupby("RF_segment").agg({"recency" : ["mean","count"],
                                          "frequency" : ["mean","count"],
                                          "monetary" : ["mean","count"]})

# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulalım ve müşteri id'lerini csv ye kaydedelim.

merged_df = pd.merge(df, rfm, on="master_id", how="left")

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçilmek isteniliyor. Bu müşterilerin sadık  ve
# kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs
# olarak kaydediniz.

merged_df[(merged_df["monetary"] > 250) &
          (merged_df["interested_in_categories_12"].str.contains("KADIN")) &
          ((merged_df["RF_segment"] == "champions") | (merged_df["RF_segment"] == "loyal_customers"))]

yeni_marka_hedef_müşteri = merged_df[(merged_df["monetary"] > 250) &
          (merged_df["interested_in_categories_12"].str.contains("KADIN")) &
          ((merged_df["RF_segment"] == "champions") | (merged_df["RF_segment"] == "loyal_customers"))]

yeni_marka_hedef_müşteri_id = pd.DataFrame()
yeni_marka_hedef_müşteri_id["master_id"] = yeni_marka_hedef_müşteri["master_id"]

yeni_marka_hedef_müşteri_id.to_csv("yeni_marka_hedef_müşteri_id.csv")

# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.

merged_df[((merged_df["RF_segment"] == "cant_loose") | (merged_df["RF_segment"] == "about_to_sleep") | (merged_df["RF_segment"] == "new_customers"))]

indirim_hedef_müşteri = merged_df[((merged_df["RF_segment"] == "cant_loose") | (merged_df["RF_segment"] == "about_to_sleep") | (merged_df["RF_segment"] == "new_customers"))]

indirim_hedef_müşteri_ids = pd.DataFrame()
indirim_hedef_müşteri_ids["master_id"] = indirim_hedef_müşteri["master_id"]

indirim_hedef_müşteri_ids.to_csv("indirim_hedef_müşteri_ids.csv")

# AŞAMA 6: Tüm süreci fonksiyonlaştıralım.

def prerfm(df):
    df["orner_num_total_ever_omnichannel"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["customer_value_total_ever_omnichannel"] = df["customer_value_total_ever_online"] + df[
        "customer_value_total_ever_offline"]
    date_columns = [col for col in df.columns if "date" in col]
    df[date_columns] = df[date_columns].apply(pd.to_datetime)
    today_date = df["last_order_date"].max() + pd.Timedelta(days=2)

    rfm = df.groupby('master_id').agg({'last_order_date': lambda last_order_date: (today_date - last_order_date.max()).days,
         'orner_num_total_ever_omnichannel': "first",
         'customer_value_total_ever_omnichannel': "first"})
    rfm.columns = ["recency", "frequency", "monetary"]

    rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    # 0-100, 0-20, 20-40, 40-60, 60-80, 80-100

    rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

    rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

    rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) +
                       rfm['frequency_score'].astype(str))

    rfm["RFM_SCORE"] = (rfm["recency_score"].astype(str) +
                        rfm["monetary_score"].astype(str) +
                        rfm["frequency_score"].astype(str))


    seg_map = {
        r'[1-2][1-2]': 'hibernating',
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

    rfm['RF_segment'] = rfm['RF_SCORE'].replace(seg_map, regex=True)
    final_df = pd.merge(df, rfm, on="master_id", how="left")
    return final_df, rfm

