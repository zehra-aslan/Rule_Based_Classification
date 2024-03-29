#############################################
# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama
#############################################

#############################################
# İş Problemi
#############################################
# Bir oyun şirketi müşterilerinin bazı özelliklerini kullanarak seviye tabanlı (level based) yeni müşteri tanımları (persona)
# oluşturmak ve bu yeni müşteri tanımlarına göre segmentler oluşturup bu segmentlere göre yeni gelebilecek müşterilerin şirkete
# ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.

# Örneğin: Türkiye’den IOS kullanıcısı olan 25 yaşındaki bir erkek kullanıcının ortalama ne kadar kazandırabileceği belirlenmek isteniyor.


#############################################
# Veri Seti Hikayesi
#############################################
# Persona.csv veri seti uluslararası bir oyun şirketinin sattığı ürünlerin fiyatlarını ve bu ürünleri satın alan kullanıcıların bazı
# demografik bilgilerini barındırmaktadır. Veri seti her satış işleminde oluşan kayıtlardan meydana gelmektedir. Bunun anlamı tablo
# tekilleştirilmemiştir. Diğer bir ifade ile belirli demografik özelliklere sahip bir kullanıcı birden fazla alışveriş yapmış olabilir.

# Price: Müşterinin harcama tutarı
# Source: Müşterinin bağlandığı cihaz türü
# Sex: Müşterinin cinsiyeti
# Country: Müşterinin ülkesi
# Age: Müşterinin yaşı

################# Uygulama Öncesi #####################

#    PRICE   SOURCE   SEX COUNTRY  AGE
# 0     39  android  male     bra   17
# 1     39  android  male     bra   17
# 2     49  android  male     bra   17
# 3     29  android  male     tur   17
# 4     49  android  male     tur   17

################# Uygulama Sonrası #####################

#       customers_level_based        PRICE SEGMENT
# 0   BRA_ANDROID_FEMALE_0_18  1139.800000       A
# 1  BRA_ANDROID_FEMALE_19_23  1070.600000       A
# 2  BRA_ANDROID_FEMALE_24_30   508.142857       A
# 3  BRA_ANDROID_FEMALE_31_40   233.166667       C
# 4  BRA_ANDROID_FEMALE_41_66   236.666667       C


import pandas as pd
df = pd.read_csv('datasets/persona.csv')

# Veri setini inceleyelim

df.info()
df.head()
df.tail()
df.describe().T
df.shape
df.columns
df.index
df.isnull().values.any()

# Kaç unique SOURCE vardır? Frekansları nedir?

df['SOURCE'].unique()
df['SOURCE'].value_counts()

# Kaç unique PRICE vardır?

df.PRICE.nunique()

# Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

df.PRICE.value_counts()

# Hangi ülkeden kaçar tane satış olmuş?

df.COUNTRY.value_counts()

# Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby('COUNTRY').agg({'PRICE': 'sum'})
# df.groupby('COUNTRY')['PRICE'].sum()

# SOURCE türlerine göre göre satış sayıları nedir?

df.SOURCE.value_counts()

# Ülkelere göre PRICE ortalamaları nedir?

df.groupby('COUNTRY').agg({'PRICE': 'mean'})

# SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby(['SOURCE']).agg({'PRICE': 'mean'})

# COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(['SOURCE', 'COUNTRY']).agg({'PRICE': 'mean'})


#############################################
# COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################

agg_df = df.groupby(['COUNTRY', 'SOURCE', 'SEX', 'AGE']).agg({'PRICE': 'mean'})


#############################################
# Çıktıyı PRICE'a göre sıralayalım
#############################################
# Çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayalım
# Çıktıyı agg_df olarak kaydedelim

agg_df.sort_values('PRICE', ascending=False)

len(agg_df.columns)
#############################################
# Indekste yer alan isimleri değişken ismine çevirelim
#############################################
# Çıktıdaki PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çevirelim
# İpucu: reset_index()
# agg_df.reset_index(inplace=True)

agg_df = agg_df.reset_index()
agg_df.columns


#############################################
# AGE değişkenini kategorik değişkene çevirip ve agg_df'e ekleyelim
#############################################
# Age sayısal değişkenini kategorik değişkene çevirelim
# Aralıkları ikna edici olacak şekilde oluşturalım
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'

# AGE değişkeninin nerelerden bölüneceğini belirtelim:

my_bins = [0, 18, 23, 30, 40, agg_df['AGE'].max()]

# Bölünen noktalara karşılık isimlendirmelerin ne olacağını ifade edelim:

mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df['AGE'].max())]
# mylabels = ['0_18', '19_23', '24_30', '31_40', f'41_{agg_df["AGE"].max()}']

# age'i bölelim:
pd.cut(agg_df['AGE'], bins=my_bins, labels=mylabels)

agg_df['AGE_CAT'] = pd.cut(agg_df['AGE'], bins=my_bins, labels=mylabels)
agg_df.head()

#############################################
# Yeni level based müşterileri tanımlayıp veri setine değişken olarak ekleyelim
#############################################
# customers_level_based adında bir değişken tanımlayıp veri setine bu değişkeni ekleyelim
# list comp ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekir
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18
# Bunları groupby'a alıp price ortalamalarını almak gerekir
agg_df.drop(['AGE', 'PRICE'], axis=1).values

# liste = ['A', 'B', 'C']
# '-'.join(liste)

agg_df["CUSTOMERS_LEVEL_BASED"] = ["_".join(i).upper() for i in agg_df.drop(['AGE', 'PRICE'], axis=1).values]
agg_df

# ["{}_{}_{}_{}".format(x.upper(),y.upper(),z.upper(),k) for x,y,z,k in zip(agg_df["COUNTRY"],agg_df["SOURCE"],agg_df["SEX"],agg_df["AGE_CAT"])]

# agg_cols=["COUNTRY","SOURCE","SEX","AGE_CAT"]
# [col[0].upper()+"_"+col[1].upper()+"_"+col[2].upper()+"_"+col[3].upper() for col in agg_df[agg_cols].values ]

# agg_df['COUNTRY'].astype(str) + "_" + \
# agg_df['SOURCE'].astype(str) + "_" + \
# agg_df['SEX'].astype(str) + "_" + \
# agg_df['AGE_CAT'].astype(str)

# Gereksiz değişkenleri çıkaralım:

agg_df.head()
agg_df = agg_df[['CUSTOMERS_LEVEL_BASED', 'PRICE']]

agg_df = agg_df.groupby('CUSTOMERS_LEVEL_BASED')['PRICE'].mean().reset_index()


# Burada ufak bir problem var. Birçok aynı segment olacak.
# örneğin USA_ANDROID_MALE_0_18 segmentinden birçok sayıda olabilir.
# Bu sebeple segmentlere göre groupby yaptıktan sonra price ortalamalarını almalı ve segmentleri tekilleştirelim


#############################################
# Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayıralım
#############################################
# PRICE'a göre segmentlere ayıralım
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyelim
# segmentleri betimleyelim

[23, 27, 34, 34, 35, 39, 41, 48]

agg_df['SEGMENT'] = pd.qcut(agg_df.PRICE, q=4, labels=['D', 'C', 'B','A'])
agg_df.head()

agg_df.groupby('SEGMENT').agg({'PRICE': ['mean', 'sum', 'min', 'max']}).reset_index()

agg_df['PRICE'].corr()

#############################################
# Yeni gelen müşterileri sınıflandırıp ne kadar gelir getirebileceğini tahmin edelim
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_user = 'TUR_ANDROID_FEMALE_31_40'
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == new_user]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

new_user = 'FRA_IOS_FEMALE_31_40'
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == new_user]
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == 'BRA_ANDROID_FEMALE_0_18']


df[['PRICE', 'AGE']].corr()
