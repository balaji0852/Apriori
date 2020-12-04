#!/usr/bin/env python
# coding: utf-8

# In[1]:



import pandas as pd
from sklearn import preprocessing 
import math


# ## Data extraction from Youtube dataset and user shopping basket list

# In[166]:


dataset = pd.read_csv('/content/Market_Basket_Optimisation.csv', header = None)
transactions = []
for i in range(0, 7501):
  transactions.append([str(dataset.values[i,j]) for j in range(0, 20)])


# In[ ]:


transactions


# In[168]:


elements = []
fooditems = []
for i in range(0,7501):
  for j in range(0,20):
    if transactions[i][j]!='nan':
      elements.append(transactions[i][j])
      
lst = list(dict.fromkeys(elements))
for i in range(0,len(lst)):
  item = list([lst[i],0,0,''])
  fooditems.append(item)

for i in range(0,7501):
  for j in range(0,20):
    if transactions[i][j]!='nan':
      for k in range(0,len(fooditems)):
        if transactions[i][j]==fooditems[k][0]:
          fooditems[k][1] = fooditems[k][1]+1
      

      


# In[ ]:


fooditems


# In[152]:


def Sort(Data,l):
  for i in range(0, l):
    for j in range(0, l-1):
      if Data[j][1] <  Data[j + 1][1]:
        tempo = Data[j]
        Data[j]= Data[j + 1]
        Data[j + 1]= tempo

def Sort2(Data,l):
  for i in range(0, l):
    for j in range(0, l-1):
      if Data[j][3] <  Data[j + 1][3]:
        tempo = Data[j]
        Data[j]= Data[j + 1]
        Data[j + 1]= tempo      


# In[170]:


Sort(fooditems,len(fooditems))


# In[154]:


import json
categories_data = []
dictdata = dict()
    


# In[155]:


Flag = []
flag = dict()
count=0
news_categories = ['/content/IN_category_id.json','/content/CA_category_id.json','/content/DE_category_id.json','/content/FR_category_id.json',
                   '/content/GB_category_id.json','/content/JP_category_id.json','/content/KR_category_id.json',
                   '/content/MX_category_id.json','/content/RU_category_id.json','/content/US_category_id.json',]
for j in range(0,len(news_categories)):
  with open(news_categories[j]) as utubejson:
    jsondata = json.load(utubejson)
    for i in jsondata['items']:
      flag = {
          i['id']:{
              'categ':i['snippet']['title'],
          }
      }
      dictdata.update(flag)
      Flag=[i['snippet']['title'],i['id']]
      categories_data.append(Flag)
      Flag.clear

      
  
    


# In[172]:


nsc = []
nsctg = []
for i in dictdata:
  nsctg= list([i, dictdata[i]['categ'],0,0,0])
  nsc.append(nsctg)
  


# In[157]:


import csv


# In[158]:


utubedata = []
file = ['/content/JP.csv','/content/RUSSIA.csv','/content/MEXICO.csv','/content/KR.csv',
        '/content/US.csv','/content/INDIA.csv','/content/DE.csv','/content/FR.csv','/content/GB.csv']
for i in file:
  with open(i) as data:
    utube = csv.reader(data)
    for row in utube:
      likes = list([row[0],row[1],row[2],row[3],])
      utubedata.append(likes)
    data.close
 


# In[159]:


for i in range(0,len(utubedata)):
  for j in range(0,len(nsc)):
    if nsc[j][0]==utubedata[i][0]:
      nsc[j][2]= nsc[j][3]+int(utubedata[i][1])
      nsc[j][3]= nsc[j][3]+int(utubedata[i][2])
      nsc[j][4]= nsc[j][4]+int(utubedata[i][3])
      
      
      


# In[ ]:


fooditems


# In[ ]:


for i in range(0,len(fooditems)):
  if i < len(nsc):
    fooditems[i][2] = int(nsc[i][0])
    fooditems[i][3] = str(nsc[i][1])
  else:
    fooditems[i][2] = 0
    fooditems[i][3] = 'nan'
fooditems  


# In[175]:


feild = 'empty'
for i in range(0,7501):
  for j in range(0,20):
    if  transactions[i][j]!='nan':
      for k in range(0,len(fooditems)):
        if transactions[i][j]==fooditems[k][0]:
          field = fooditems[k][3]
      if field == 'empty':
        transactions[i][j]=''
      else:
        transactions[i][j] = field

     


# In[ ]:


transactions


# In[178]:


get_ipython().system('pip install apyori')


# In[181]:


dataset1 = pd.read_csv('/content/Market_Basket_Optimisation.csv', header = None)
transactions1 = []
for i in range(0, 7501):
  transactions1.append([str(dataset1.values[i,j]) for j in range(0, 20)])


# In[202]:


dataset2 = pd.read_csv('/content/dataset.csv', header = None)
transactions2 = []
for i in range(0, 7501):
  transactions2.append([str(dataset2.values[i,j]) for j in range(0, 20)])


# In[224]:


from apyori import apriori
rules = apriori(transactions = transactions2, min_support = 0.003, min_confidence = 0.3, min_lift = 3, min_length = 2, max_length = 3)


# In[225]:


results = list(rules)
print(results)


# In[221]:


def inspect(results):
    lhs         = [tuple(result[2][0][0])[0] for result in results]
    rhs         = [tuple(result[2][0][1])[0] for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))
resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])


# In[240]:


pd.set_option("display.max_rows", None, "display.max_columns", None)


# In[179]:


with open('dataset.csv','w',newline='') as newsdata:
  writeit = csv.writer(newsdata)
  for i in range(0,len(transactions)):
    writeit.writerow(transactions[i])


# In[222]:


resultsinDataFrame


# In[237]:


rules1 = apriori(transactions = transactions1, min_support = 0.003, min_confidence = 0.3, min_lift = 3, min_length = 2, max_length = 3)


# In[238]:


results2 = list(rules1)
resultsinDataFrame1 = pd.DataFrame(inspect(results2), columns = ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])


# In[241]:


resultsinDataFrame1

