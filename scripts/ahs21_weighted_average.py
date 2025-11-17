#%% RUN 
# import needed modules
print('Importing needed modules')
import os
import numpy as np
import pandas as pd

#Enter the number of rows wanted
ap = 6 #number of apartments
at = 6 #number of attached homes
de = 5 #number of detached homes
mh = 1 #number of manufacured homes

#%% RUN User defines directory path for datset, dataset used, and dataset final location
# User set absolute_path
absolute_path = 'C:/Users/nml/OneDrive - NIST/Documents/NIST/suit_of_homes_research/' #USER ENTERED PROJECT PATH
os.chdir(absolute_path)

apartment = pd.read_csv('ahs21_apartment_characteristics.csv')
apartment = apartment[apartment['year_built']==6].drop(['count', 'running_%'], axis=1)
apartment = apartment.reset_index(drop=True).head(ap)

attached = pd.read_csv('ahs21_attached_characteristics.csv')
attached = attached[attached['year_built']==6].drop(['count', 'running_%'], axis=1)
attached = attached.reset_index(drop=True).head(at)

detached = pd.read_csv('ahs21_detached_characteristics.csv')
detached = detached[detached['year_built']==6].drop(['count', 'running_%'], axis=1)
detached = detached.reset_index(drop=True).head(de)

mobile_home = pd.read_csv('ahs21_mobile_home_characteristics.csv')
mobile_home = mobile_home[mobile_home['year_built']==6].drop(['count', 'running_%'], axis=1)
mobile_home = mobile_home.reset_index(drop=True).head(mh)
# %%
print('apartment')
print(apartment.groupby(['UNITSIZE','#_of_units'])['weight'].sum())
print('attached')
print(attached.groupby('UNITSIZE')['weight'].sum())
print('detached')
print(detached.groupby('UNITSIZE')['weight'].sum())
print('mobile_home')
print(mobile_home.groupby('UNITSIZE')['weight'].sum())