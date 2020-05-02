#!/usr/bin/python
__all__ = ['TobRegScraper','GenNewRet']

# import modules
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# add the drop down options

localauthorities = {'1': 'Aberdeen City',
 '2': 'Aberdeenshire',
 '3': 'Angus',
 '4': 'Argyll and Bute',
 '5': 'Clackmannanshire',
 '6': 'Comhairle nan Eilean Siar',
 '7': 'Dumfries and Galloway',
 '8': 'Dundee City',
 '9': 'East Ayrshire',
 '10': 'East Dunbartonshire',
 '11': 'East Lothian',
 '12': 'East Renfrewshire',
 '13': 'Edinburgh City',
 '14': 'Falkirk',
 '15': 'Fife',
 '16': 'Glasgow City',
 '17': 'Highland',
 '18': 'Inverclyde',
 '19': 'Midlothian',
 '20': 'Moray',
 '21': 'North Ayrshire',
 '22': 'North Lanarkshire',
 '23': 'Orkney Islands',
 '24': 'Perth and Kinross',
 '25': 'Renfrewshire',
 '26': 'Scottish Borders',
 '27': 'Shetland Islands',
 '28': 'South Ayrshire',
 '29': 'South Lanarkshire',
 '30': 'Stirling',
 '31': 'West Dunbartonshire',
 '32': 'West Lothian',
 '': ''}


businesstype = {'BulkSuppliers': 'Bulk Suppliers',
 'ConvenienceStore': 'Convenience Store',
 'Newsagents': 'Confectionary / Tobacconist / Newsagents',
 'EntertainmentVenue': 'Entertainment Venue',
 'ForecourtGarage': 'Forecourt Garage',
 'Hotel': 'Hotel',
 'MobileTrade': 'Mobile Trade',
 'Nightclub': 'Nightclub',
 'OffLicence': 'Off-Licence',
 'OtherCatering': 'Other Catering',
 'OtherRetail': 'Other Retail',
 'PrivateClub': 'Private Club',
 'PublicHouse': 'Public House',
 'Restaurant': 'Restaurant',
 'SpecialistTobacconists': 'Specialist Tobacconists',
 'SportsClub': 'Sports Club',
 'Supermarket': 'Supermarket and Other Retail Outlets',
 '': ''}

productssold = {'TobaccoOnly': 'Tobacco Only',
 'NicotineVapourProductsOnly': 'Nicotine Vapour Products Only',
 'TobaccoAndNicotineVapourProducts': 'Tobacco And Nicotine Vapour Products',
 '': ''}

status = {'Active': 'Active', 'Inactive': 'Inactive', 'Suspended': 'Suspended', '': ''}

# get the options for the selection

page = requests.get("https://www.tobaccoregisterscotland.org/search-the-register/")

def TobRegScraper(Name, Postcode, LA, BT, PS, S):
    """Build the search string to download the data"""

    baseurl="https://www.tobaccoregisterscotland.org/search-the-register/"
    searchurl = baseurl + "?Name=" + Name + "&Postcode=" + Postcode
    
    if LA not in localauthorities:
        raise ValueError("Unknown local authority: {}".format(LA))
    
    searchurl = searchurl + "&LocalAuthority=" + LA 
    
    if BT not in businesstype:
        raise ValueError("Unknown business type: {}".format(BT))
        
    searchurl = searchurl + "&BusinessType=" + BT     
    
    if PS not in productssold:
        raise ValueError("Unknown product sold: {}".format(PS))
        
    searchurl = searchurl + "&ProductType=" + PS   
        
    if S not in status:
        raise ValueError("Unknown status: {}".format(S))
    
    searchurl = searchurl + "&PremisesStatus=" + S + "&page=all" 
    

    page = requests.get(searchurl)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find_all("dl")
    count = len(soup.find_all(text='Address:'))
    

    tob_info = pd.DataFrame()
    cleaned_id_text = []
    
    # get all the data from the dt and dd tags
    for f in range(0,count):
        for i in info[f].find_all('dt'):
            cleaned_id_text.append(i.text)
            cleaned_id__attrb_text = []
    for f in range(0,count):        
        for i in info[f].find_all('dd'):
            cleaned_id__attrb_text.append(i.text)
       
    # stick it in the tob_info pandas dataframe
    tob_info['Type'] = cleaned_id_text
    tob_info['Attribute'] = cleaned_id__attrb_text
    
    # make an id column so we can pivot
    x = np.array(range(0,count))
    ID = np.repeat(x, [6], axis=0)
    tob_info["ID"]= ID
    tob_info['Type'] = tob_info['Type'].str.replace(":","")
     
    # use the pivot command
    tob_info_output = tob_info.pivot(index='ID', columns='Type', values='Attribute')
   
    # output the final tobacco retailer dataset
    return(tob_info_output)
    
   
    