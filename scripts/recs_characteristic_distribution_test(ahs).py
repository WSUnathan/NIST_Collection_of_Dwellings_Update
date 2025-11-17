# -*- coding: utf-8 -*-
#%% import needed modules and define directory path
print('Importing needed modules and define directory path.')
import os
import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models.tools import HoverTool, CrosshairTool, Span
from bokeh.layouts import gridplot
from bokeh.models import CrosshairTool, Span

absolute_path = 'C:/Users/nml/OneDrive - NIST/Documents/NIST/suit_of_homes_research/'
os.chdir(absolute_path)

#%% Select dataset
# use only one dataset at a time
dataset = 'ahs21' #select 'recs15', 'recs20' , 'ahs19' , 'ahs21'

#%% Set up Datasets that are used
print(dataset + ' dataset selected and final file path defined')

if dataset == 'recs15':
    df = pd.read_csv("./recs_data/2015/recs2015_public_v4.csv")
    df.rename(columns = {'NWEIGHT':'weight', 'BEDROOMS':'#_of_bedrooms', 'NCOMBATH':'#_of_bathrooms', 'NHAFBATH':'#_of_halfbathrooms', 'OTHROOMS':'#_of_otherrooms', 'WINDOWS':'#_of_windows'}, inplace = True)
elif dataset == 'recs20':
    df = pd.read_csv("./recs_data/2020/recs2020_public_v1_data.csv")
    df.rename(columns = {'NWEIGHT':'weight', 'BEDROOMS':'#_of_bedrooms', 'NCOMBATH':'#_of_bathrooms', 'NHAFBATH':'#_of_halfbathrooms', 'OTHROOMS':'#_of_otherrooms', 'WINDOWS':'#_of_windows'}, inplace = True)
elif dataset == 'ahs19':
    df = pd.read_csv("./ahs_data/2019/household.csv")
    df.replace('\'','',regex=True,inplace=True)
    df.drop(df.index[df['BLD']=='10'],inplace=True) #remove boat_rv_etc
    df.drop(df.index[df['UNITSIZE']=='-9'],inplace=True) #remove all units without a sqft size 
    df=df.copy()
    df.rename(columns = {'BEDROOMS':'#_of_bedrooms', 'WEIGHT':'weight'}, inplace = True)
elif dataset == 'ahs21':
    df = pd.read_csv("./ahs_data/2021/household.csv")
    df.replace('\'','',regex=True,inplace=True)
    df.drop(df.index[df['BLD']=='10'],inplace=True) #remove boat_rv_etc
    df.drop(df.index[df['UNITSIZE']=='-9'],inplace=True) #remove all units without a sqft size 
    df=df.copy()
    df.rename(columns = {'BEDROOMS':'#_of_bedrooms', 'WEIGHT':'weight'}, inplace = True)

#Replace columns data with common values'
print('Replace columns data with common values')
if dataset == 'recs15':
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
    df.loc[df['EQUIPM'] == 6,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 7,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 8,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 10,'forced-air'] = "1"
    df.loc[df['EQUIPM'] == 21,'forced-air'] = "1"
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
    # garage
    # change valued to match past study
    # (1)No & (2)Yes
    df.loc[df['SIZEOFGARAGE'] == 1, "garage"] = "2"
    df.loc[df['SIZEOFGARAGE'] == 2, "garage"] = "2"
    df.loc[df['SIZEOFGARAGE'] == 3, "garage"] = "2"
    df.loc[df['SIZEOFGARAGE'] == -2, "garage"] = "1"
    # number of floors
    # true values
    df.loc[df['STORIES'] == 10, "#_of_floors"] = "1"
    df.loc[df['STORIES'] == 20, "#_of_floors"] = "2"
    df.loc[df['STORIES'] == 31, "#_of_floors"] = "3"
    df.loc[df['STORIES'] == 32, "#_of_floors"] = "4"
    df.loc[df['STORIES'] == 40, "#_of_floors"] = "2"
    df.loc[df['STORIES'] == -2, "#_of_floors"] = "n/a"
    # foundation
    # (1)concrete slab, (2)crawl space, (3)Basement, (4)n/a
    print('1. Lacks full list of foundation types (only includes basements)')
    df.loc[(df['CELLAR'] == 0), "foundation"] = "3"
    df.loc[(df['CELLAR'] == 1), "foundation"] = "4"
    df.loc[(df['CELLAR'] == -2), "foundation"] = "4"
    # air conditioning set up
    # (1)Central system, (2)Individual units, (3)Both, (4)None
    df.loc[df['COOLTYPE'] == 1, "air_conditioning"] = "1" # Central system
    df.loc[df['COOLTYPE'] == 3, "air_conditioning"] = "2" # Individual units
    df.loc[df['COOLTYPE'] == 4, "air_conditioning"] = "3" # Both
    df.loc[df['COOLTYPE'] == -2, "air_conditioning"] = "4" # None
    # floor area
        # mobile_home floor_area
    # (1)less than 1500sq/sf (2)greater than 1500sq/ft
    df.loc[(df["TOTSQFT_EN"] <= 1490) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #Less than 1,490 square feet
    df.loc[(df["TOTSQFT_EN"] >= 1500) & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #1,500 square feet or more
    # attached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["TOTSQFT_EN"] <= 1490) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #Less than 1,490 square feet
    df.loc[(df["TOTSQFT_EN"] >= 1500) & (df["TOTSQFT_EN"] <= 2490) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #1,500 to 2,490 square feet
    df.loc[(df["TOTSQFT_EN"] >= 2500) & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #2,500 square feet or more
    # detached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["TOTSQFT_EN"] <= 1490) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #Less than 1,490 square feet
    df.loc[(df["TOTSQFT_EN"] >= 1500) & (df["TOTSQFT_EN"] <= 2490) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #1,500 to 2,490 square feet
    df.loc[(df["TOTSQFT_EN"] >= 2500) & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #2,500 square feet or more
    # apartment floor_area
    # (1)less than 1000sq/sf (2)greater than 1000sq/ft
    df.loc[(df["TOTSQFT_EN"] <= 990) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #Less than 990 square feet
    df.loc[(df["TOTSQFT_EN"] >= 1000) & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #1,000 square feet or more
    # number of units
    df['#_of_units'] = ''
    print('2. number of units is not a variable in the REC database')

elif dataset == 'recs20':
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
    df.loc[df['ACEQUIPM_pub'] == 1, "air_conditioning"] = "1" # Central system
    df.loc[df['ACEQUIPM_pub'] == 3, "air_conditioning"] = "2" # Individual units
    df.loc[df['ACEQUIPM_pub'] == 4, "air_conditioning"] = "2" # Individual units
    df.loc[df['ACEQUIPM_pub'] == 5, "air_conditioning"] = "2" # Individual units
    df.loc[df['ACEQUIPM_pub'] == 6, "air_conditioning"] = "2" # Individual units
    df.loc[df['ACEQUIPM_pub'] == -2, "air_conditioning"] = "4" # None
    # floor area
    df['floor_area'] = ''
    print('floor area is not currently in the REC database')
    # number of units
    df['#_of_units'] = ''
    print('number of units is not a variable in the REC database')

elif dataset == 'ahs19':
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
    df.loc[df["YRBUILT"] >= 2000, "year_built"] = "6" #2000 = 2000 to 2009 The > catches all values higher up to 2019
    # mobile_home floor_area
    # (1)less than 1500sq/sf (2)greater than 1500sq/ft
    df.loc[(df["UNITSIZE"] == '1') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["UNITSIZE"] == '2') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["UNITSIZE"] == '3') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["UNITSIZE"] == '4') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["UNITSIZE"] == '5') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["UNITSIZE"] == '6') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["UNITSIZE"] == '7') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["UNITSIZE"] == '8') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["UNITSIZE"] == '9') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'9' = 4,000 square feet or more
    df.loc[(df["UNITSIZE"] == '-9') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "n/a" #'-9' = Not reported
    # attached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["UNITSIZE"] == '1') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["UNITSIZE"] == '2') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["UNITSIZE"] == '3') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["UNITSIZE"] == '4') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["UNITSIZE"] == '5') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["UNITSIZE"] == '6') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["UNITSIZE"] == '7') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["UNITSIZE"] == '8') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["UNITSIZE"] == '9') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'9' = 4,000 square feet or more
    df.loc[(df["UNITSIZE"] == '-9') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "n/a" #'-9' = Not reported
    # detached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["UNITSIZE"] == '1') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["UNITSIZE"] == '2') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["UNITSIZE"] == '3') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["UNITSIZE"] == '4') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["UNITSIZE"] == '5') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["UNITSIZE"] == '6') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["UNITSIZE"] == '7') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["UNITSIZE"] == '8') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["UNITSIZE"] == '9') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'9' = 4,000 square feet or more
    df.loc[(df["UNITSIZE"] == '-9') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "n/a" #'-9' = Not reported
    # apartment floor_area
    # (1)less than 1000sq/sf (2)greater than 1000sq/ft
    df.loc[(df["UNITSIZE"] == '1') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["UNITSIZE"] == '2') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["UNITSIZE"] == '3') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["UNITSIZE"] == '4') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["UNITSIZE"] == '5') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["UNITSIZE"] == '6') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["UNITSIZE"] == '7') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["UNITSIZE"] == '8') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["UNITSIZE"] == '9') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'9' = 4,000 square feet or more
    df.loc[(df["UNITSIZE"] == '-9') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "n/a" #'-9' = Not reported
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
    df.loc[(df["UNITSIZE"] == '1') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["UNITSIZE"] == '2') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["UNITSIZE"] == '3') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["UNITSIZE"] == '4') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["UNITSIZE"] == '5') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["UNITSIZE"] == '6') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["UNITSIZE"] == '7') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["UNITSIZE"] == '8') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["UNITSIZE"] == '9') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "2" #'9' = 4,000 square feet or more
    df.loc[(df["UNITSIZE"] == '-9') & (df["TypeofHousehold"] == "mobile_home"), "floor_area"] = "n/a" #'-9' = Not reported
    # attached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["UNITSIZE"] == '1') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["UNITSIZE"] == '2') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["UNITSIZE"] == '3') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["UNITSIZE"] == '4') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["UNITSIZE"] == '5') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["UNITSIZE"] == '6') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["UNITSIZE"] == '7') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["UNITSIZE"] == '8') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["UNITSIZE"] == '9') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "3" #'9' = 4,000 square feet or more
    df.loc[(df["UNITSIZE"] == '-9') & (df["TypeofHousehold"] == "attached"), "floor_area"] = "n/a" #'-9' = Not reported
    # detached single family floor_area
    # (1)less than 1500sq/sf (2)1500-2500sq/ft (3)greater than 2500sq/ft
    df.loc[(df["UNITSIZE"] == '1') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["UNITSIZE"] == '2') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["UNITSIZE"] == '3') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["UNITSIZE"] == '4') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "1" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["UNITSIZE"] == '5') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["UNITSIZE"] == '6') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["UNITSIZE"] == '7') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["UNITSIZE"] == '8') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["UNITSIZE"] == '9') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "3" #'9' = 4,000 square feet or more
    df.loc[(df["UNITSIZE"] == '-9') & (df["TypeofHousehold"] == "detached"), "floor_area"] = "n/a" #'-9' = Not reported
    # apartment floor_area
    # (1)less than 1000sq/sf (2)greater than 1000sq/ft
    df.loc[(df["UNITSIZE"] == '1') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'1' = Less than 500 square feet
    df.loc[(df["UNITSIZE"] == '2') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'2' = 500 to 749 square feet
    df.loc[(df["UNITSIZE"] == '3') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "1" #'3' = 750 to 999 square feet
    df.loc[(df["UNITSIZE"] == '4') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'4' = 1,000 to 1,499 square feet
    df.loc[(df["UNITSIZE"] == '5') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'5' = 1,500 to 1,999 square feet
    df.loc[(df["UNITSIZE"] == '6') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'6' = 2,000 to 2,499 square feet
    df.loc[(df["UNITSIZE"] == '7') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'7' = 2,500 to 2,999 square feet
    df.loc[(df["UNITSIZE"] == '8') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'8' = 3,000 to 3,999 square feet
    df.loc[(df["UNITSIZE"] == '9') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "2" #'9' = 4,000 square feet or more
    df.loc[(df["UNITSIZE"] == '-9') & (df["TypeofHousehold"] == "apartment"), "floor_area"] = "n/a" #'-9' = Not reported
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
df = df[['TypeofHousehold','#_of_floors','#_of_units','floor_area','year_built','foundation','garage','forced-air','weight','#_of_bedrooms','#_of_bathrooms','#_of_halfbathrooms','#_of_otherrooms','#_of_windows','air_conditioning']]

print('make four household type dataframes')
apartment = df.loc[df['TypeofHousehold'] == 'apartment', df.columns.drop(['foundation', 'garage'])]
attached = df.loc[df['TypeofHousehold'] == 'attached', df.columns.drop(['#_of_units'])]
detached = df.loc[df['TypeofHousehold'] == 'detached', df.columns.drop(['#_of_units'])]
mobile_home = df.loc[df['TypeofHousehold'] == 'mobile_home', df.columns.drop(['#_of_floors','#_of_units','foundation', 'garage'])]

print('make home definition variable')
apartment['home_definition'] = apartment['#_of_floors']+apartment['#_of_units']+apartment['floor_area']+apartment['year_built']
attached['home_definition'] = attached['#_of_floors']+attached['floor_area']+attached['year_built']+attached['foundation']+attached['garage']
detached['home_definition'] = detached['#_of_floors']+detached['floor_area']+detached['year_built']+detached['foundation']+detached['garage']
mobile_home['home_definition'] = mobile_home['floor_area']+mobile_home['year_built']

#%%
# Print # of unique homes 
print('# of unique apartments: ')
print(apartment['home_definition'].nunique())
print('# of unique attached homes:')
print(attached['home_definition'].nunique())
print('# of unique detached homes:')
print(detached['home_definition'].nunique())
print('# of unique mobile homes:')
print(mobile_home['home_definition'].nunique())
#%%
# make individual columns for home characteristics 
print('making individual columns for home characteristics')
# apartment
# number of bedrooms
apartment.loc[apartment['#_of_bedrooms']==0, '0_#_of_bedrooms']='1'
apartment.loc[apartment['#_of_bedrooms']==1, '1_#_of_bedrooms']='1'
apartment.loc[apartment['#_of_bedrooms']==2, '2_#_of_bedrooms']='1'
apartment.loc[apartment['#_of_bedrooms']==3, '3_#_of_bedrooms']='1'
apartment.loc[apartment['#_of_bedrooms']==4, '4_#_of_bedrooms']='1'
apartment.loc[apartment['#_of_bedrooms']==5, '5_#_of_bedrooms']='1'
# number of baths
apartment.loc[apartment['#_of_bathrooms']=='0', '0_#_of_bathrooms']='1'
apartment.loc[apartment['#_of_bathrooms']=='1', '1_#_of_bathrooms']='1'
apartment.loc[apartment['#_of_bathrooms']=='2', '2_#_of_bathrooms']='1'
apartment.loc[apartment['#_of_bathrooms']=='3', '3_#_of_bathrooms']='1'
apartment.loc[apartment['#_of_bathrooms']=='4', '4_#_of_bathrooms']='1'
# number of halfbaths
apartment.loc[apartment['#_of_halfbathrooms']=='0', '0_#_of_halfbathrooms']='1'
apartment.loc[apartment['#_of_halfbathrooms']=='1', '1_#_of_halfbathrooms']='1'
# air conditioning 
apartment.loc[apartment['air_conditioning']=='1', 'central_ac']='1'
apartment.loc[apartment['air_conditioning']=='2', 'individual_ac']='1'
apartment.loc[apartment['air_conditioning']=='4', 'no_ac']='1'

# attached
# number of bedrooms
attached.loc[attached['#_of_bedrooms']==0, '0_#_of_bedrooms']='1'
attached.loc[attached['#_of_bedrooms']==1, '1_#_of_bedrooms']='1'
attached.loc[attached['#_of_bedrooms']==2, '2_#_of_bedrooms']='1'
attached.loc[attached['#_of_bedrooms']==3, '3_#_of_bedrooms']='1'
attached.loc[attached['#_of_bedrooms']==4, '4_#_of_bedrooms']='1'
attached.loc[attached['#_of_bedrooms']==5, '5_#_of_bedrooms']='1'
# number of baths
attached.loc[attached['#_of_bathrooms']=='0', '0_#_of_bathrooms']='1'
attached.loc[attached['#_of_bathrooms']=='1', '1_#_of_bathrooms']='1'
attached.loc[attached['#_of_bathrooms']=='2', '2_#_of_bathrooms']='1'
attached.loc[attached['#_of_bathrooms']=='3', '3_#_of_bathrooms']='1'
attached.loc[attached['#_of_bathrooms']=='4', '4_#_of_bathrooms']='1'
# number of halfbaths
attached.loc[attached['#_of_halfbathrooms']=='0', '0_#_of_halfbathrooms']='1'
attached.loc[attached['#_of_halfbathrooms']=='1', '1_#_of_halfbathrooms']='1'
# air conditioning 
attached.loc[attached['air_conditioning']=='1', 'central_ac']='1'
attached.loc[attached['air_conditioning']=='2', 'individual_ac']='1'
attached.loc[attached['air_conditioning']=='4', 'no_ac']='1'

#detached
# number of bedrooms
detached.loc[detached['#_of_bedrooms']==0, '0_#_of_bedrooms']='1'
detached.loc[detached['#_of_bedrooms']==1, '1_#_of_bedrooms']='1'
detached.loc[detached['#_of_bedrooms']==2, '2_#_of_bedrooms']='1'
detached.loc[detached['#_of_bedrooms']==3, '3_#_of_bedrooms']='1'
detached.loc[detached['#_of_bedrooms']==4, '4_#_of_bedrooms']='1'
detached.loc[detached['#_of_bedrooms']==5, '5_#_of_bedrooms']='1'
# number of baths
detached.loc[detached['#_of_bathrooms']=='0', '0_#_of_bathrooms']='1'
detached.loc[detached['#_of_bathrooms']=='1', '1_#_of_bathrooms']='1'
detached.loc[detached['#_of_bathrooms']=='2', '2_#_of_bathrooms']='1'
detached.loc[detached['#_of_bathrooms']=='3', '3_#_of_bathrooms']='1'
detached.loc[detached['#_of_bathrooms']=='4', '4_#_of_bathrooms']='1'
# number of halfbaths
detached.loc[detached['#_of_halfbathrooms']=='0', '0_#_of_halfbathrooms']='1'
detached.loc[detached['#_of_halfbathrooms']=='1', '1_#_of_halfbathrooms']='1'
# air conditioning 
detached.loc[detached['air_conditioning']=='1', 'central_ac']='1'
detached.loc[detached['air_conditioning']=='2', 'individual_ac']='1'
detached.loc[detached['air_conditioning']=='4', 'no_ac']='1'

# mobile_home
# number of bedrooms
mobile_home.loc[mobile_home['#_of_bedrooms']==0, '0_#_of_bedrooms']='1'
mobile_home.loc[mobile_home['#_of_bedrooms']==1, '1_#_of_bedrooms']='1'
mobile_home.loc[mobile_home['#_of_bedrooms']==2, '2_#_of_bedrooms']='1'
mobile_home.loc[mobile_home['#_of_bedrooms']==3, '3_#_of_bedrooms']='1'
mobile_home.loc[mobile_home['#_of_bedrooms']==4, '4_#_of_bedrooms']='1'
mobile_home.loc[mobile_home['#_of_bedrooms']==5, '5_#_of_bedrooms']='1'
# number of baths
mobile_home.loc[mobile_home['#_of_bathrooms']=='0', '0_#_of_bathrooms']='1'
mobile_home.loc[mobile_home['#_of_bathrooms']=='1', '1_#_of_bathrooms']='1'
mobile_home.loc[mobile_home['#_of_bathrooms']=='2', '2_#_of_bathrooms']='1'
mobile_home.loc[mobile_home['#_of_bathrooms']=='3', '3_#_of_bathrooms']='1'
mobile_home.loc[mobile_home['#_of_bathrooms']=='4', '4_#_of_bathrooms']='1'
# number of halfbaths
mobile_home.loc[mobile_home['#_of_halfbathrooms']=='0', '0_#_of_halfbathrooms']='1'
mobile_home.loc[mobile_home['#_of_halfbathrooms']=='1', '1_#_of_halfbathrooms']='1'
# air conditioning 
mobile_home.loc[mobile_home['air_conditioning']=='1', 'central_ac']='1'
mobile_home.loc[mobile_home['air_conditioning']=='2', 'individual_ac']='1'
mobile_home.loc[mobile_home['air_conditioning']=='4', 'no_ac']='1'

# Make home characteristic datasets
print('Making home characteristic datasets')
apartment_characteristic = apartment.groupby(['home_definition']).agg({'#_of_floors':['min'],'#_of_units':['min'],'floor_area': ['min'],
    'year_built':['min'], 'forced-air':['min'],'home_definition':['count'],'weight':['sum'],'0_#_of_bedrooms': ['count'],
    '1_#_of_bedrooms': ['count'],'2_#_of_bedrooms': ['count'],'3_#_of_bedrooms': ['count'],'4_#_of_bedrooms': ['count'],
    '5_#_of_bedrooms': ['count'],'0_#_of_bathrooms': ['count'],'1_#_of_bathrooms': ['count'],'2_#_of_bathrooms': ['count'],
    '3_#_of_bathrooms': ['count'],'4_#_of_bathrooms': ['count'],'0_#_of_halfbathrooms': ['count'],'1_#_of_halfbathrooms': ['count'],
    'central_ac': ['count'],'individual_ac': ['count'],'no_ac': ['count']})

attached_characteristic = attached.groupby(['home_definition']).agg({'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'home_definition':['count'],'weight':['sum'],
    '0_#_of_bedrooms': ['count'],'1_#_of_bedrooms': ['count'],'2_#_of_bedrooms': ['count'],'3_#_of_bedrooms': ['count'],
    '4_#_of_bedrooms': ['count'],'5_#_of_bedrooms': ['count'],'0_#_of_bathrooms': ['count'],'1_#_of_bathrooms': ['count'],
    '2_#_of_bathrooms': ['count'],'3_#_of_bathrooms': ['count'],'4_#_of_bathrooms': ['count'],'0_#_of_halfbathrooms': ['count'],
    '1_#_of_halfbathrooms': ['count'],'central_ac': ['count'],'individual_ac': ['count'],'no_ac': ['count']})

detached_characteristic = detached.groupby(['home_definition']).agg({'#_of_floors':['min'],'floor_area': ['min'],
    'year_built':['min'], 'foundation': ['min'],'garage':['min'],'forced-air':['min'],'home_definition':['count'],'weight':['sum'],
    '0_#_of_bedrooms': ['count'],'1_#_of_bedrooms': ['count'],'2_#_of_bedrooms': ['count'],'3_#_of_bedrooms': ['count'],
    '4_#_of_bedrooms': ['count'],'5_#_of_bedrooms': ['count'],'0_#_of_bathrooms': ['count'],'1_#_of_bathrooms': ['count'],
    '2_#_of_bathrooms': ['count'],'3_#_of_bathrooms': ['count'],'4_#_of_bathrooms': ['count'],'0_#_of_halfbathrooms': ['count'],
    '1_#_of_halfbathrooms': ['count'],'central_ac': ['count'],'individual_ac': ['count'],'no_ac': ['count']})

mobile_home_characteristic = mobile_home.groupby(['home_definition']).agg({'floor_area': ['min'],'year_built':['min'],
    'forced-air':['min'],'home_definition':['count'],'weight':['sum'],'0_#_of_bedrooms': ['count'], '1_#_of_bedrooms': ['count'],
    '2_#_of_bedrooms': ['count'],'3_#_of_bedrooms': ['count'],'4_#_of_bedrooms': ['count'],'5_#_of_bedrooms': ['count'],
    '0_#_of_bathrooms': ['count'],'1_#_of_bathrooms': ['count'],'2_#_of_bathrooms': ['count'],'3_#_of_bathrooms': ['count'],
    '4_#_of_bathrooms': ['count'],'0_#_of_halfbathrooms': ['count'],'1_#_of_halfbathrooms': ['count'],'central_ac': ['count'],
    'individual_ac': ['count'],'no_ac': ['count']})

# Drop second part of muilti level index 
apartment_characteristic.columns = apartment_characteristic.columns.droplevel(1)
attached_characteristic.columns = attached_characteristic.columns.droplevel(1)
detached_characteristic.columns = detached_characteristic.columns.droplevel(1)
mobile_home_characteristic.columns = mobile_home_characteristic.columns.droplevel(1)
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
#%%
# Plot Percentage coverage as a function of dataset sample size
output_file("AHSRemoved_Percentage_coverage_" + dataset + ".html")

p = figure()

p.line(apartment_characteristic['count'], apartment_characteristic['running_%'], legend_label="apartment", line_color="red")
p.line(attached_characteristic['count'], attached_characteristic['running_%'], legend_label="attached_home", line_color="green")
p.line(detached_characteristic['count'], detached_characteristic['running_%'], legend_label="detached_home", line_color="blue")
p.line(mobile_home_characteristic['count'], mobile_home_characteristic['running_%'], legend_label="mobile_home", line_color="orange")

p.title.text = "Percentage coverage as a function of " + dataset + " sample size"
p.title.text_font_size = '12pt'
p.title.align = 'center'

p.xaxis.axis_label = "Sample Size (#)"

p.yaxis.axis_label = "Percent of Building Stock Represented (%)"

p.legend.location = "bottom_right"

width = Span(dimension="width", line_width=1)
height = Span(dimension="height", line_width=1)

p.add_tools(HoverTool(tooltips=[("(#,%)","($x{0.0},$y{0.0})")]))
p.add_tools(CrosshairTool(overlay=[width, height]))

show(p)


#%% 
# save to CSV
#apartment_characteristic.to_csv('apartmeant_characteristic.csv')
#attached_characteristic.to_csv('attached_characteristic.csv')
#detached_characteristic.to_csv('detached_characteristic.csv')
#mobile_home_characteristic.to_csv('mobile_home_characteristic.csv')

#%%
# import 1997 definitions
home_definitions_1997 = pd.read_csv('1997_home_definitions.csv',dtype=np.object_)

#%%
test = [e for e in apartment['home_definition'].unique() if e not in list(home_definitions_1997['apartment'].unique())]

#%%
#random code
#df['new'] = df['id'].isin(df['authorid'])
#df['new'] = df['id'].astype(str).isin(df['authorid'].astype(str))

#print(df['BATHROOMS'].value_counts()['06'])
#df['#_of_bathrooms'] = df['#_of_bathrooms'].astype(str).astype(int)
#print(df['#_of_floor']+df['#_of_units']+df['floor_area']+df['year_built']+df['foundation']+df['garage']+df['forced-air'])

#mobile_home_unique = mobile_home['home_definition'].unique()
#test = []
#for i in mobile_home_unique:
#    test.append(
#        {
#            'floor_area':mobile_home
#            'number_in_survey':len(mobile_home[mobile_home['home_definition']==i])
#        }
#    )
#d.DataFrame(test)