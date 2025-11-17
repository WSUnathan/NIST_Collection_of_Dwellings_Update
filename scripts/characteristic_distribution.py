# -*- coding: utf-8 -*-
#%% RUN 
# import needed modules
print('Importing needed modules')
import os
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models.tools import HoverTool, CrosshairTool, Span
from bokeh.layouts import gridplot
from bokeh.models import CrosshairTool, Span

#%% RUN User defines directory path for datset, dataset used, and dataset final location
# User set absolute_path
absolute_path = 'C:/Users/nml/OneDrive - NIST/Documents/NIST/suit_of_homes_research/' #USER ENTERED PROJECT PATH
os.chdir(absolute_path)

# use only one dataset at a time
dataset = 'recs20' #USER ENTERED select 'recs20' or 'ahs21'
print('dataset selected: '+dataset)

# Set up Datasets that are used
print(dataset + ' dataset selected and final file path defined')
if dataset == 'recs20':
    #df = pd.read_csv("./recs_data/2020/recs2020_public_v2.csv") #USER ENTERED FINAL PATH FOR RECS
    df = pd.read_csv("./recs_data/2020/RECS2020_NIST.csv") #USER ENTERED FINAL PATH FOR RECS
    df.rename(columns = {'NWEIGHT':'weight', 'BEDROOMS':'#_of_bedrooms', 'NCOMBATH':'#_of_bathrooms', 'NHAFBATH':'#_of_halfbathrooms', 'OTHROOMS':'#_of_otherrooms', 'WINDOWS':'#_of_windows', 'SQFTRANGE':'sqft'}, inplace = True)
elif dataset == 'ahs21':
    df = pd.read_csv("./ahs_data/2021/household.csv") #USER ENTERED FINAL PATH FOR AHS
    df.replace('\'','',regex=True,inplace=True)
    df.drop(df.index[df['BLD']=='10'],inplace=True) #remove boat_rv_etc
    df.drop(df.index[df['UNITSIZE']=='-9'],inplace=True) #remove all units without a sqft size 
    df=df.copy()
    df.rename(columns = {'BEDROOMS':'#_of_bedrooms', 'WEIGHT':'weight', 'UNITSIZE':'sqft'}, inplace = True)

#%% RUN
#Replace columns data with common values'
print('Replace columns data with common values')
if dataset == 'recs20':
    print('RECs dataset know problems')
    df.loc[df["TYPEHUQ"] == 1, "TypeofHousehold"] = "mobile_home"
    df.loc[df["TYPEHUQ"] == 2, "TypeofHousehold"] = "detached"
    df.loc[df["TYPEHUQ"] == 3, "TypeofHousehold"] = "attached"
    df.loc[df["TYPEHUQ"] == 4, "TypeofHousehold"] = "apartment"
    df.loc[df["TYPEHUQ"] == 5, "TypeofHousehold"] = "apartment"
    # forced-air system
    # (1)No & (2)Yes
    df.loc[df['EQUIPM'] == 2,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 3,'forced-air'] = "2"
    df.loc[df['EQUIPM'] == 4,'forced-air'] = "2"
    df.loc[df['EQUIPM'] == 5,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 7,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 8,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 10,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 13,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 99,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == -2,'forced-air'] = "1"
        # Year Built are grouped as 
    # To match the LBL residential diagnostics database for envelope leakage:
    #   (1)before 1960, (2)1960-1969, (3)1970-1979, (4)1980-1989, (5)1990-1999, (6)after 2000 
    # To most closely match past study:
    #   (1)before 1940, (2)1940-1969, (3)1970-1989, (4)1990-1999, (5)after 2000
    df.loc[df["YEARMADERANGE"] == 1, "year_built"] = "1" #1 = Before 1950
    df.loc[df["YEARMADERANGE"] == 2, "year_built"] = "1" #2 = 1950 to 1959
    df.loc[df["YEARMADERANGE"] == 3, "year_built"] = "2" #3 = 1960 to 1969
    df.loc[df["YEARMADERANGE"] == 4, "year_built"] = "3" #4 = 1970 to 1979
    df.loc[df["YEARMADERANGE"] == 5, "year_built"] = "4" #5 = 1980 to 1989
    df.loc[df["YEARMADERANGE"] == 6, "year_built"] = "5" #6 = 1990 to 1999
    df.loc[df["YEARMADERANGE"] == 7, "year_built"] = "6" #7 = 2000 to 2009
    df.loc[df["YEARMADERANGE"] == 8, "year_built"] = "6" #8 = 2010 to 2015
    df.loc[df["YEARMADERANGE"] == 9, "year_built"] = "6" #9 = 2016 to 2020
    # garage
    # change valued to match past study
    # (1)No & (2)Yes
    df.loc[df['SIZEOFGARAGE'] == 1, "garage"] = "2"
    df.loc[df['SIZEOFGARAGE'] == 2, "garage"] = "2"
    df.loc[df['SIZEOFGARAGE'] == 3, "garage"] = "2"
    df.loc[df['SIZEOFGARAGE'] == -2, "garage"] = "1"
    # number of floors
    # true values 
    df.loc[df['STORIES'] == 1, "#_of_floors"] = "1"
    df.loc[df['STORIES'] == 2, "#_of_floors"] = "2"
    df.loc[df['STORIES'] == 3, "#_of_floors"] = "3"
    df.loc[df['STORIES'] == 4, "#_of_floors"] = "3"
    df.loc[df['STORIES'] == 5, "#_of_floors"] = "sl"
    df.loc[df['STORIES'] == -2, "#_of_floors"] = "n/a"
    # foundation
    # (1)concrete slab, (2)crawl space, (3)Basement, (4)n/a
    df.loc[(df[['CELLAR','CRAWL','CONCRETE']] == -2).any(axis=1), "foundation"] = "4"
    df.loc[(df['CELLAR'] == 0) & (df['CRAWL'] == 0) & (df['CONCRETE'] == 1), "foundation"] = "1"
    df.loc[(df['CELLAR'] == 0) & (df['CRAWL'] == 1) & (df['CONCRETE'] == 0), "foundation"] = "2"
    df.loc[(df['CELLAR'] == 1) & (df['CRAWL'] == 0) & (df['CONCRETE'] == 0), "foundation"] = "3"
    df.loc[(df['CELLAR'] == 0) & (df['CRAWL'] == 0) & (df['CONCRETE'] == 0), "foundation"] = "4"
    df.loc[(df['CELLAR'] == 1) & (df['CRAWL'] == 1) & (df['CONCRETE'] == 0), "foundation"] = "4"
    df.loc[(df['CELLAR'] == 0) & (df['CRAWL'] == 1) & (df['CONCRETE'] == 1), "foundation"] = "4"
    df.loc[(df['CELLAR'] == 1) & (df['CRAWL'] == 0) & (df['CONCRETE'] == 1), "foundation"] = "4"
    df.loc[(df['CELLAR'] == 1) & (df['CRAWL'] == 1) & (df['CONCRETE'] == 1), "foundation"] = "4"
    # air conditioning set up
    # (1)Central system, (2)Individual units, (3)Both, (4)None
    # If using the recs public file the A/C set up will be a "ACEQUIPM_pub" call, If using the EIA nonpublic recs file the call will be "ACEQUIPM_PUB".
    df.loc[df['ACEQUIPM_PUB'] == 1, "air_conditioning"] = "1" # Central system
    df.loc[df['ACEQUIPM_PUB'] == 3, "air_conditioning"] = "2" # Individual units
    df.loc[df['ACEQUIPM_PUB'] == 4, "air_conditioning"] = "2" # Individual units
    df.loc[df['ACEQUIPM_PUB'] == 5, "air_conditioning"] = "2" # Individual units
    df.loc[df['ACEQUIPM_PUB'] == 6, "air_conditioning"] = "2" # Individual units
    df.loc[df['ACEQUIPM_PUB'] == -2, "air_conditioning"] = "4" # None
    # mobile_home floor_area
    # (1)less than 1500sq/sf (2)greater than 1500sq/ft
    df.loc[(df["sqft"] == 1) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #1 = Less than 600 square feet
    df.loc[(df["sqft"] == 2) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #2 = 600 to 799 square feet
    df.loc[(df["sqft"] == 3) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #3 = 800 to 999 square feet
    df.loc[(df["sqft"] == 4) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #4 = 1,000 to 1,499 square feet
    df.loc[(df["sqft"] == 5) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #5 = 1,500 to 1,999 square feet
    df.loc[(df["sqft"] == 6) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #6 = 2,000 to 2,499 square feet
    df.loc[(df["sqft"] == 7) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #7 = 2,500 to 2,999 square feet
    df.loc[(df["sqft"] == 8) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #8 = 3,000 square feet or more
    # attached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["sqft"] == 1) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #1 = Less than 600 square feet
    df.loc[(df["sqft"] == 2) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #2 = 600 to 799 square feet
    df.loc[(df["sqft"] == 3) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #3 = 800 to 999 square feet
    df.loc[(df["sqft"] == 4) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #4 = 1,000 to 1,499 square feet
    df.loc[(df["sqft"] == 5) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "2" #5 = 1,500 to 1,999 square feet
    df.loc[(df["sqft"] == 6) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "2" #6 = 2,000 to 2,499 square feet
    df.loc[(df["sqft"] == 7) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #7 = 2,500 to 2,999 square feet
    df.loc[(df["sqft"] == 8) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #8 = 3,000 square feet or more
    # detached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["sqft"] == 1) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #1 = Less than 600 square feet
    df.loc[(df["sqft"] == 2) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #2 = 600 to 799 square feet
    df.loc[(df["sqft"] == 3) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #3 = 800 to 999 square feet
    df.loc[(df["sqft"] == 4) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #4 = 1,000 to 1,499 square feet
    df.loc[(df["sqft"] == 5) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "2" #5 = 1,500 to 1,999 square feet
    df.loc[(df["sqft"] == 6) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "2" #6 = 2,000 to 2,499 square feet
    df.loc[(df["sqft"] == 7) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #7 = 2,500 to 2,999 square feet
    df.loc[(df["sqft"] == 8) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #8 = 3,000 square feet or more
    # apartment floor_area
    # (1)less than 1000sq/sf (2)greater than 1000sq/ft
    df.loc[(df["sqft"] == 1) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #1 = Less than 600 square feet
    df.loc[(df["sqft"] == 2) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #2 = 600 to 799 square feet
    df.loc[(df["sqft"] == 3) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #3 = 800 to 999 square feet
    df.loc[(df["sqft"] == 4) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #4 = 1,000 to 1,499 square feet
    df.loc[(df["sqft"] == 5) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #5 = 1,500 to 1,999 square feet
    df.loc[(df["sqft"] == 6) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #6 = 2,000 to 2,499 square feet
    df.loc[(df["sqft"] == 7) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #7 = 2,500 to 2,999 square feet
    df.loc[(df["sqft"] == 8) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #8 = 3,000 square feet or more
    # number of units
    # (1)2-4 (2)5-9 (3)10-19 (4)20-49 (5)>50
    df.loc[df["TYPEHUQ"] == 1, "#_of_units"] = "n/a"
    df.loc[df["TYPEHUQ"] == 2, "#_of_units"] = "n/a"
    df.loc[df["TYPEHUQ"] == 3, "#_of_units"] = "n/a"
    df.loc[df["TYPEHUQ"] == 4, "#_of_units"] = "1"
    df.loc[(df["TYPEHUQ"] == 5) & (df["building_units"] >= 2) & (df["building_units"] <= 4), "#_of_units"] = "1"
    df.loc[(df["TYPEHUQ"] == 5) & (df["building_units"] >= 5) & (df["building_units"] <= 9), "#_of_units"] = "2"
    df.loc[(df["TYPEHUQ"] == 5) & (df["building_units"] >= 10) & (df["building_units"] <= 19), "#_of_units"] = "3"
    df.loc[(df["TYPEHUQ"] == 5) & (df["building_units"] >= 20) & (df["building_units"] <= 49), "#_of_units"] = "4"
    df.loc[(df["TYPEHUQ"] == 5) & (df["building_units"] >= 50), "#_of_units"] = "5"
    df.loc[(df["TYPEHUQ"] == 5) & (df["building_units"] == 1), "#_of_units"] = "TEST" #This was not expected to be needed, it also does not make since that it is there.
elif dataset == 'ahs21':
    print('AHS dataset known problems')
    df.loc[df["BLD"] == '01', "TypeofHousehold"] = "mobile_home"
    df.loc[df["BLD"] == '02', "TypeofHousehold"] = "detached"
    df.loc[df["BLD"] == '03', "TypeofHousehold"] = "attached"
    df.loc[df["BLD"] == '04', "TypeofHousehold"] = "apartment"
    df.loc[df["BLD"] == '05', "TypeofHousehold"] = "apartment"
    df.loc[df["BLD"] == '06', "TypeofHousehold"] = "apartment"
    df.loc[df["BLD"] == '07', "TypeofHousehold"] = "apartment"
    df.loc[df["BLD"] == '08', "TypeofHousehold"] = "apartment"
    df.loc[df["BLD"] == '09', "TypeofHousehold"] = "apartment"
    df.loc[df["BLD"] == '10', "TypeofHousehold"] = "boat_rv_etc" 
    # forced air
    # (1)No, (2)Yes
    df.loc[df["HEATTYPE"] == '01', "forced-air"] = "2"
    df.loc[df["HEATTYPE"] == '02', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '03', "forced-air"] = "2"
    df.loc[df["HEATTYPE"] == '04', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '05', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '06', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '07', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '08', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '09', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '10', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '11', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '12', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '13', "forced-air"] = "1"
    df.loc[df["HEATTYPE"] == '14', "forced-air"] = "1"
    # Year Built are grouped as 
    # To match the LBL residential diagnostics database for envelope leakage:
    #   (1)before 1960, (2)1960-1969, (3)1970-1979, (4)1980-1989, (5)1990-1999, (6)after 2000 
    # To most closely match past study:
    #   (1)before 1940, (2)1940-1969, (3)1970-1989, (4)1990-1999, (5)after 2000
    df.loc[df["YRBUILT"] == 1919, "year_built"] = "1" #1919 = 1919 or earlier
    df.loc[df["YRBUILT"] == 1920, "year_built"] = "1" #1920 = 1920 to 1929
    df.loc[df["YRBUILT"] == 1930, "year_built"] = "1" #1930 = 1930 to 1939
    df.loc[df["YRBUILT"] == 1940, "year_built"] = "1" #1940 = 1940 to 1949
    df.loc[df["YRBUILT"] == 1950, "year_built"] = "1" #1950 = 1950 to 1959
    df.loc[df["YRBUILT"] == 1960, "year_built"] = "2" #1960 = 1960 to 1969
    df.loc[df["YRBUILT"] == 1970, "year_built"] = "3" #1970 = 1970 to 1979
    df.loc[df["YRBUILT"] == 1980, "year_built"] = "4" #1980 = 1980 to 1989
    df.loc[df["YRBUILT"] == 1990, "year_built"] = "5" #1990 = 1990 to 1999
    df.loc[df["YRBUILT"] >= 2000, "year_built"] = "6" #2000 = 2000 to 2009 The > catches all values higher up to 2021
    # mobile_home floor_area
    # (1)less than 1500sq/sf (2)greater than 1500sq/ft
    df.loc[(df["sqft"] == '1') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["sqft"] == '2') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["sqft"] == '3') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["sqft"] == '4') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["sqft"] == '5') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["sqft"] == '6') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["sqft"] == '7') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["sqft"] == '8') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["sqft"] == '9') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'9' = 4,000 square feet or more
    df.loc[(df["sqft"] == '-9') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "n/a" #'-9' = Not reported
    # attached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["sqft"] == '1') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["sqft"] == '2') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["sqft"] == '3') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["sqft"] == '4') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["sqft"] == '5') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["sqft"] == '6') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["sqft"] == '7') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["sqft"] == '8') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["sqft"] == '9') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'9' = 4,000 square feet or more
    df.loc[(df["sqft"] == '-9') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "n/a" #'-9' = Not reported
    # detached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["sqft"] == '1') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["sqft"] == '2') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["sqft"] == '3') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["sqft"] == '4') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["sqft"] == '5') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["sqft"] == '6') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["sqft"] == '7') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["sqft"] == '8') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["sqft"] == '9') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'9' = 4,000 square feet or more
    df.loc[(df["sqft"] == '-9') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "n/a" #'-9' = Not reported
    # apartment floor_area
    # (1)less than 1000sq/sf (2)greater than 1000sq/ft
    df.loc[(df["sqft"] == '1') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["sqft"] == '2') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["sqft"] == '3') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["sqft"] == '4') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["sqft"] == '5') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["sqft"] == '6') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["sqft"] == '7') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["sqft"] == '8') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["sqft"] == '9') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'9' = 4,000 square feet or more
    df.loc[(df["sqft"] == '-9') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "n/a" #'-9' = Not reported
    # garage
    # change valued to match past study
    # (1)No & (2)Yes
    df.loc[df['GARAGE'] == '1', "garage"] = "2"
    df.loc[df['GARAGE'] == '2', "garage"] = "1"
    df.loc[df['GARAGE'] == '-9', "garage"] = "1"
    # number of floors
    # true values
    df["STORIES_temp"] = df['STORIES'].mask(df.FOUNDTYPE == '1',df['STORIES']-1)
    df.loc[df['STORIES_temp'] == 1, "#_of_floors"] = "1"
    df.loc[df['STORIES_temp'] == 2, "#_of_floors"] = "2"
    df.loc[df['STORIES_temp'] == 3, "#_of_floors"] = "3"
    df.loc[df['STORIES_temp'] == 4, "#_of_floors"] = "3"
    df.loc[df['STORIES_temp'] == 5, "#_of_floors"] = "3"
    df.loc[df['STORIES_temp'] == 6, "#_of_floors"] = "4"
    df.loc[df['STORIES_temp'] == 7, "#_of_floors"] = "4"
    # foundation
    # (1)concrete slab, (2)crawl space, (3)Basement, (4)n/a
    df.loc[df['FOUNDTYPE'] == '4', "foundation"] = "1"
    df.loc[df['FOUNDTYPE'] == '3', "foundation"] = "2"
    df.loc[df['FOUNDTYPE'] == '1', "foundation"] = "3"
    df.loc[df['FOUNDTYPE'] == '2', "foundation"] = "4"
    df.loc[df['FOUNDTYPE'] == '5', "foundation"] = "4"
    df.loc[df['FOUNDTYPE'] == '6', "foundation"] = "4"
    df.loc[df['FOUNDTYPE'] == '7', "foundation"] = "4"
    df.loc[df['FOUNDTYPE'] == '8', "foundation"] = "4"
    df.loc[df['FOUNDTYPE'] == '9', "foundation"] = "4"
    df.loc[df['FOUNDTYPE'] == '-6', "foundation"] = "4"
    # number of units
    # (1)2-4units, (2)5-9units, (3)10-19units, (4)20-49units, (5)50 or more units
    df.loc[df['BLD'] == '04', "#_of_units"] = "1"
    df.loc[df['BLD'] == '05', "#_of_units"] = "1"
    df.loc[df['BLD'] == '06', "#_of_units"] = "2"
    df.loc[df['BLD'] == '07', "#_of_units"] = "3"
    df.loc[df['BLD'] == '08', "#_of_units"] = "4" #this does not match original dataset
    df.loc[df['BLD'] == '09', "#_of_units"] = "5" #this does not match original dataset
    df.loc[df['BLD'] == '03', "#_of_units"] = "n/a"
    df.loc[df['BLD'] == '02', "#_of_units"] = "n/a"
    df.loc[df['BLD'] == '01', "#_of_units"] = "n/a"
    # Bathroom data setup
    # true values
    df.loc[df['BATHROOMS'] == '01', "#_of_bathrooms"] = "1"
    df.loc[df['BATHROOMS'] == '02', "#_of_bathrooms"] = "1"
    df.loc[df['BATHROOMS'] == '03', "#_of_bathrooms"] = "2"
    df.loc[df['BATHROOMS'] == '04', "#_of_bathrooms"] = "2"
    df.loc[df['BATHROOMS'] == '05', "#_of_bathrooms"] = "3"
    df.loc[df['BATHROOMS'] == '06', "#_of_bathrooms"] = "4" # more then three
    df.loc[df['BATHROOMS'] == '07', "#_of_bathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '08', "#_of_bathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '09', "#_of_bathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '11', "#_of_bathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '12', "#_of_bathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '13', "#_of_bathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '02', "#_of_halfbathrooms"] = "1"
    df.loc[df['BATHROOMS'] == '04', "#_of_halfbathrooms"] = "1"
    df.loc[df['BATHROOMS'] == '01', "#_of_halfbathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '03', "#_of_halfbathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '05', "#_of_halfbathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '06', "#_of_halfbathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '07', "#_of_halfbathrooms"] = "1"
    df.loc[df['BATHROOMS'] == '08', "#_of_halfbathrooms"] = "1"
    df.loc[df['BATHROOMS'] == '09', "#_of_halfbathrooms"] = "1"
    df.loc[df['BATHROOMS'] == '11', "#_of_halfbathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '12', "#_of_halfbathrooms"] = "0"
    df.loc[df['BATHROOMS'] == '13', "#_of_halfbathrooms"] = "0"
    # other rooms
    df['#_of_otherrooms'] = ''
    print('using total rooms and removing bedrooms and bathrooms leads to negative numbers')
    # windows
    df['#_of_windows'] = ''
    print('number of windows is not a variable in the ACH database')
    # air conditioning set up
    # (1)Central system, (2)Individual units, (3)Both, (4)None
    df.loc[df['ACPRIMARY'] == '01', "air_conditioning"] = "1" # Central system
    df.loc[df['ACPRIMARY'] == '02', "air_conditioning"] = "1" # Central system
    df.loc[df['ACPRIMARY'] == '03', "air_conditioning"] = "1" # Central system
    df.loc[df['ACPRIMARY'] == '04', "air_conditioning"] = "1" # Central system
    df.loc[df['ACPRIMARY'] == '05', "air_conditioning"] = "2" # Individual units
    df.loc[df['ACPRIMARY'] == '06', "air_conditioning"] = "2" # Individual units
    df.loc[df['ACPRIMARY'] == '07', "air_conditioning"] = "2" # Individual units
    df.loc[df['ACPRIMARY'] == '08', "air_conditioning"] = "2" # Individual units
    df.loc[df['ACPRIMARY'] == '09', "air_conditioning"] = "2" # Individual units
    df.loc[df['ACPRIMARY'] == '10', "air_conditioning"] = "2" # Individual units
    df.loc[df['ACPRIMARY'] == '11', "air_conditioning"] = "2" # Individual units
    df.loc[df['ACPRIMARY'] == '12', "air_conditioning"] = "4" # None
#%%
# Drop unused variable, make household dataframes, and build home definition
print('drop unused variable')
if dataset == 'recs20':
    df = df[['TypeofHousehold','#_of_floors','#_of_units','floor_area','year_built','foundation','garage','forced-air','weight','#_of_bedrooms','#_of_bathrooms','#_of_halfbathrooms','#_of_otherrooms','#_of_windows','air_conditioning','sqft',"building_units"]]
elif dataset == 'ahs21':
    df = df[['TypeofHousehold','#_of_floors','#_of_units','floor_area','year_built','foundation','garage','forced-air','weight','#_of_bedrooms','#_of_bathrooms','#_of_halfbathrooms','#_of_otherrooms','#_of_windows','air_conditioning','sqft']]

print('make four household type dataframes')
apartment = df.loc[df['TypeofHousehold'] == 'apartment', df.columns.drop(['foundation', 'garage'])]
attached = df.loc[df['TypeofHousehold'] == 'attached', df.columns.drop(['#_of_units'])]
detached = df.loc[df['TypeofHousehold'] == 'detached', df.columns.drop(['#_of_units'])]
mobile_home = df.loc[df['TypeofHousehold'] == 'mobile_home', df.columns.drop(['#_of_floors','#_of_units','foundation', 'garage'])]

print('make home definition variable w/o year')
apartment['home_definition_year'] = apartment['#_of_floors']+apartment['#_of_units']+apartment['floor_area']+apartment['forced-air']
attached['home_definition_year'] = attached['#_of_floors']+attached['floor_area']+attached['foundation']+attached['garage']+attached['forced-air']
detached['home_definition_year'] = detached['#_of_floors']+detached['floor_area']+detached['foundation']+detached['garage']+detached['forced-air']
mobile_home['home_definition_year'] = mobile_home['floor_area']+mobile_home['forced-air']

print('make home definition variable')
apartment['home_definition'] = apartment['#_of_floors']+apartment['#_of_units']+apartment['floor_area']+apartment['year_built']+apartment['forced-air']
attached['home_definition'] = attached['#_of_floors']+attached['floor_area']+attached['year_built']+attached['foundation']+attached['garage']+attached['forced-air']
detached['home_definition'] = detached['#_of_floors']+detached['floor_area']+detached['year_built']+detached['foundation']+detached['garage']+detached['forced-air']
mobile_home['home_definition'] = mobile_home['floor_area']+mobile_home['year_built']+mobile_home['forced-air']

#%% RUN to print unique home counts
# Print # of unique homes 
print('# of unique apartments: ')
print(apartment['home_definition'].nunique())
print(apartment['home_definition_year'].nunique())
print('# of unique attached homes:')
print(attached['home_definition'].nunique())
print(attached['home_definition_year'].nunique())
print('# of unique detached homes:')
print(detached['home_definition'].nunique())
print(detached['home_definition_year'].nunique())
print('# of unique mobile homes:')
print(mobile_home['home_definition'].nunique())
print(mobile_home['home_definition_year'].nunique())

#%% RUN
# Make home characteristic datasets
print('Making home characteristic datasets')
#apartment_characteristic = apartment.groupby(['home_definition']).agg({'home_definition_year':['min'],'#_of_floors':['min'],'#_of_units':['min'],'floor_area': ['min'],
#    'year_built':['min'], 'forced-air':['min'],'home_definition':['count'],'weight':['sum']}).rename(columns={'home_definition':'#_of_homes'})

if dataset == 'recs20':
    apartment_characteristic1 = apartment.groupby('home_definition').apply(lambda x: pd.Series((x['building_units']*x['weight']).sum()/x['weight'].sum(),index=['#_of_units_avg']))
    apartment_characteristic2 = apartment.groupby(['home_definition']).agg({'home_definition_year':'min','#_of_floors':'min','#_of_units':'min', 'floor_area': 'min',
    'year_built':'min','forced-air':'min','home_definition':'count','weight':'sum'}).rename(columns={'home_definition':'#_of_homes'})
    apartment_characteristic = pd.merge(apartment_characteristic1,apartment_characteristic2,on='home_definition')
    apartment_characteristic = apartment_characteristic[['home_definition_year','#_of_floors','#_of_units','#_of_units_avg','floor_area','year_built','forced-air','#_of_homes','weight']]
elif dataset == 'ahs21':
    apartment_characteristic = apartment.groupby(['home_definition']).agg({'home_definition_year':'min','#_of_floors':'min','#_of_units':'min', 'floor_area': 'min',
    'year_built':'min','forced-air':'min','home_definition':'count','weight':'sum'}).rename(columns={'home_definition':'#_of_homes'})
    apartment_characteristic = apartment_characteristic[['home_definition_year','#_of_floors','#_of_units','floor_area','year_built','forced-air','#_of_homes','weight']]

attached_characteristic = attached.groupby(['home_definition']).agg({'home_definition_year':'min','#_of_floors':'min','floor_area':'min','year_built':'min','foundation':'min',
    'garage':'min','forced-air':'min','home_definition':'count','weight':'sum',}).rename(columns={'home_definition':'#_of_homes'})

detached_characteristic = detached.groupby(['home_definition']).agg({'home_definition_year':'min','#_of_floors':'min','floor_area':'min','year_built':'min','foundation':'min',
    'garage':'min','forced-air':'min','home_definition':'count','weight':'sum',}).rename(columns={'home_definition':'#_of_homes'})

mobile_home_characteristic = mobile_home.groupby(['home_definition']).agg({'home_definition_year':'min','floor_area':'min','year_built':'min','forced-air':'min',
    'home_definition':'count','weight':'sum'}).rename(columns={'home_definition':'#_of_homes'})

# Sort datasets by ________
print('Sorting datasets by national home weight')
apartment_characteristic.sort_values(by='weight', ascending=False,inplace=True)
apartment_characteristic = apartment_characteristic.assign(count=range(len(apartment_characteristic)))
apartment_characteristic['count'] = apartment_characteristic['count']+1
attached_characteristic.sort_values(by='weight', ascending=False,inplace=True)
attached_characteristic = attached_characteristic.assign(count=range(len(attached_characteristic)))
attached_characteristic['count'] = attached_characteristic['count']+1
detached_characteristic.sort_values(by='weight', ascending=False,inplace=True)
detached_characteristic = detached_characteristic.assign(count=range(len(detached_characteristic)))
detached_characteristic['count'] = detached_characteristic['count']+1
mobile_home_characteristic.sort_values(by='weight', ascending=False,inplace=True)
mobile_home_characteristic = mobile_home_characteristic.assign(count=range(len(mobile_home_characteristic)))
mobile_home_characteristic['count'] = mobile_home_characteristic['count']+1

# Set up plotting variables
apartment_characteristic['running_%']=(apartment_characteristic['weight'].cumsum()/apartment_characteristic['weight'].sum())*100
attached_characteristic['running_%']=(attached_characteristic['weight'].cumsum()/attached_characteristic['weight'].sum())*100
detached_characteristic['running_%']=(detached_characteristic['weight'].cumsum()/detached_characteristic['weight'].sum())*100
mobile_home_characteristic['running_%']=(mobile_home_characteristic['weight'].cumsum()/mobile_home_characteristic['weight'].sum())*100

#%% RUN for plot
# Plot Percentage coverage as a function of dataset sample size
output_file("YearBuiltRemoved_Percentage_coverage_" + dataset + "_update.html")

p = figure(x_range=[0, 850], y_range=[0, 100], max_width=800, height=400)

p.line(apartment_characteristic['count'], apartment_characteristic['running_%'], legend_label="Apartments", line_color="red", line_dash="solid")
p.line(attached_characteristic['count'], attached_characteristic['running_%'], legend_label="Attached_Dwellings", line_color="green", line_dash= "dashed")
p.line(detached_characteristic['count'], detached_characteristic['running_%'], legend_label="Detached_Dwellings", line_color="orange", line_dash="dotted")
p.line(mobile_home_characteristic['count'], mobile_home_characteristic['running_%'], legend_label="Manufactured_Dwellings", line_color="blue", line_dash="dotdash")

#p.title.text = "Percentage coverage as a function of " + dataset + " sample size"
#p.title.text_font_size = '12pt'
#p.title.align = 'center'

p.xaxis.axis_label = "Number of Dwelling  (#)"

p.yaxis.axis_label = "Percent of Building Stock Represented (%)"

p.legend.location = "bottom_right"

width = Span(dimension="width", line_width=1)
height = Span(dimension="height", line_width=1)

p.add_tools(HoverTool(tooltips=[("(#,%)","($x{0.0},$y{0.0})")]))
p.add_tools(CrosshairTool(overlay=[width, height]))

show(p)

#%% RUN
# Make variables to solve for diffrent home variables 
print('make variable for number of bedrooms')
apartment['#_of_bedrooms_variable'] = apartment['#_of_floors']+apartment['#_of_units']+apartment['floor_area']+apartment['year_built']+apartment['forced-air']+apartment['#_of_bedrooms'].apply(str)
attached['#_of_bedrooms_variable'] = attached['#_of_floors']+attached['floor_area']+attached['year_built']+attached['foundation']+attached['garage']+attached['forced-air']+attached['#_of_bedrooms'].apply(str)
detached['#_of_bedrooms_variable'] = detached['#_of_floors']+detached['floor_area']+detached['year_built']+detached['foundation']+detached['garage']+detached['forced-air']+detached['#_of_bedrooms'].apply(str)
mobile_home['#_of_bedrooms_variable'] = mobile_home['floor_area']+mobile_home['year_built']+mobile_home['forced-air']+mobile_home['#_of_bedrooms'].apply(str)

print('make variable for number of bathrooms')
apartment['#_of_bathrooms_variable'] = apartment['#_of_floors']+apartment['#_of_units']+apartment['floor_area']+apartment['year_built']+apartment['forced-air']+apartment['#_of_bathrooms'].apply(str)
attached['#_of_bathrooms_variable'] = attached['#_of_floors']+attached['floor_area']+attached['year_built']+attached['foundation']+attached['garage']+attached['forced-air']+attached['#_of_bathrooms'].apply(str)
detached['#_of_bathrooms_variable'] = detached['#_of_floors']+detached['floor_area']+detached['year_built']+detached['foundation']+detached['garage']+detached['forced-air']+detached['#_of_bathrooms'].apply(str)
mobile_home['#_of_bathrooms_variable'] = mobile_home['floor_area']+mobile_home['year_built']+mobile_home['forced-air']+mobile_home['#_of_bathrooms'].apply(str)

print('make variable for number of halfbathrooms')
apartment['#_of_halfbathrooms_variable'] = apartment['#_of_floors']+apartment['#_of_units']+apartment['floor_area']+apartment['year_built']+apartment['forced-air']+apartment['#_of_halfbathrooms'].apply(str)
attached['#_of_halfbathrooms_variable'] = attached['#_of_floors']+attached['floor_area']+attached['year_built']+attached['foundation']+attached['garage']+attached['forced-air']+attached['#_of_halfbathrooms'].apply(str)
detached['#_of_halfbathrooms_variable'] = detached['#_of_floors']+detached['floor_area']+detached['year_built']+detached['foundation']+detached['garage']+detached['forced-air']+detached['#_of_halfbathrooms'].apply(str)
mobile_home['#_of_halfbathrooms_variable'] = mobile_home['floor_area']+mobile_home['year_built']+mobile_home['forced-air']+mobile_home['#_of_halfbathrooms'].apply(str)

print('make variable for number of other rooms')
apartment['#_of_otherrooms_variable'] = apartment['#_of_floors']+apartment['#_of_units']+apartment['floor_area']+apartment['year_built']+apartment['forced-air']+apartment['#_of_otherrooms'].apply(str)
attached['#_of_otherrooms_variable'] = attached['#_of_floors']+attached['floor_area']+attached['year_built']+attached['foundation']+attached['garage']+attached['forced-air']+attached['#_of_otherrooms'].apply(str)
detached['#_of_otherrooms_variable'] = detached['#_of_floors']+detached['floor_area']+detached['year_built']+detached['foundation']+detached['garage']+detached['forced-air']+detached['#_of_otherrooms'].apply(str)
mobile_home['#_of_otherrooms_variable'] = mobile_home['floor_area']+mobile_home['year_built']+mobile_home['forced-air']+mobile_home['#_of_otherrooms'].apply(str)

print('make variable for air_conditioning type')
apartment['air_conditioning_variable'] = apartment['#_of_floors']+apartment['#_of_units']+apartment['floor_area']+apartment['year_built']+apartment['forced-air']+apartment['air_conditioning'].apply(str)
attached['air_conditioning_variable'] = attached['#_of_floors']+attached['floor_area']+attached['year_built']+attached['foundation']+attached['garage']+attached['forced-air']+attached['air_conditioning'].apply(str)
detached['air_conditioning_variable'] = detached['#_of_floors']+detached['floor_area']+detached['year_built']+detached['foundation']+detached['garage']+detached['forced-air']+detached['air_conditioning'].apply(str)
mobile_home['air_conditioning_variable'] = mobile_home['floor_area']+mobile_home['year_built']+mobile_home['forced-air']+mobile_home['air_conditioning'].apply(str)

# Make home characteristic for floorplan determination
print('Making home characteristic for apartment floorplan determination')
apartment_bedrooms_characteristic = apartment.groupby(['#_of_bedrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'#_of_units':['min'],'floor_area': ['min'],
    'year_built':['min'], 'forced-air':['min'],'#_of_bedrooms':['min'],'weight':['sum']})
apartment_bedrooms_characteristic.columns = apartment_bedrooms_characteristic.columns.droplevel(1)
apartment_bathrooms_characteristic = apartment.groupby(['#_of_bathrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'#_of_units':['min'],'floor_area': ['min'],
    'year_built':['min'], 'forced-air':['min'],'#_of_bathrooms':['min'],'weight':['sum']})
apartment_bathrooms_characteristic.columns = apartment_bathrooms_characteristic.columns.droplevel(1)
apartment_halfbathrooms_characteristic = apartment.groupby(['#_of_halfbathrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'#_of_units':['min'],'floor_area': ['min'],
    'year_built':['min'], 'forced-air':['min'],'#_of_halfbathrooms':['min'],'weight':['sum']})
apartment_halfbathrooms_characteristic.columns = apartment_halfbathrooms_characteristic.columns.droplevel(1)
apartment_otherrooms_characteristic = apartment.groupby(['#_of_otherrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'#_of_units':['min'],'floor_area': ['min'],
    'year_built':['min'], 'forced-air':['min'],'#_of_otherrooms':['min'],'weight':['sum']})
apartment_otherrooms_characteristic.columns = apartment_otherrooms_characteristic.columns.droplevel(1)
apartment_air_conditioning_characteristic = apartment.groupby(['air_conditioning_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'#_of_units':['min'],'floor_area': ['min'],
    'year_built':['min'], 'forced-air':['min'],'air_conditioning':['min'],'weight':['sum']})
apartment_air_conditioning_characteristic.columns = apartment_air_conditioning_characteristic.columns.droplevel(1)

print('Making home characteristic for attached floorplan determination')
attached_bedrooms_characteristic = attached.groupby(['#_of_bedrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'#_of_bedrooms':['min'],'weight':['sum'],})
attached_bedrooms_characteristic.columns = attached_bedrooms_characteristic.columns.droplevel(1)
attached_bathrooms_characteristic = attached.groupby(['#_of_bathrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'#_of_bathrooms':['min'],'weight':['sum'],})
attached_bathrooms_characteristic.columns = attached_bathrooms_characteristic.columns.droplevel(1)
attached_halfbathrooms_characteristic = attached.groupby(['#_of_halfbathrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'#_of_halfbathrooms':['min'],'weight':['sum'],})
attached_halfbathrooms_characteristic.columns = attached_halfbathrooms_characteristic.columns.droplevel(1)
attached_otherrooms_characteristic = attached.groupby(['#_of_otherrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'#_of_otherrooms':['min'],'weight':['sum'],})
attached_otherrooms_characteristic.columns = attached_otherrooms_characteristic.columns.droplevel(1)
attached_air_conditioning_characteristic = attached.groupby(['air_conditioning_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'air_conditioning':['min'],'weight':['sum'],})
attached_air_conditioning_characteristic.columns = attached_air_conditioning_characteristic.columns.droplevel(1)

print('Making home characteristic for detached floorplan determination')
detached_bedrooms_characteristic = detached.groupby(['#_of_bedrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'#_of_bedrooms':['min'],'weight':['sum'],})
detached_bedrooms_characteristic.columns = detached_bedrooms_characteristic.columns.droplevel(1)
detached_bathrooms_characteristic = detached.groupby(['#_of_bathrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'#_of_bathrooms':['min'],'weight':['sum'],})
detached_bathrooms_characteristic.columns = detached_bathrooms_characteristic.columns.droplevel(1)
detached_halfbathrooms_characteristic = detached.groupby(['#_of_halfbathrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'#_of_halfbathrooms':['min'],'weight':['sum'],})
detached_halfbathrooms_characteristic.columns = detached_halfbathrooms_characteristic.columns.droplevel(1)
detached_otherrooms_characteristic = detached.groupby(['#_of_otherrooms_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'#_of_otherrooms':['min'],'weight':['sum'],})
detached_otherrooms_characteristic.columns = detached_otherrooms_characteristic.columns.droplevel(1)
detached_air_conditioning_characteristic = detached.groupby(['air_conditioning_variable']).agg({'home_definition':['min'],'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'air_conditioning':['min'],'weight':['sum'],})
detached_air_conditioning_characteristic.columns = detached_air_conditioning_characteristic.columns.droplevel(1)

print('Making home characteristic for mobile_home floorplan determination')
mobile_home_bedrooms_characteristic = mobile_home.groupby(['#_of_bedrooms_variable']).agg({'home_definition':['min'],'floor_area': ['min'],'year_built':['min'],
    'forced-air':['min'],'#_of_bedrooms':['min'],'weight':['sum']})
mobile_home_bedrooms_characteristic.columns = mobile_home_bedrooms_characteristic.columns.droplevel(1)
mobile_home_bathrooms_characteristic = mobile_home.groupby(['#_of_bathrooms_variable']).agg({'home_definition':['min'],'floor_area': ['min'],'year_built':['min'],
    'forced-air':['min'],'#_of_bathrooms':['min'],'weight':['sum']})
mobile_home_bathrooms_characteristic.columns = mobile_home_bathrooms_characteristic.columns.droplevel(1)
mobile_home_halfbathrooms_characteristic = mobile_home.groupby(['#_of_halfbathrooms_variable']).agg({'home_definition':['min'],'floor_area': ['min'],'year_built':['min'],
    'forced-air':['min'],'#_of_halfbathrooms':['min'],'weight':['sum']})
mobile_home_halfbathrooms_characteristic.columns = mobile_home_halfbathrooms_characteristic.columns.droplevel(1)
mobile_home_otherrooms_characteristic = mobile_home.groupby(['#_of_otherrooms_variable']).agg({'home_definition':['min'],'floor_area': ['min'],'year_built':['min'],
    'forced-air':['min'],'#_of_otherrooms':['min'],'weight':['sum']})
mobile_home_otherrooms_characteristic.columns = mobile_home_otherrooms_characteristic.columns.droplevel(1)
mobile_home_air_conditioning_characteristic = mobile_home.groupby(['air_conditioning_variable']).agg({'home_definition':['min'],'floor_area': ['min'],'year_built':['min'],
    'forced-air':['min'],'air_conditioning':['min'],'weight':['sum']})
mobile_home_air_conditioning_characteristic.columns = mobile_home_air_conditioning_characteristic.columns.droplevel(1)

# Sorting  home characteristic datasets by home variable charachteristics'
print('Sorting datasets by home variable charachteristics')
apartment_bedrooms_characteristic.sort_values(by='#_of_bedrooms_variable', ascending=True,inplace=True)
apartment_bathrooms_characteristic.sort_values(by='#_of_bathrooms_variable', ascending=True,inplace=True)
apartment_halfbathrooms_characteristic.sort_values(by='#_of_halfbathrooms_variable', ascending=True,inplace=True)
apartment_otherrooms_characteristic.sort_values(by='#_of_otherrooms_variable', ascending=True,inplace=True)
apartment_air_conditioning_characteristic.sort_values(by='air_conditioning_variable', ascending=True,inplace=True)
attached_bedrooms_characteristic.sort_values(by='#_of_bedrooms_variable', ascending=True,inplace=True)
attached_bathrooms_characteristic.sort_values(by='#_of_bathrooms_variable', ascending=True,inplace=True)
attached_halfbathrooms_characteristic.sort_values(by='#_of_halfbathrooms_variable', ascending=True,inplace=True)
attached_otherrooms_characteristic.sort_values(by='#_of_otherrooms_variable', ascending=True,inplace=True)
attached_air_conditioning_characteristic.sort_values(by='air_conditioning_variable', ascending=True,inplace=True)
detached_bedrooms_characteristic.sort_values(by='#_of_bedrooms_variable', ascending=True,inplace=True)
detached_bathrooms_characteristic.sort_values(by='#_of_bathrooms_variable', ascending=True,inplace=True)
detached_halfbathrooms_characteristic.sort_values(by='#_of_halfbathrooms_variable', ascending=True,inplace=True)
detached_otherrooms_characteristic.sort_values(by='#_of_otherrooms_variable', ascending=True,inplace=True)
detached_air_conditioning_characteristic.sort_values(by='air_conditioning_variable', ascending=True,inplace=True)
mobile_home_bedrooms_characteristic.sort_values(by='#_of_bedrooms_variable', ascending=True,inplace=True)
mobile_home_bathrooms_characteristic.sort_values(by='#_of_bathrooms_variable', ascending=True,inplace=True)
mobile_home_halfbathrooms_characteristic.sort_values(by='#_of_halfbathrooms_variable', ascending=True,inplace=True)
mobile_home_otherrooms_characteristic.sort_values(by='#_of_otherrooms_variable', ascending=True,inplace=True)
mobile_home_air_conditioning_characteristic.sort_values(by='air_conditioning_variable', ascending=True,inplace=True)

#%% RUN to Write home characteristics excel files
# Write all home characteristics datasets to excel files
print('Write apartment characteristics datasets to excel file')
with pd.ExcelWriter(dataset+"_apartment_characteristics.xlsx") as writer:
    # use to_excel function and specify the sheet_name and index
    # to store the dataframe in specified sheet
    apartment_characteristic.to_excel(writer, sheet_name="apartment_characteristic", index=True)
    apartment_bedrooms_characteristic.to_excel(writer, sheet_name="bedrooms", index=True)
    apartment_bathrooms_characteristic.to_excel(writer, sheet_name="bathrooms", index=True)
    apartment_halfbathrooms_characteristic.to_excel(writer, sheet_name="halfbathrooms", index=True)
    apartment_otherrooms_characteristic.to_excel(writer, sheet_name="otherrooms", index=True)
    apartment_air_conditioning_characteristic.to_excel(writer, sheet_name="air_conditioning", index=True)

print('Write attached home characteristics datasets to excel file')
with pd.ExcelWriter(dataset+"_attached_characteristics.xlsx") as writer:
    # use to_excel function and specify the sheet_name and index
    # to store the dataframe in specified sheet
    attached_characteristic.to_excel(writer, sheet_name="attached_characteristic", index=True)
    attached_bedrooms_characteristic.to_excel(writer, sheet_name="bedrooms", index=True)
    attached_bathrooms_characteristic.to_excel(writer, sheet_name="bathrooms", index=True)
    attached_halfbathrooms_characteristic.to_excel(writer, sheet_name="halfbathrooms", index=True)
    attached_otherrooms_characteristic.to_excel(writer, sheet_name="otherrooms", index=True)
    attached_air_conditioning_characteristic.to_excel(writer, sheet_name="air_conditioning", index=True)

print('Write detached home characteristics datasets to excel file')
with pd.ExcelWriter(dataset+"_detached_characteristics.xlsx") as writer:
    # use to_excel function and specify the sheet_name and index
    # to store the dataframe in specified sheet
    detached_characteristic.to_excel(writer, sheet_name="detached_characteristic", index=True)
    detached_bedrooms_characteristic.to_excel(writer, sheet_name="bedrooms", index=True)
    detached_bathrooms_characteristic.to_excel(writer, sheet_name="bathrooms", index=True)
    detached_halfbathrooms_characteristic.to_excel(writer, sheet_name="halfbathrooms", index=True)
    detached_otherrooms_characteristic.to_excel(writer, sheet_name="otherrooms", index=True)
    detached_air_conditioning_characteristic.to_excel(writer, sheet_name="air_conditioning", index=True)

print('Write mobile home characteristics datasets to excel file')
with pd.ExcelWriter(dataset+"_mobile_home_characteristics.xlsx") as writer:
    # use to_excel function and specify the sheet_name and index
    # to store the dataframe in specified sheet
    mobile_home_characteristic.to_excel(writer, sheet_name="mobile_home_characteristic", index=True)
    mobile_home_bedrooms_characteristic.to_excel(writer, sheet_name="bedrooms", index=True)
    mobile_home_bathrooms_characteristic.to_excel(writer, sheet_name="bathrooms", index=True)
    mobile_home_halfbathrooms_characteristic.to_excel(writer, sheet_name="halfbathrooms", index=True)
    mobile_home_otherrooms_characteristic.to_excel(writer, sheet_name="otherrooms", index=True)
    mobile_home_air_conditioning_characteristic.to_excel(writer, sheet_name="air_conditioning", index=True)

#%% RUN
# Sort room characteristic dataframe by weight and remove duplicate home definitions. This finds the highest weighted home chacteristic.
apartment_bedrooms_characteristic = apartment_bedrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
apartment_bathrooms_characteristic = apartment_bathrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
apartment_halfbathrooms_characteristic = apartment_halfbathrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
apartment_otherrooms_characteristic = apartment_otherrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
apartment_air_conditioning_characteristic = apartment_air_conditioning_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
attached_bedrooms_characteristic = attached_bedrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
attached_bathrooms_characteristic = attached_bathrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
attached_halfbathrooms_characteristic = attached_halfbathrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
attached_otherrooms_characteristic = attached_otherrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
attached_air_conditioning_characteristic = attached_air_conditioning_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
detached_bedrooms_characteristic = detached_bedrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
detached_bathrooms_characteristic = detached_bathrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
detached_halfbathrooms_characteristic = detached_halfbathrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
detached_otherrooms_characteristic = detached_otherrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
detached_air_conditioning_characteristic = detached_air_conditioning_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
mobile_home_bedrooms_characteristic = mobile_home_bedrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
mobile_home_bathrooms_characteristic = mobile_home_bathrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
mobile_home_halfbathrooms_characteristic = mobile_home_halfbathrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
mobile_home_otherrooms_characteristic = mobile_home_otherrooms_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])
mobile_home_air_conditioning_characteristic = mobile_home_air_conditioning_characteristic.sort_values(by='weight', ascending=False).drop_duplicates(['home_definition'])

# Drops all columns from room characteristic dataframes other then home_definition and the room (or variable)
apartment_bedrooms_characteristic = apartment_bedrooms_characteristic[['home_definition','#_of_bedrooms']]
apartment_bathrooms_characteristic = apartment_bathrooms_characteristic[['home_definition','#_of_bathrooms']]
apartment_halfbathrooms_characteristic = apartment_halfbathrooms_characteristic[['home_definition','#_of_halfbathrooms']]
apartment_otherrooms_characteristic = apartment_otherrooms_characteristic[['home_definition','#_of_otherrooms']]
apartment_air_conditioning_characteristic = apartment_air_conditioning_characteristic[['home_definition','air_conditioning']]
attached_bedrooms_characteristic = attached_bedrooms_characteristic[['home_definition','#_of_bedrooms']]
attached_bathrooms_characteristic = attached_bathrooms_characteristic[['home_definition','#_of_bathrooms']]
attached_halfbathrooms_characteristic = attached_halfbathrooms_characteristic[['home_definition','#_of_halfbathrooms']]
attached_otherrooms_characteristic = attached_otherrooms_characteristic[['home_definition','#_of_otherrooms']]
attached_air_conditioning_characteristic = attached_air_conditioning_characteristic[['home_definition','air_conditioning']]
detached_bedrooms_characteristic = detached_bedrooms_characteristic[['home_definition','#_of_bedrooms']]
detached_bathrooms_characteristic = detached_bathrooms_characteristic[['home_definition','#_of_bathrooms']]
detached_halfbathrooms_characteristic = detached_halfbathrooms_characteristic[['home_definition','#_of_halfbathrooms']]
detached_otherrooms_characteristic = detached_otherrooms_characteristic[['home_definition','#_of_otherrooms']]
detached_air_conditioning_characteristic = detached_air_conditioning_characteristic[['home_definition','air_conditioning']]
mobile_home_bedrooms_characteristic = mobile_home_bedrooms_characteristic[['home_definition','#_of_bedrooms']]
mobile_home_bathrooms_characteristic = mobile_home_bathrooms_characteristic[['home_definition','#_of_bathrooms']]
mobile_home_halfbathrooms_characteristic = mobile_home_halfbathrooms_characteristic[['home_definition','#_of_halfbathrooms']]
mobile_home_otherrooms_characteristic = mobile_home_otherrooms_characteristic[['home_definition','#_of_otherrooms']]
mobile_home_air_conditioning_characteristic = mobile_home_air_conditioning_characteristic[['home_definition','air_conditioning']]

# removes home_definition column from dataframe this will be repaced with the index (this is done due to data type problems)
#apartment_characteristic = apartment_characteristic.drop(columns=['home_definition'])
#attached_characteristic = attached_characteristic.drop(columns=['home_definition'])
#detached_characteristic = detached_characteristic.drop(columns=['home_definition'])
#mobile_home_characteristic = mobile_home_characteristic.drop(columns=['home_definition'])

# reset index and move home_definition to dataframe
apartment_characteristic.reset_index(level=0,drop=False,inplace=True)
attached_characteristic.reset_index(level=0,drop=False,inplace=True)
detached_characteristic.reset_index(level=0,drop=False,inplace=True)
mobile_home_characteristic.reset_index(level=0,drop=False,inplace=True)

# Add room (or AC) characteristic variables to home characteristic dataframes
apartment_characteristic = apartment_characteristic.merge(apartment_bedrooms_characteristic[['home_definition','#_of_bedrooms']],on='home_definition')
apartment_characteristic = apartment_characteristic.merge(apartment_bathrooms_characteristic[['home_definition','#_of_bathrooms']],on='home_definition')
apartment_characteristic = apartment_characteristic.merge(apartment_halfbathrooms_characteristic[['home_definition','#_of_halfbathrooms']],on='home_definition')
apartment_characteristic = apartment_characteristic.merge(apartment_otherrooms_characteristic[['home_definition','#_of_otherrooms']],on='home_definition')
apartment_characteristic = apartment_characteristic.merge(apartment_air_conditioning_characteristic[['home_definition','air_conditioning']],on='home_definition')
attached_characteristic = attached_characteristic.merge(attached_bedrooms_characteristic[['home_definition','#_of_bedrooms']],on='home_definition')
attached_characteristic = attached_characteristic.merge(attached_bathrooms_characteristic[['home_definition','#_of_bathrooms']],on='home_definition')
attached_characteristic = attached_characteristic.merge(attached_halfbathrooms_characteristic[['home_definition','#_of_halfbathrooms']],on='home_definition')
attached_characteristic = attached_characteristic.merge(attached_otherrooms_characteristic[['home_definition','#_of_otherrooms']],on='home_definition')
attached_characteristic = attached_characteristic.merge(attached_air_conditioning_characteristic[['home_definition','air_conditioning']],on='home_definition')
detached_characteristic = detached_characteristic.merge(detached_bedrooms_characteristic[['home_definition','#_of_bedrooms']],on='home_definition')
detached_characteristic = detached_characteristic.merge(detached_bathrooms_characteristic[['home_definition','#_of_bathrooms']],on='home_definition')
detached_characteristic = detached_characteristic.merge(detached_halfbathrooms_characteristic[['home_definition','#_of_halfbathrooms']],on='home_definition')
detached_characteristic = detached_characteristic.merge(detached_otherrooms_characteristic[['home_definition','#_of_otherrooms']],on='home_definition')
detached_characteristic = detached_characteristic.merge(detached_air_conditioning_characteristic[['home_definition','air_conditioning']],on='home_definition')
mobile_home_characteristic = mobile_home_characteristic.merge(mobile_home_bedrooms_characteristic[['home_definition','#_of_bedrooms']],on='home_definition')
mobile_home_characteristic = mobile_home_characteristic.merge(mobile_home_bathrooms_characteristic[['home_definition','#_of_bathrooms']],on='home_definition')
mobile_home_characteristic = mobile_home_characteristic.merge(mobile_home_halfbathrooms_characteristic[['home_definition','#_of_halfbathrooms']],on='home_definition')
mobile_home_characteristic = mobile_home_characteristic.merge(mobile_home_otherrooms_characteristic[['home_definition','#_of_otherrooms']],on='home_definition')
mobile_home_characteristic = mobile_home_characteristic.merge(mobile_home_air_conditioning_characteristic[['home_definition','air_conditioning']],on='home_definition')

#%% RUN to save final home characteristics file to CSV
# Save final home characteristics file to CSV
apartment_characteristic.to_csv(dataset + "_apartment_characteristics.csv", index=False)
attached_characteristic.to_csv(dataset + "_attached_characteristics.csv", index=False)
detached_characteristic.to_csv(dataset + "_detached_characteristics.csv", index=False)
mobile_home_characteristic.to_csv(dataset + "_mobile_home_characteristics.csv", index=False)

#%%
if dataset == 'recs20':
    print('apartment')
    print(apartment.groupby(['sqft','#_of_units'])['weight'].sum())
    print('attached')
    print(attached.groupby('sqft')['weight'].sum())
    print('detached')
    print(detached.groupby('sqft')['weight'].sum())
    print('mobile_home')
    print(mobile_home.groupby('sqft')['weight'].sum())

elif dataset == 'ahs21':
    print('apartment')
    print(apartment.groupby(['sqft','#_of_units'])['weight'].sum())
    print('attached')
    print(attached.groupby('sqft')['weight'].sum())
    print('detached')
    print(detached.groupby('sqft')['weight'].sum())
    print('mobile_home')
    print(mobile_home.groupby('sqft')['weight'].sum())

#'1' = Less than 500 square feet
#'2' = 500 to 749 square feet
#'3' = 750 to 999 square feet
#'4' = 1,000 to 1,499 square feet
#'5' = 1,500 to 1,999 square feet
#'6' = 2,000 to 2,499 square feet
#'7' = 2,500 to 2,999 square feet
#'8' = 3,000 to 3,999 square feet
#'9' = 4,000 square feet or more

#%% DO NOT RUN Left over code
# Not valid since both sqft and home age variables do match the past study.
# import 1997 definitions
home_definitions_1997 = pd.read_csv('1997_home_definitions.csv',dtype=np.object_)

test = [e for e in apartment['home_definition'].unique() if e not in list(home_definitions_1997['apartment'].unique())]