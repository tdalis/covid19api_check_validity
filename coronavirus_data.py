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

""" After further analysis and a conversation with the developer of the api (find Kyle on Twitter: https://twitter.com/ksredelinghuys)
I realised that the problem is not in the data, but in the way I intrepreted the data, a common problem for other
users of the API according to Kyle. The confirmed/recovered/deaths cases are the accumulated cases not the daily cases,
therefore, we need to take the latest date for each country """

""" The code below will solve this problem on a basic level, but it won't provide you with the daily count, if you need
the daily count, let me know and I'll try to write a script for that too """

# drop first row because it had a weird date and empty fields (double check your df before executing this)
df = df.drop(0, axis=0)

# transformed Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# create a boolean mask, call it latest_date and assign the latest date to it (latest date could be datetime.datetime, np.datetime64, pd.Timestamp, or even datetime strings)
latest_date = (df['Date'] == '2020-03-25')

# assign the sub-DataFrame to a new dataframe
df_latest = df.loc[latest_date]

# export df_latest to a csv
df_latest.to_csv("corona_data.csv", index=False)

""" You can use the code below to double check that the numbers make sense this time, using the China cases again """
# create a boolean for China == True
latC = df_latest['Country'] == 'China'
# create a boolean for confirmed == True
confC = df_latest['Status'] == 'confirmed'
# create a sub-DataFrame where both China and confnirmed are True
latCdf = df_latest[latC & confC]
# See the sum of the cases
sum(latCdf['Cases'])
