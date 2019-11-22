# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:15:25 2019

@author: mcherrie
"""

# import all the modules required
from bs4 import BeautifulSoup
import requests
import pandas as pd


page = requests.get("https://www.tobaccoregisterscotland.org/search-the-register/")

soup = BeautifulSoup(page.content, 'html.parser')

selectoptions = soup.find('select', { "id"})

# Get the selection values and keys
items = soup.select('option[value]')
values = [item.get('value') for item in items]
textValues = [item.text for item in items]

# put into a pandas dataframe
valueDF = pd.DataFrame(values)
valueDF['value'] = textValues
valueDF = valueDF[valueDF.value != 'Select']
valueDF.rename(columns={valueDF.columns[0]: "Key" }, inplace = True)

# create the dictionaries

localauthorities = pd.Series(valueDF[0:31].value.values,index=valueDF[0:31].Key).to_dict()
localauthorities[""] = ""

businesstype = pd.Series(valueDF[32:49].value.values,index=valueDF[32:49].Key).to_dict()
businesstype[""] = ""

productssold = pd.Series(valueDF[49:52].value.values,index=valueDF[49:52].Key).to_dict()
productssold[""] = ""

status = pd.Series(valueDF[52:56].value.values,index=valueDF[52:56].Key).to_dict()
status[""] = ""
