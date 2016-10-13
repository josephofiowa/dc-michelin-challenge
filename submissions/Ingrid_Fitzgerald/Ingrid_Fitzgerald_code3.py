
# coding: utf-8

# In[15]:

import json
import pandas as pd
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key='903135fd80248bdbf6292749c51f4a87656b511b')


# In[47]:

import json
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1
 
 
url = 'http://www.opentable.com/kapnos#reviews'

# operations to perform
extract = ['keyword', 'emotion', ]
 
alchemy_language = AlchemyLanguageV1(api_key= '903135fd80248bdbf6292749c51f4a87656b511b')
results = alchemy_language.combined(url=url, extract=extract)
 
# print the results
print(json.dumps(results, indent=1))


# In[54]:

a1 = AlchemyLanguageV1(api_key='903135fd80248bdbf6292749c51f4a87656b511b')


data=json.dumps(alchemy_language.keywords(url='http://www.opentable.com/fiola-mare?covers=2&dateTime=2016-10-06%2019%3A00#reviews'),indent=1)
data1=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/fiola-mare?covers=2&dateTime=2016-10-06%2019%3A00#reviews'),indent=1)



# In[32]:

a=pd.read_json(data)
a.head(5)


# In[55]:

a1=pd.read_json(data1)
a1.head(5)


# In[ ]:




# In[35]:

temp2=[]
temp2=a['keywords'].tolist()
dftemp2=pd.DataFrame(temp2)
dftemp2


# In[62]:

temp1=[]
temp1=a1['docSentiment'].tolist()
dftemp1=pd.DataFrame(temp1)
dftemp1


# In[89]:

x = AlchemyLanguageV1(api_key='903135fd80248bdbf6292749c51f4a87656b511b')
fiora=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/fiola-mare?covers=2&dateTime=2016-10-06%2019%3A00#reviews'),indent=2)
rasika=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/rasika?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
minijose=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/barmini-by-jose-andres?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
sushitaro=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/sushi-taro?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
blueduck=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/blue-duck-tavern?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
marcels=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/marcels-by-robert-wiedmaier?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
plume=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/plume-at-the-jefferson-hotel?p=2&sd=2016-12-08%2018%3A00'),indent=2) 
littlewash=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/the-inn-at-little-washington?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
charliepalmer=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/charlie-palmer-steak-washington?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
matisse=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/matisse?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
lediplomate= json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/le-diplomate?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
blacksalt=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/blacksalt?covers=2&dateTime=2016-12-08%2018%3A00#reviews'),indent=2)
proofrestaurant=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/proof-restaurant?covers=2&dateTime=2016-12-08%2018%3A00#reviews'),indent=2)
ovalroom=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/the-oval-room?covers=2&dateTime=2016-12-08%2018%3A00#reviews'),indent=2)
joesseafood=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/joes-seafood-prime-steak-and-stone-crab-washington-dc?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
toscaristorante=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/tosca-ristorante-washington?p=2&sd=2016-12-08%2018%3A00'),indent=2)
acadia=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/acadiana?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
marcelbyrobert=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/marcels-by-robert-wiedmaier?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)
kazsishi=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/kaz-sushi-bistro?p=2&sd=2016-12-08%2018%3A00'),indent=2)
jaleo=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/jaleo-washington-dc?p=2#reviews'),indent=2)
filomenaristorante=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/filomena-ristorante?p=2#reviews'),indent=2)
thesource=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/the-source-by-wolfgang-puck?covers=2&dateTime=2016-12-08%2018%3A00#reviews'),indent=2)
Pineapple_Pearls=json.dumps(alchemy_language.sentiment(url='https://www.yelp.com/biz/pineapple-and-pearls-washington-3?osq=pineaples+and+pearls'),indent=2)
komi=json.dumps(alchemy_language.sentiment(url='https://www.yelp.com/biz/komi-washington'),indent=2)
tailupgoat=json.dumps(alchemy_language.sentiment(url='https://www.yelp.com/biz/tail-up-goat-washington?osq=komi'),indent=2)
roseluxe=json.dumps(alchemy_language.sentiment(url='https://www.yelp.com/biz/roses-luxury-washington?osq=komi'),indent=2)
ovelisk=json.dumps(alchemy_language.sentiment(url='https://www.yelp.com/biz/obelisk-washington?osq=komi'),indent=2)
TheCapitalGrille=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/the-capital-grille-chevy-chase?p=2&sd=2016-12-08%2018%3A00#reviews'),indent=2)


# In[129]:

dieznueve=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/1789-restaurant?covers=2&dateTime=2016-12-08%2018%3A00#reviews'),indent=2)
pennsix=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/pennsylvania-6-dc?covers=2&dateTime=2016-12-08%2018%3A00#reviews'),indent=2)
vidalia=json.dumps(alchemy_language.sentiment(url='http://www.opentable.com/vidalia?covers=2&dateTime=2016-12-08%2018%3A00#reviews'),indent=2)


# In[ ]:




# In[ ]:

#fiora  


# In[70]:

restfiora=pd.read_json(fiora)
restfiora.head(5)

tempfiora=[]
tempfiora=restfiora['docSentiment'].tolist()
dftempfiora=pd.DataFrame(tempfiora)
dftempfiora


# In[90]:

#rasika

restrasika=pd.read_json(rasika)
restrasika.head(5)

temprasika=[]
temprasika=restrasika['docSentiment'].tolist()
dftemprasika=pd.DataFrame(temprasika)
dftemprasika



# In[ ]:




# In[91]:

#minijose
restminijose=pd.read_json(minijose)
restminijose.head(5)

tempminijose=[]
tempminijose=restminijose['docSentiment'].tolist()
dftempminijose=pd.DataFrame(tempminijose)
dftempminijose


# In[92]:

#sushitaro
restsushitaro=pd.read_json(sushitaro)
restsushitaro.head(5)

tempsushitaro=[]
tempsushitaro=restsushitaro['docSentiment'].tolist()
dftempsushitaro=pd.DataFrame(tempsushitaro)
dftempsushitaro


# In[93]:

#blueduck
restblueduck=pd.read_json(blueduck)
restblueduck.head(5)

tempblueduck=[]
tempblueduck=restblueduck['docSentiment'].tolist()
dftempblueduck=pd.DataFrame(tempblueduck)
dftempblueduck


# In[94]:

#marcels
restmarcels=pd.read_json(marcels)
restmarcels.head(5)

tempmarcels=[]
tempmarcels=restmarcels['docSentiment'].tolist()
dftempmarcels=pd.DataFrame(tempmarcels)
dftempmarcels



# In[95]:

#plume
restplume=pd.read_json(plume)
restplume.head(5)

tempplume=[]
tempplume=restplume['docSentiment'].tolist()
dftempplume=pd.DataFrame(tempplume)
dftempplume


# In[96]:

#littlewash

restlittlewash=pd.read_json(littlewash)
restlittlewash.head(5)

templittlewash=[]
templittlewash=restlittlewash['docSentiment'].tolist()
dftemplittlewash=pd.DataFrame(templittlewash)
dftemplittlewash


# In[97]:

#littlewash

restcharliepalmer=pd.read_json(charliepalmer)
restcharliepalmer.head(5)

tempcharliepalmer=[]
tempcharliepalmer=restcharliepalmer['docSentiment'].tolist()
dftempcharliepalmer=pd.DataFrame(tempcharliepalmer)
dftempcharliepalmer


# In[98]:

#charliepalmer

restcharliepalmer=pd.read_json(charliepalmer)
restcharliepalmer.head(5)

tempcharliepalmer=[]
tempcharliepalmer=restcharliepalmer['docSentiment'].tolist()
dftempcharliepalmer=pd.DataFrame(tempcharliepalmer)
dftempcharliepalmer


# In[99]:

#matisse

restmatisse=pd.read_json(matisse)
restmatisse.head()

tempmatisse=[]
tempmatisse=restmatisse['docSentiment'].tolist()
dftempmatisse=pd.DataFrame(tempmatisse)
dftempmatisse


# In[100]:

#lediplomate

restlediplomate=pd.read_json(lediplomate)
restlediplomate.head(5)

templediplomate=[]
templediplomate=restlediplomate['docSentiment'].tolist()
dftemplediplomate=pd.DataFrame(templediplomate)
dftemplediplomate


# In[101]:

#blacksalt

restblacksalt=pd.read_json(blacksalt)
restblacksalt.head(5)

tempblacksalt=[]
tempblacksalt=restblacksalt['docSentiment'].tolist()
dftempblacksalt=pd.DataFrame(tempblacksalt)
dftempblacksalt


# In[102]:

#proofrestaurant

restproofrestaurant=pd.read_json(proofrestaurant)
restproofrestaurant.head(5)

tempproofrestaurant=[]
tempproofrestaurant=restproofrestaurant['docSentiment'].tolist()
dftempproofrestaurant=pd.DataFrame(tempproofrestaurant)
dftempproofrestaurant


# In[103]:

#ovalroom

restovalroom=pd.read_json(ovalroom)
restovalroom.head(5)

tempovalroom=[]
tempovalroom=restovalroom['docSentiment'].tolist()
dftempovalroom=pd.DataFrame(tempovalroom)
dftempovalroom


# In[104]:

#joesseafood

restjoesseafood=pd.read_json(joesseafood)
restjoesseafood.head(5)

tempjoesseafood=[]
tempjoesseafood=restjoesseafood['docSentiment'].tolist()
dftempjoesseafood=pd.DataFrame(tempjoesseafood)
dftempjoesseafood


# In[105]:

#toscaristorante

resttoscaristorante=pd.read_json(toscaristorante)
resttoscaristorante.head(5)

temptoscaristorante=[]
temptoscaristorante=resttoscaristorante['docSentiment'].tolist()
dftemptoscaristorante=pd.DataFrame(temptoscaristorante)
dftemptoscaristorante


# In[106]:

#acadia

restacadia=pd.read_json(acadia)
restacadia.head(5)

tempacadia=[]
tempacadia=restacadia['docSentiment'].tolist()
dftempacadia=pd.DataFrame(tempacadia)
dftempacadia


# In[107]:

#marcelbyrobert

restmarcelbyrobert=pd.read_json(marcelbyrobert)
restmarcelbyrobert.head(5)

tempmarcelbyrobert=[]
tempmarcelbyrobert=restmarcelbyrobert['docSentiment'].tolist()
dftempmarcelbyrobert=pd.DataFrame(tempmarcelbyrobert)
dftempmarcelbyrobert


# In[108]:

#kazsishi

restkazsishi=pd.read_json(kazsishi)
restkazsishi.head(5)

tempkazsishi=[]
tempkazsishi=restkazsishi['docSentiment'].tolist()
dftempkazsishi=pd.DataFrame(tempkazsishi)
dftempkazsishi


# In[110]:

#jaleo

restjaleo=pd.read_json(jaleo)
restjaleo.head(5)

tempjaleo=[]
tempjaleo=restjaleo['docSentiment'].tolist()
dftempjaleo=pd.DataFrame(tempjaleo)
dftempjaleo


# In[111]:

#filomenaristorante

restfilomenaristorante=pd.read_json(filomenaristorante)
restfilomenaristorante.head(5)

tempfilomenaristorante=[]
tempfilomenaristorante=restfilomenaristorante['docSentiment'].tolist()
dftempfilomenaristorante=pd.DataFrame(tempfilomenaristorante)
dftempfilomenaristorante


# In[112]:

#thesource

restthesource=pd.read_json(thesource)
restthesource.head(5)

tempthesource=[]
tempthesource=restthesource['docSentiment'].tolist()
dftempthesource=pd.DataFrame(tempthesource)
dftempthesource


# In[113]:

#Pineapple_Pearls

restPineapple_Pearls=pd.read_json(Pineapple_Pearls)
restPineapple_Pearls.head(5)

tempPineapple_Pearls=[]
tempPineapple_Pearls=restPineapple_Pearls['docSentiment'].tolist()
dftempPineapple_Pearls=pd.DataFrame(tempPineapple_Pearls)
dftempPineapple_Pearls


# In[115]:

#komi

restkomi=pd.read_json(komi)
restkomi.head(5)

tempkomi=[]
tempkomi=restkomi['docSentiment'].tolist()
dftempkomi=pd.DataFrame(tempkomi)
dftempkomi


# In[117]:

#

resttailupgoat=pd.read_json(tailupgoat)
resttailupgoat.head(5)

temptailupgoat=[]
temptailupgoat=resttailupgoat['docSentiment'].tolist()
dftemptailupgoat=pd.DataFrame(temptailupgoat)
dftemptailupgoat


# In[118]:

#roseluxe

restroseluxe=pd.read_json(roseluxe)
restroseluxe.head(5)

temproseluxe=[]
temproseluxe=restroseluxe['docSentiment'].tolist()
dftemproseluxe=pd.DataFrame(temproseluxe)
dftemproseluxe


# In[122]:

#ovelisk

restovelisk=pd.read_json(ovelisk)
restovelisk.head(5)

tempovelisk=[]
tempovelisk=restovelisk['docSentiment'].tolist()
dftempovelisk=pd.DataFrame(tempovelisk)
dftempovelisk


# In[123]:

#TheCapitalGrille

restTheCapitalGrille=pd.read_json(TheCapitalGrille)
restTheCapitalGrille.head(5)

tempTheCapitalGrille=[]
tempTheCapitalGrille=restTheCapitalGrille['docSentiment'].tolist()
dftempTheCapitalGrille=pd.DataFrame(tempTheCapitalGrille)
dftempTheCapitalGrille


# In[126]:

#dieznueve

restdieznueve=pd.read_json(dieznueve)
restdieznueve.head(5)

tempdieznueve=[]
tempdieznueve=restdieznueve['docSentiment'].tolist()
dftempdieznueve=pd.DataFrame(tempdieznueve)
dftempdieznueve


# In[128]:

#pennsix

restpennsix=pd.read_json(pennsix)
restpennsix.head(5)

temppennsix=[]
temppennsix=restpennsix['docSentiment'].tolist()
dftemppennsix=pd.DataFrame(temppennsix)
dftemppennsix


# In[130]:

#vidalia

restvidalia=pd.read_json(vidalia)
restvidalia.head(5)

tempvidalia=[]
tempvidalia=restvidalia['docSentiment'].tolist()
dftempvidalia=pd.DataFrame(tempvidalia)
dftempvidalia


# In[ ]:




# In[136]:

import pandas as pd

final = pd.read_csv('/users/quantum/desktop/data/final2.csv')


# In[137]:

final.head()


# In[139]:

final.sort('sentiment')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



