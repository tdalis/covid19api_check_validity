#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:41:25 2020

@author: zeus
"""

# Import libraries

import pandas as pd
import json
import urllib.request
import os

# set working environment
os.chdir("/YourDirectory")

# define url for all the data
url = "https://api.covid19api.com/all"

# request the data and decode them using json
with urllib.request.urlopen(url) as url:
    data = json.loads(url.read().decode())
   # print(data)

# make the data into a pandas dataframe
df = pd.DataFrame(data)

# save on your local directory
df.to_csv("corona_data.csv", index=False)

""" I've noticed somehting funny when I was exploring the data in Tablaeu, the Chinese cases were in the millions
but the reports are around 90k, so I decided to see if Tablaeu was the problem or the data """

# Create a df where only China exists
china = df['Country'] == 'China'

chinadf = df[china]

# find the sum of chinese cases in our df dataframe
sum(chinadf['Cases'])

""" When running the sum function above the result is 3,694,614 cases, way above the reported numbers """

""" To double check, the covid19api also has links to help you pull in data by country, so I decided to see if the
data is different when calling the China API link directly """

# define urlc
urlc = "https://api.covid19api.com/country/china/status/confirmed"

# create datac by requesting the data using urllib and decoding using json
with urllib.request.urlopen(urlc) as urlc:
    datac = json.loads(urlc.read().decode())
   # print(datac)

# create the dfc dataframe
dfc = pd.DataFrame(datac)

# find the sum of chinese cases in our dfc dataframe
sum(dfc['Cases'])

""" When running the sum function above the result is 5,754,978 - a different umber from the previous pull but still
in the millions """