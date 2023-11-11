                        # AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması

"""
                                           İş Problemi
 Facebook kısa süre önce mevcut "maximum bidding" adı verilen teklif verme türüne alternatif
olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
bu yeni özelliği test etmeye karar verdi ve averagebidding'in maximum bidding'den daha fazla dönüşüm
getirip getirmediğini anlamak için bir A/B testiyapmak istiyor.A/B testi 1 aydır devam ediyor ve
bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.
"""

                                          # Veri Seti Hikayesi
"""
Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer
almaktadır. Kontrol grubuna Maximum Bidding, test grubuna Average Bidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç

"""



                                        # AB Testing (Bağımsız İki Örneklem T Testi)
# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.






                                          # Proje Görevleri
                                 # Görev 1:  Veriyi Hazırlama ve Analiz Etme
# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

#Öncelikle kullanacağımız kütüphaneleri import edelim.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro, levene, ttest_ind


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df_control = pd.read_excel(r"C:\Users\sevim\Desktop\MIUUL\HAFTA 4\CASE STUDY 2\ABTesti\ab_testing.xlsx", sheet_name =  "Control Group")
df_test = pd.read_excel(r"C:\Users\sevim\Desktop\MIUUL\HAFTA 4\CASE STUDY 2\ABTesti\ab_testing.xlsx", sheet_name =  "Test Group")


# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
df_test.describe().T
df_control.describe().T
df_control.head()
df_test.head()

##her bir sayısal sütunun diğer sayısal sütunlarla olan ilişkisini görsel olarak gözlemleyelim.
pd.plotting.scatter_matrix(df_control)
plt.show(block=True)

pd.plotting.scatter_matrix(df_test)
plt.show(block=True)

#Not:block=True parametresi, grafiğin görüntülendiği sırada programın diğer işlemlerin beklemesini sağlar.
# Eğer bu parametre belirtilmezse, program diğer işlemlere devam ederken grafiği beklemeksizin görüntüler.



#Kontrol ve test grubunun satın alma değişkenlerinin ortalamasını kontrol edip kıyaslayalım.

df_control["Purchase"].mean()   #550.8940587702316
df_test["Purchase"].mean()      #582.1060966484677



# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.
df_control["Bidding"] = "Maximum Bidding"
df_test["Bidding"] = "Average Bidding"

df_control.groupby("Bidding").agg({"Purchase": "mean"})
df_test.groupby("Bidding").agg({"Purchase": "mean"})
df=pd.concat([df_control,df_test], axis=0,ignore_index=True)
df.groupby("Bidding").agg({"Purchase": "mean"})
df_control.head()
df_test.head()
df.head()
df.tail()
#Bidding kesişimine göre df_control ve df_test dataframelerini concat ettik.

                            # Görev 2:  A/B Testinin Hipotezinin Tanımlanması

# Adım 1: Hipotezi tanımlayınız.

#Buradaki amacımız daha önceden geliştirdiğimiz Maximum Bidding ile Average Bidding satışlarının gerçekten hesaplanılan
#farkta olup olmadığıdır. Sonradan geliştirilen uygulama müşteriyi cezbetti mi, kazancı daha çok arttırdı mı bunu
#AB Testi ile gözlemleyeceğiz.

"""
Tezimizi kuralım.
H0 : M1 = M2         average bidding ile maximum bidding arasında fark yoktur.    
H1 : M1!= M2         average bidding ile maximum bidding arasında fark vardır. 
"""

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz.

df.groupby("Bidding").agg({"Purchase": "mean"})
#Daha sonra geliştirilen uygulama ile daha fazla satış yapıldığı görülmektedir.Doğruluğunu test edelim.



                              # GÖREV 3: Hipotez Testinin Gerçekleştirilmesi

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
"""  
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# 4. p-value değerine göre sonuçları yorumla
"""

#Normallik varsayımı Shapiro testi ile gerçekleştirilir.
#p value değeri 0.01den daha küçükse H0 reddedilir.


#Normallik Varsayımı
test_stat, pvalue = shapiro(df.loc[df["Bidding"]=="Average Bidding" , "Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
#p-value = 0.1541


test_stat, pvalue = shapiro(df.loc[df["Bidding"]=="Maximum Bidding", "Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.5891

#p-value = 0.1541
#H0 REDDEDİLEMEZ.


# Varyans Homojenligi Varsayımı
test_stat, pvalue = levene(df.loc[df["Bidding"] == "Maximum Bidding", "Purchase"].dropna(),
                           df.loc[df["Bidding"] == "Average Bidding", "Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p-value = 0.1083
#H0 REDDEDİLEMEZ.


"""HOMOJEN BİR DAGILIMA SAHİP. O SEBEPLE TTEST UYGULANACAKTIR."""

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz
nan_policy='omit'
test_stat, pvalue = ttest_ind(df.loc[df["Bidding"] == "Maximum Bidding", "Purchase"].dropna(),
                              df.loc[df["Bidding"] == "Average Bidding", "Purchase"].dropna(),
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p-value = 0.3493
#H0 REDDEDİLEMEZ.


# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

"""
İSTATİSTİKİ OLARAK İKİ FARKLI MODELİN HİCBİR FARKI YOKTUR. SATIŞ ORANINDAKİ FARKLILIKLAR ŞANS
ESERİ ORTAYA ÇIKMIŞ KABUL EDİLMEKTEDİR.
Örneklem sayısı arttırılabilir , süre uzatılabilir.Her iki model için daha fazla müşteri ile kontak kurularak uygulamanın
kullanılması ile analiz örnekleri çoğaltılabilir.
"""