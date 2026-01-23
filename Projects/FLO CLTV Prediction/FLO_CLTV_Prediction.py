##############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
##############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO satış ve pazarlama faaliyetleri için roadmap belirlemek istemektedir.
# Şirketin orta uzun vadeli plan yapabilmesi için var olan müşterilerin gelecekte şirkete sağlayacakları potansiyel değerin tahmin edilmesi gerekmektedir.


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

###############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
###############################################################

import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
from sklearn.preprocessing import MinMaxScaler



# AŞAMA 1: Veriyi Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturuyoruz.
df_ = pd.read_csv("Projects/FLO CLTV Prediction/flo_data_20k.csv")
df = df_.copy()
df.head()
df.describe().T

           # 2. Aykırı değerleri baskılamak için gerekli olan outlier_thresholds ve replace_with_thresholds fonksiyonlarını tanımlayalım.
           # Not: cltv hesaplanırken frequency değerleri integer olması gerekmektedir.Bu nedenle alt ve üst limitlerini round() ile yuvarlıyoruz.

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    low_limit, up_limit = round(low_limit), round(up_limit)
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


           # 3. "order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online" değişkenlerinin
           # aykırı değerleri varsa baskılıyoruz.

outlier_thresholds(df, ["order_num_total_ever_online","order_num_total_ever_offline","customer_value_total_ever_offline","customer_value_total_ever_online"])
replace_with_thresholds(df, "order_num_total_ever_online")
replace_with_thresholds(df, "order_num_total_ever_offline")
replace_with_thresholds(df, "customer_value_total_ever_offline")
replace_with_thresholds(df, "customer_value_total_ever_online")

           # 4. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturuyoruz.

df["order_num_total_ever"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total_ever"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

           # 5. Değişken tiplerini inceleyip, tarih ifade eden değişkenlerin tipini date'e çeviriyoruz.
date_cols = [col for col in df.columns if "date" in col.lower()]
df[date_cols] = df[date_cols].apply(pd.to_datetime, errors="coerce")
df.dtypes

# AŞAMA 2: CLTV Veri Yapısının Oluşturulması
           # 1.Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihidir.

df["last_order_date"].max()
today_date = df["last_order_date"].max() + pd.Timedelta(days=2)

           # 2.customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturuyoruz.
           # Monetary değeri satın alma başına ortalama değer olarak, recency ve tenure değerleri ise haftalık cinsten ifade edilecek.

cltv_c = df.groupby('master_id').agg({'last_order_date': lambda last_order_date: (today_date - last_order_date.max()).days / 7,
                                     'first_order_date': lambda first_order_date : (today_date - first_order_date.min()).days / 7,
                                     'order_num_total_ever': ["sum"],
                                     'customer_value_total_ever': ["sum"]})

cltv_c.columns = cltv_c.columns.droplevel(1)

cltv_c.columns= ["recency_cltv_weekly", "T_weekly", "frequency", "monetary_cltv_avg"]

cltv_c["monetary_cltv_avg"] = cltv_c["monetary_cltv_avg"] / cltv_c["frequency"]
cltv_c = cltv_c[cltv_c["frequency"] > 1]

# AŞAMA 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması, CLTV'nin hesaplanması
           # 1. BG/NBD modelini fit ediniz.

bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv_c["frequency"],
        cltv_c["recency_cltv_weekly"],
        cltv_c["T_weekly"])

                # a. 3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_3_month olarak cltv dataframe'ine ekliyoruz.
cltv_c["exp_sales_3_month"] = bgf.predict(4 * 3,
                                              cltv_c["frequency"],
                                              cltv_c["recency_cltv_weekly"],
                                              cltv_c["T_weekly"])

                # b. 6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_6_month olarak cltv dataframe'ine ekliyoruz.
cltv_c["exp_sales_6_month"] = bgf.predict(4 * 6,
                                              cltv_c["frequency"],
                                              cltv_c["recency_cltv_weekly"],
                                              cltv_c["T_weekly"])
plot_period_transactions(bgf)
plt.show()

           # 2. Gamma-Gamma modelini fit ediniz. Müşterilerin ortalama bırakacakları değeri tahminleyip exp_average_value olarak cltv dataframe'ine ekliyoruz.
ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_c['frequency'], cltv_c["monetary_cltv_avg"])

cltv_c["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_c['frequency'],
                                                                             cltv_c["monetary_cltv_avg"])


           # 3. 6 aylık CLTV hesaplıyoruz ve cltv ismiyle dataframe'e ekliyoruz.
cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_c["frequency"],
                                   cltv_c["recency_cltv_weekly"],
                                   cltv_c["T_weekly"],
                                   cltv_c["exp_average_value"],
                                   time=6,  # 6 aylık
                                   freq="W",  # T'nin frekans bilgisi.
                                   discount_rate=0.01)

cltv.head()

cltv = cltv.reset_index()


cltv_final = cltv_c.merge(cltv, on="master_id", how="left")

                # b. Cltv değeri en yüksek 20 kişi
cltv_final.sort_values(by="clv", ascending=False).head(20)

# AŞAMA 4: CLTV'ye Göre Segmentlerin Oluşturulması
           # 1. 6 aylık tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz. cltv_segment ismi ile dataframe'e ekliyoruz.
cltv_final["cltv_segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

           # 2. 4 grup içerisinden seçeceğiniz 2 grup için yönetime kısa kısa 6 aylık aksiyon önerilerinde bulunalım.
cltv_final.groupby("cltv_segment").agg({
    "clv": ["mean", "min", "max", "sum"],
    "frequency": "mean",
    "monetary_cltv_avg": "mean",
    "recency_cltv_weekly": "mean",
    "T_weekly": "mean"
})

# AŞAMA 5: Tüm süreci fonksiyonlaştırma

def create_cltv_p(dataframe, month=3):
    replace_with_thresholds(df, "order_num_total_ever_online")
    replace_with_thresholds(df, "order_num_total_ever_offline")
    replace_with_thresholds(df, "customer_value_total_ever_offline")
    replace_with_thresholds(df, "customer_value_total_ever_online")

    df["order_num_total_ever"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["customer_value_total_ever"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

    date_cols = [col for col in df.columns if "date" in col.lower()]
    df[date_cols] = df[date_cols].apply(pd.to_datetime, errors="coerce")

    today_date = df["last_order_date"].max() + pd.Timedelta(days=2)

    cltv_c = df.groupby('master_id').agg(
        {'last_order_date': lambda last_order_date: (today_date - last_order_date.max()).days / 7,
         'first_order_date': lambda first_order_date: (today_date - first_order_date.min()).days / 7,
         'order_num_total_ever': ["sum"],
         'customer_value_total_ever': ["sum"]})

    cltv_c.columns = cltv_c.columns.droplevel(1)
    cltv_c.columns = ["recency_cltv_weekly", "T_weekly", "frequency", "monetary_cltv_avg"]
    cltv_c["monetary_cltv_avg"] = cltv_c["monetary_cltv_avg"] / cltv_c["frequency"]
    cltv_c = cltv_c[cltv_c["frequency"] > 1]

    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_c["frequency"],
            cltv_c["recency_cltv_weekly"],
            cltv_c["T_weekly"])

    cltv_c["exp_sales_3_month"] = bgf.predict(4 * 3,
                                              cltv_c["frequency"],
                                              cltv_c["recency_cltv_weekly"],
                                              cltv_c["T_weekly"])


    cltv_c["exp_sales_6_month"] = bgf.predict(4 * 6,
                                              cltv_c["frequency"],
                                              cltv_c["recency_cltv_weekly"],
                                              cltv_c["T_weekly"])

    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_c['frequency'], cltv_c["monetary_cltv_avg"])

    cltv_c["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_c['frequency'],
                                                                          cltv_c["monetary_cltv_avg"])

    cltv = ggf.customer_lifetime_value(bgf,
                                       cltv_c["frequency"],
                                       cltv_c["recency_cltv_weekly"],
                                       cltv_c["T_weekly"],
                                       cltv_c["exp_average_value"],
                                       time=6,  # 6 aylık
                                       freq="W",  # T'nin frekans bilgisi.
                                       discount_rate=0.01)

    cltv = cltv.reset_index()
    cltv_final = cltv_c.merge(cltv, on="master_id", how="left")
    cltv_final["cltv_segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])
    return cltv_final

df = df_.copy()
cltv_final2 = create_cltv_p(df)
cltv_final2.to_csv("cltv_prediction.csv")