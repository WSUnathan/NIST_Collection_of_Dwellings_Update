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
    df.rename(columns = {'NWEIGHT':'weight', 'BEDROOMS':'#_of_bedrooms', 'NCOMBATH':'#_of_bathrooms', 'NHAFBATH':'#_of_halfbathrooms', 'OTHROOMS':'#_of_otherrooms', 'WINDOWS':'#_of_windows', 'SQFTRANGE':'sqft', 'TOTSQFT_EN':'conditioned_sqft'}, inplace = True)
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
    df.loc[df['STORIES'] == 4, "#_of_floors"] = "4"
    df.loc[df['STORIES'] == 5, "#_of_floors"] = "2"
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
    df.loc[df['STORIES'] == 1, "#_of_floors"] = "1"
    df.loc[df['STORIES'] == 2, "#_of_floors"] = "2"
    df.loc[df['STORIES'] >= 3, "#_of_floors"] = "3"
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

# Drop unused variable, make household dataframes, and build home definition
print('drop unused variable')
df = df[['TypeofHousehold','#_of_floors','#_of_units','floor_area','year_built','foundation','garage','forced-air','weight','#_of_bedrooms','#_of_bathrooms','#_of_halfbathrooms','#_of_otherrooms','#_of_windows','air_conditioning','sqft','conditioned_sqft']]

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

#%%
def w_avg(df, values, weights):
    d = df[values]
    w = df[weights]
    return (d * w).sum() / w.sum()

#%%
ap1 = apartment[(apartment['conditioned_sqft']<1000) & (apartment['#_of_units']=="1")]
ap2 = apartment[(apartment['conditioned_sqft']>=1000) & (apartment['#_of_units']=="1")]
ap3 = apartment[(apartment['conditioned_sqft']<1000) & (apartment['#_of_units']>="2")]
ap4 = apartment[(apartment['conditioned_sqft']>=1000) & (apartment['#_of_units']>="2")]
at1 = attached[(attached['conditioned_sqft']<1600)]
at2 = attached[(attached['conditioned_sqft']>=1600) & (attached['conditioned_sqft']<=2399)]
at3 = attached[(attached['conditioned_sqft']>=2400)]
de1 = detached[(detached['conditioned_sqft']<1600)]
de2 = detached[(detached['conditioned_sqft']>=1600) & (detached['conditioned_sqft']<=2399)]
de3 = detached[(detached['conditioned_sqft']>=2400)]
mh1 = mobile_home[(mobile_home['conditioned_sqft']<1600)]
mh2 = mobile_home[(mobile_home['conditioned_sqft']>=1600)]

#%%
print('apartment_2-4_<1000')
print(w_avg(ap1,'conditioned_sqft','weight'))

print('apartment_2-4_>1000')
print(w_avg(ap2,'conditioned_sqft','weight'))

print('apartment_5+_<1000')
print(w_avg(ap3,'conditioned_sqft','weight'))

print('apartment_5+_>1000')
print(w_avg(ap4,'conditioned_sqft','weight'))

print('attached_<1600')
print(w_avg(at1,'conditioned_sqft','weight'))

print('attached_1600-2399')
print(w_avg(at2,'conditioned_sqft','weight'))

print('attached_>=2400')
print(w_avg(at3,'conditioned_sqft','weight'))

print('detached_<1600')
print(w_avg(de1,'conditioned_sqft','weight'))

print('detached_1600-2399')
print(w_avg(de2,'conditioned_sqft','weight'))

print('detached_>=2400')
print(w_avg(de3,'conditioned_sqft','weight'))

print('mobile_<1600')
print(w_avg(mh1,'conditioned_sqft','weight'))

print('mobile_>=1600')
print(w_avg(mh2,'conditioned_sqft','weight'))
# %%
