
# coding: utf-8

# In[2]:

from __future__ import division, print_function

from IPython.core.display import HTML, Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

get_ipython().magic(u'matplotlib inline')
plt.style.use('fivethirtyeight')


# In[ ]:




# In[3]:

yelp = pd.read_csv ('/users/quantum/desktop/data/items.csv')


# In[4]:

yelp.tail(100)


# In[5]:

yelp.reviews_date.describe()


# In[6]:

yelp.reviews_date((reviews_date)<=2016)


# In[7]:

yelp.dtypes


# In[8]:

yelp.count()


# In[9]:

yelp.isnull().sum()


# In[10]:

yelpdc= yelp.copy()


# In[11]:

yelpdc.head()


# In[12]:

yelpdc.shape 


# In[13]:

yelpdc.describe() 


# In[14]:

yelpdc.reviews


# In[15]:

yelpdc.count()


# In[16]:

yelpdc.isnull().sum()
yelpdc.dropna(inplace=True)
yelpdc.describe() 


# In[17]:

yelpdc.dropna(inplace=True)


# In[18]:

yelpdc.describe() 


# In[19]:

yelpdc.isnull().sum()


# In[20]:

yelpdc.count()


# In[21]:

yelpdc.duplicated().sum()


# In[22]:

yelp.plot( kind = "hist" )


# In[23]:

yelpdc.plot( kind = "hist" )


# In[24]:

#users.occupation.unique()       # return the unique values

yelpdc.name.unique()


# In[25]:

yelpdc['reviews_date']=pd.to_datetime(yelpdc['reviews_date'])


# In[26]:

yelpdc.dtypes


# In[27]:

yelpdc[reviews_date]=yelpdc.reviews_date.to_datetime()


# In[ ]:




# In[28]:

#drinks.groupby('continent').beer.mean()

#users.sort('age', ascending=False


# In[29]:

yelpdc.groupby('restaurant_url').reviews_stars.agg(['count']).sort()







# In[30]:

#yelpdc.groupby('name').describe().sort_index()#'reviews_stars')
yelpdc.groupby('name').reviews_stars.agg(['count', 'mean', 'min', 'max']).sort()

#yeldc.head(100)


# In[41]:

yelpdc.groupby('name')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[42]:

yelpdc.groupby('name').reviews_stars.agg(['count']).head(322).sort('count')


# In[ ]:

#Pennsylvania 6 DC
#Pineapple & Pearls
#komi $$$$
#Barmini By José Andrés $$$$ 
#Conosci $135 $31-61  (american)
#2020 Restaurant and Lounge , above$61
#1789 Restaurant prix fixe $85-$109
#quill $31-60
#Rasika tasting $75/60
#RPM Italian $31-60
#Obelisk 5 course $75-85 *one month
#nostos $31-60  $$$
#The Capital Grille  $85-115
#Tosca $$$ , $31-60 , main course=$40
#kazsishi, $$$, 2015 winner open table , 
#The Source , asian , $$$, $31-60, tasting menu= no prirce
#Vidalia , $$$, $31-60 tasting menu $78 per person ,"american"
#The Oval Room , $$$, tasting menu $60, $90 with wine
#Blue Duck Tavern , $$$, 31-$60
#Sushi Taro , $ tasting menu $140-245, *one month 
#Graffiato $$
#Proof Restaurant *mr $31-60
#black salt 31-60
#Rose’s Luxury #mr
#Jaleo DC 
#Central Michel Richard $$$, french, 
#fiola
#


# In[ ]:




# In[29]:

yelpdc.groupby('name').reviews_stars.agg([ 'mean']).sort('mean').plot( kind = "hist" )


# In[46]:

yelpdc.groupby('reviews_stars').reviews_stars.agg(['name']).sort('mean').plot( kind = "hist" )


# In[ ]:




# In[ ]:




# In[44]:

yelpdc.groupby('name').count().sort('reviews_stars')


# In[94]:

#yelpdc= pd.DataFrame(yelpdc)
#yelpdc.to_csv('yelp_sort.csv',index=False)


# In[55]:

yelpdc.isnull().sum()
yelpdc.dropna(inplace=True)
#yelpdc.describe() 




# In[22]:

yelpdc.describe() 


# In[ ]:




# In[31]:

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

cols = ['name', 'reviewsstars']
yelpdc.plot( kind = "hist" )



# In[57]:

yelpdc2= pd.DataFrame(yelpdc)
fina['WnvPresent']=y_probf
finalSubmission.to_csv('kaggleSubmission19.csv',index=False)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



