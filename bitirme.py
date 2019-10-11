import pandas as pd                 # Veri Analiz ve önişleme
import matplotlib.pyplot as plt     # Görselleştirme için kullanacağımız kütüphane
import re                           # Düzensiz ve istenmeyen ifadeleri kaldırmak için kullandığımız kütüphane
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

from wordcloud import WordCloud,STOPWORDS
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import seaborn as sns

# Verinin yüklenmesi

alexa_veri = pd.read_csv("amazon_alexa.csv")     
yorumlar = alexa_veri["verified_reviews"]
df_yorumlar = pd.DataFrame(yorumlar)
df_yorumlar.columns = ["Yorumlar"]

############################################################################################
# Verimize index atadık

index_ = []

for i in range(0, len(df_yorumlar['Yorumlar']) ):
    index_.append(i)
    
df_yorumlar["index"] = index_
alexa_veri["index"] = index_


############################################################################################

# Parantezler içerisindeki ifadeleri bulup siliyor. "" karakteriyle yer değiştiriyor diğer bir ifadeyle
yerine_bosluk_birakma = re.compile("(\.) | (\;) | (\:) | (\!) | (\') | (\?) | (\,) | (\") | (\() | (\)) | (\[) | (\])")
# Parantezler içerisindeki ifadelerin yerine boşluk karakteri koyuyoruz " "
yerine_bosluk_birak= re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def on_isleme(veri):
    veri = [yerine_bosluk_birakma.sub("", satir.lower()) for satir in veri]
    veri = [yerine_bosluk_birak.sub(" ", satir) for satir in veri]
    return veri

yari_temizlenmis_veri = on_isleme(yorumlar)

df_yari_temizlenmis_veri = pd.DataFrame(yari_temizlenmis_veri)


df_yari_temizlenmis_veri.columns = ["Yorumlar"]

df_yari_temizlenmis_veri["index"] = index_


############################################################################################
"""
cumleler = []
kelime_listesi = []
satir = []

for i in range(0, len(df_yari_temizlenmis_veri.Yorumlar)):
    cumleler=df_yari_temizlenmis_veri.Yorumlar[i].split(" ")
    
    for j in range(0, len(df_yari_temizlenmis_veri.Yorumlar[i].split(" "))):
        kelime_listesi.append(cumleler[j])
        satir.append(i)

df_kelime_listesi = pd.DataFrame(kelime_listesi, columns = ["kelimeler"])
df_satir = pd.DataFrame(satir)

kelime_index = df_kelime_listesi
kelime_index["index"] = df_satir
"""
############################################################################################

# atilacak_kelimeler = set(stopwords.words('english'))  
"""
temizlenmis_kelimeler = [i for i in kelime_index["kelimeler"] if not i in atilacak_kelimeler]  

temizlenmis_kelimeler = [] 
  
for i in kelime_index["kelimeler"]: 
    if i not in atilacak_kelimeler: 
        temizlenmis_kelimeler.append(i)  

df_temizlenmis_kelimeler = pd.DataFrame(temizlenmis_kelimeler) 
df_temizlenmis_kelimeler.columns = ["kelimeler"]
"""

############################################################################################
# 3 haften küçük olan kelimeleri sildirmeye çalışıyorum. 
"""
yeni_temizlenmis_kelimeler=[]
for i in range(0,len(temizlenmis_kelimeler)):
    if len(temizlenmis_kelimeler[i])>3:
        yeni_temizlenmis_kelimeler.append(temizlenmis_kelimeler[i])

df_yeni_temizlenmis_kelimeler=pd.DataFrame(yeni_temizlenmis_kelimeler)


"""
############################################################################################

atilacak_kelimeler = set(stopwords.words('english'))  
kelime_temizle = []
satir = []

for i in range(0,len(df_yari_temizlenmis_veri.Yorumlar)):
    cumleler = df_yari_temizlenmis_veri.Yorumlar[i].split(" ")

    for j in range(0, len(df_yari_temizlenmis_veri.Yorumlar[i].split(" "))):
        if len(cumleler[j]) > 3 and cumleler[j] not in atilacak_kelimeler:
            kelime_temizle.append(cumleler[j])
            satir.append(i)
            
son_kelime_listesi = pd.DataFrame(kelime_temizle, columns = ["kelimeler"])
son_satir = pd.DataFrame(satir)

kelime_index = son_kelime_listesi
kelime_index["index"] = son_satir

############################################################################################
"""
wordcloud = WordCloud(width = 800, height = 800, 
                background_color = 'black',
                min_font_size = 10).generate(str(kelime_temizle)) 

plt.figure(figsize = (8, 8), facecolor = "cyan") 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()
"""

############################################################################################

file = 'afinn.xlsx' 

afinn = pd.ExcelFile(file)

print(afinn.sheet_names)

sozluk_afinn = afinn.parse('Sheet1')

sozluk_afinn.rename(columns = {'word':'kelimeler'}, inplace = True)


duygu_afinn = pd.merge(kelime_index, sozluk_afinn, on = "kelimeler")

############### Nrc Sözlüğü ################################################################

file = 'nrc.xlsx'

nrc = pd.ExcelFile(file)

print(nrc.sheet_names)

sozluk_nrc = nrc.parse('Sheet1')

sozluk_nrc.rename(columns = {'word':'kelimeler'}, inplace = True)

duygu_nrc = pd.merge(kelime_index, sozluk_nrc, on = "kelimeler")

################# Bing Sözlüğü #############################################################


file = 'bing.xlsx'

bing = pd.ExcelFile(file)

print(bing.sheet_names)

sozluk_bing = bing.parse('Sheet1')

sozluk_bing.rename(columns = {'word':'kelimeler'}, inplace = True)


duygu_bing = pd.merge(kelime_index, sozluk_bing, on = "kelimeler")


############################################################################################
tam_veri_afinn = pd.merge(duygu_afinn, alexa_veri, on = "index")
tam_veri_nrc = pd.merge(duygu_nrc, alexa_veri, on = "index")
tam_veri_bing = pd.merge(duygu_bing, alexa_veri, on = "index")



#veriyi excele yazdırmak
writer = pd.ExcelWriter('tam_veri_afinn.xlsx') #nereye yazacağımızı belirtiyoruz.
tam_veri_afinn.to_excel(writer, 'Afinn verisi')  #DataFrame'i excele dönüştürdük
writer.save() 

writer = pd.ExcelWriter('tam_veri_nrc.xlsx') #nereye yazacağımızı belirtiyoruz.
tam_veri_nrc.to_excel(writer,'Nrc Verisi')  #DataFrame'i excele dönüştürdük
writer.save() 

writer = pd.ExcelWriter('tam_veri_bing.xlsx') #nereye yazacağımızı belirtiyoruz.
tam_veri_bing.to_excel(writer,'Bing verisi')  #DataFrame'i excele dönüştürdük
writer.save() 

############################################################################################
"""
#grafiklerde kullanmak için filtre
def filter_func(x):
    for i in range(0,len(tam_veri_afinn.score)):
        if tam_veri_afinn==5:
            return tam_veri_afinn



tam_veri_afinn.groupby(['index']).sum()['score'].plot()

tam_veri_afinn.groupby(['variation']).count()['score'].plot()



tam_veri_afinn.groupby(['kelimeler']).describe()['score'].sum().plot()

fig, ax = plt.subplots(figsize=(15,7))
tam_veri_afinn.groupby(['variation','variation'])['score'].plot(ax=ax)

"""

############################################################################################



























