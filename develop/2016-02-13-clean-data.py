
# coding: utf-8

# In[1]:

import pandas as pd
import re
import requests

from IPython.display import IFrame

import folium


# In[2]:

df = pd.read_excel('../data/one_dollar_oysters.xlsx')


# In[3]:

df.tail(n=2)


# In[4]:

df.shape


# In[5]:

# Split df.Hours into days of week, start time, and end time (not done yet, obvs)
re.compile('')
df['days'] = df.Hours


# In[6]:

f = open('/Users/tesskornfield/google_api_key.txt', 'r')
GOOGLE_API_KEY = f.readline().rstrip()


# In[7]:

lats = []
lngs = []

for address in df.Address.tolist()[:69]:
    
    try: 
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=%s+San+Francisco' %address)
        responsejson = response.json()

        lat = responsejson['results'][0]['geometry']['location']['lat']
        lng = responsejson['results'][0]['geometry']['location']['lng']
        
    except:
        lat = 'na'
        lng = 'na'
        
    lats.append(lat)
    lngs.append(lng)


# In[8]:

df['lats'] = lats
df['lngs'] = lngs


# In[14]:

tileset = r'http://tile.stamen.com/toner-lite/{z}/{x}/{y}.png'
attribution = 'Map data by OpenStreetMap, under ODbL.'
zip_map = folium.Map(location=[37.769230, -122.433810], zoom_start=11, tiles=tileset, attr=attribution)

for row_index, row in df.iterrows():
    
    zip_map.simple_marker([row['lats'],row['lngs']],popup='%s, %s, %s' %(row['Name'],row['Address'],row['Hours']))

mappath = 'orsters.html'
zip_map.create_map(path=mappath)

IFrame(mappath,1200,500)


# In[ ]:



