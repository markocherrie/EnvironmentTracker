# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 16:54:54 2019

@author: mcherrie
"""
from datetime import date
import GetData

df=GetData.TobRegScraper('','','','','','')
today = date.today()
todayformatted = today.strftime("%Y-%m-%d")
repo = 'data/STRR_'
ext = '.csv'
output = [repo, todayformatted, ext]
output = "".join(output)
df.to_csv(output)
