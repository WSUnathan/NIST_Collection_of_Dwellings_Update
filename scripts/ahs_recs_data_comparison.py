# -*- coding: utf-8 -*-
#%% import needed modules 
import os
import numpy as np
import pandas as pd

#%% set path, directory, and load datasets
absolute_path = 'C:/Users/nml/OneDrive - NIST/Documents/NIST/suit_of_homes_research/'
os.chdir(absolute_path)

recs_1997 = pd.read_csv("./recs_data/1997/1997_recs_data.csv")
recs_2020 = pd.read_csv("./recs_data/2020/recs2020_public_v2.csv")

ahs_1997 = pd.read_csv("./ahs_data/1997/household.csv")
ahs_2021 = pd.read_csv("./ahs_data/2021/household.csv")

#%% Column heading, Table 1, & Table 2 notes
""" recs 1997
(Note(s): All values must be adjusted by there NWEIGHT 'The Final Weight' value for each of the DOEID '4-digit identification number' households.)
    Unit type
        TYPEHUQ 'Type of Home: as report by Respondent'
            1 = Mobile Home
            2 = Single-Family Detached
            3 = Single-Family Attached
            4 = Apartment in Building containing 2-4 units
            5 = Apartment in Building Containing 5 or more units
            (Table 1 Note:
                Apartment = 4,5)
    Region
        REGIONC 'Census Region'
            1 = Northeast
            2 = Midwest
            3 = South
            4 = West
    Forced-air distribution
        EQUIPM 'Main Home Heating Equipment'
            2  = Steam
            3  = Central Warm-Air Furnace With Ducts
            4  = Heat Pump
            5  = Built-In Electric Units In The Walls, etc. 
            6  = Built-In Floor
            7  = Room Heater Burning Gas, Oil, Or Kerosene
            8  = Heating Stove
            9  = Fireplace
            10 = Portable Electric Heaters 
            11 = Portable Kerosene Heaters
            12 = Cooking Stove (Used to Heat Home)
            21 = Equipment Not Listed
            99 = Not Applicable
            (Table 1 Note(s):
                Yes = 3
                No = 2,4,5,6,7,8,9,10,11,12,21,99) 
            (General Note: Verify which variable was used in study
                The above assumption works better the ACDUCTS below)
        ACDUCTS 'Home Has Ducts'
            0 = No
            1 = Yes
            9 = Not Applicable
            (General Note: Verify which variable was used in study
                This variable is not in the 2020 data)
            (Table 2 Note(s):
                This variable name changes for each of the different home types, What was used for the models?)
    Floor area
        SQFTEST  'Respondent Estimate of Total Heated Floorspace'
            1 =Fewer Than 600 Square Feet
            2 = 600 To 999 Square Feet
            3 = 1,000 To 1,599 Square Feet
            4 = 1,600 To 1,999 Square Feet
            5 = 2,000 To 2,399 Square Feet
            6 = 2,400 To 2,999 Square Feet
            7 = 3,000 or More Square Feet
            96 = Don't Know
            97 = Refused
            98 = No Answer
            (Table 1 Note(s):
                < 93 m2 (1000 ft2) = 1,2
                93 m2 to186 m2 (1000 ft2 to 1999 ft2) = 3,4
                186 m2 to 279 m2 (2000 ft2 to 2999 ft2) = 5,6
                > 279 m2 (3000 ft2) = 7)
            (Table 2 Note(s): For Single family (attached and detached)
                < 149 (1600) = 1,2,3
                149 to 223 (1600 to 2399) = 4,5
                > 223 (2400) = 6,7
                For Apartments
                < 93 (1000) = 1,2
                > 93 (1000) = 3,4,5,6,7
                For Manufacutured homes
                < 149 (1600) = 1,2,3
                > 149 (1600) = 4,5,6,7)
    Occupants per household
        NHSLDMEM 'Number Of Household Members'
            (true values)
            1 = 1
            2 = 2
            3 = 3
            4 = 4
            5 = 5
            6 = 6
            7 = 7
            8 = 8
            (Table 1 Note(s):
                1 = 1
                2 = 2
                3-4 = 3,4
                ≥5 = 5,6,7,8)
    Central air conditioning
        COOLTYPE 'Type Of Air-Conditioning Equipment'
            1 = Central System
            2 = Individual Units
            3 = Both Central And Units
            9 = Not Applicable
            (Table 1 Note(s):
                Yes = 1,3
                No = 2,4
                Verify if option 3 was included as Yes for study)
            (Table 2 Note(s):
                This variable name changes for each of the different home types, What was used for the models?)
    Year built
        YEARMADE 'Year Home Built' 
            1 = Before 1940
            2 = 1940-49
            3 = 1950-59
            4 = 1960-69
            5 = 1970-76
            6 = 1977-79
            7 = 1980-86
            8 = 1987-89
            9 = 1990
            10 = 1991
            11 = 1992
            12 = 1993
            13 = 1994
            14 = 1995
            15 = 1996
            16 = 1997
            (Table 1 note(s):
                <1940 = 1
                1940-1949 = 2
                1950-1959 = 3
                1960-1969 = 4
                1970-1979 = 5,6
                1980-1989 = 7,8
                >1990 = 9,10,11,12,13,14,15,16)
            (Table 2 Note(s):
                <1940 = 1
                1940-1969 = 2,3,4
                1970-1989 = 5,6,7,8
                1990-1997 = 9,10,11,12,13,14,15,16) 
    Garage or carport
        PRKGPLCE 'Home has Garage or Carport' 
            0 = No
            1 = Yes
            9 = Not Applicable
    Foundations type
        CELLAR  'Home Has Basement' 
            0 = No
            1 = Yes
            9 = Not Applicable
            (Table 1 Note(s):
                Basement = 1)
        CRAWL  'Home Has Crawl Space'
            0 = No
            1 = Yes
            9 = Not Applicable
            (Table 1 Note(s):
                Crawl space = 1)
        CONCRETE 'Home Has Concrete Slab'
            0 = No
            1 = Yes
            9 = Not Applicable
            (Table 1 Note(s):
                Slab = 1)
    Number of stories
        STORIES  'Reported Stories in Housing Unit'
            1 = One-Story
            2 = Two-Stories
            3 = Three or More Stories
            4 = Split-Level
            5 = Some Other Type
            9 = Not Applicable
            (Table 1 Note(s):
                1 = 1
                2 = 2
                ≥3 = 3
                How was split-level classed?)
    # of units in building
        UNITS 'Interviewer Rprted Num of Units in Apt Building'
            (true values)
            5-435 = 5-435
            995 = 995 Units or More
            998 = No Answer
            999 = Not Applicable
            (Table 2 Note(s):
                2-4 = 2-4
                5-9 = 5-9
                10-19 = 10-19
                20-39 = 20-39
                >40 = 40-435)       
"""
""" recs 2020
(Note(s): All values must be adjusted by there NWEIGHT 'Final Analysis Weight' value for each of the DOEID 'Unique identifier for each respondent' households.)
    Unit type
        TYPEHUQ 'Type of Home: as report by Respondent'
            1 = Mobile Home
            2 = Single-Family Detached
            3 = Single-Family Attached
            4 = Apartment in Building containing 2-4 units
            5 = Apartment in Building Containing 5 or more units
            (Table 1 Note:
                Apartment = 4,5)
    Region
        REGIONC 'Census Region'
            1 = Northeast
            2 = Midwest
            3 = South
            4 = West
    Forced-air distribution
        EQUIPM 'Main Home Heating Equipment'
            2  = Steam or hot water system with radiators or pipes 
            3  = Central Furnace
            4  = Central Heat Pump
            5  = Built-In Electric Units In The Walls, ceilings, baseboards, or floors
            7  = Buit-in Room Heater Burning Gas or Oil
            8  = Wood or Pellet Stove
            10 = Portable Electric Heaters
            13 = Ductless heat pump, also know as a "mini-split" 
            99 = Other
            -2 = Not Applicable
            (Table 1 Note(s):
                Yes = 3
                No = 2,4,5,7,8,10,13,99,-2) 
    Floor area
        (Note(s): currently not part of the dataset)
    Occupants per household
        NHSLDMEM 'Number Of Household Members'
            (true values)
            1 = 1
            2 = 2
            3 = 3
            4 = 4
            5 = 5
            6 = 6
            7 = 7
            (Table 1 Note(s):
                1 = 1
                2 = 2
                3-4 = 3,4
                ≥5 = 5,6,7)
    Central air conditioning
        ACEQUIPM_pub 'Main air conditioning equipment type'
            1 = Central air conditioner (includes central heat pump)
            3 = Ductless heat pump, also known as a “mini-split”
            4 = Window or wall air conditioner
            5 = Portable air conditioner
            6 = Evaporative or swamp cooler
            -2 = Not applicable
            (Table 1 Note(s):
                Yes = 1
                No = 3,4,5,6,-2)
    Year built
        YEARMADERANGE 'Range when housing unit was built'
            1 = Before 1950
            2 = 1950 to 1959
            3 = 1960 to 1969
            4 = 1970 to 1979
            5 = 1980 to 1989
            6 = 1990 to 1999
            7 = 2000 to 2009
            8 = 2010 to 2015
            9 = 2016 to 2020
            (Table 1 note(s):
                <1940 = *not directly available 
                1940-194 = *not directly available 
                1950-1959 = 2
                1960-1969 = 3
                1970-1979 = 4
                1980-1989 = 5
                >1990 = 6,7,8,9
                New range will need to be developed)
    Garage or carport
        PRKGPLC1 'Attached garage'
            1 = Yes
            0 = No
            -2 = Not applicable
            (Table 1 Note(s):
                The garage or carport has been change to only attached garages with no other options available)
    Foundations type
        CELLAR  'Housing unit over a basement' 
            0 = No
            1 = Yes
            -2 = Not Applicable
            (Table 1 Note(s):
                Basement = 1)
        CRAWL  'Housing unit over a crawlspace'
            0 = No
            1 = Yes
            -2 = Not Applicable
            (Table 1 Note(s):
                Crawl space = 1)
        CONCRETE 'Housing unit over a concrete slab'
            0 = No
            1 = Yes
            -2 = Not Applicable
            (Table 1 Note(s):
                Slab = 1)
    Number of stories
        STORIES  'Number of stories in a single-family home'
            1 = One story
            2 = Two stories
            3 = Three stories
            4 = Four or more stories
            5 = Split-Level
            -2 = Not Applicable
            (Table 1 Note(s):
                1 = 1
                2 = 2
                ≥3 = 3,4
                How was split-level classed?)
    # of units in building
        (Note(s): This looks to be no longer part of the dataset)        
"""
""" ahs 1997
    Unit type
        NUNIT2
            '1' = 1 unit building, detached
            '2' = 1 unit building, attached
            '3' = Building with 2 or more apartments
            '4' = One unit mobile home
            '5' = Two or more unit mobile home
            (Table 1 Note:
                Manufactured home = '4','5')

    Region
        REGION '1997-2013 National'
            '1' = Northeast
            '2' = Midwest
            '3' = South
            '4' = West

    Forced-air distribution
        HEQUIP 'Main heating equipment'
            '01' = Forced warm-air furnace with ducts and vents to
            '02' = Steam/hot water system with radiators OR other 
            '03' = Electric heat pump
            '04' = Built-in elec. baseboard heat or elec. coils in
            '05' = Floor, wall, or other pipeless furnace built in
            '06' = VENTED room heaters burning kerosene, gas, or o
            '07' = UNVENTED room heaters burning kerosene, gas, or
            '08' = Portable electric heaters
            '09' = Woodburning stove, pot belly stove, Franklin st
            '10' = Fireplace WITH inserts
            '11' = Fireplace WITHOUT inserts
            '12' = Other heating equipment
            '13' = No heating equipment
            '14' = Cooking stove (gas or electric)
            (Table 1 Note(s):
                Yes = '01'
                No = '02','03','04','05','06','07','08','09','10','11','12','13','14') 
            
    Floor area
        UNITSF
            True values
            -9 (note: this is not listed as an value should a '.D' or '.R')
            99 = 99sqft or less
            100-4618 = square footage of unit
            (Table 1 Note(s):
                < 93 m2 (1000 ft2) = all values less then 1000
                93 m2 to186 m2 (1000 ft2 to 1999 ft2) = all values between 1000 - 1999
                186 m2 to 279 m2 (2000 ft2 to 2999 ft2) = all values between 2000 - 2999
                > 279 m2 (3000 ft2) = all values greater then 3000)
            (Table 2 Note(s): For Single family (attached and detached)
                < 149 (1600) = all values less then 1600
                149 to 223 (1600 to 2399) = all values between 1600 - 2399
                > 223 (2400) = all values greater then 2400
                For Apartments
                < 93 (1000) = all values less then 1000
                > 93 (1000) = all values greater then 1000
                For Manufacutured homes
                < 149 (1600) = all values less then 1600
                > 149 (1600) = all values greater then 1600)
            
    Occupants per household
        (note(s): This was not obvious how this was calculated)

    Central air conditioning
        AIR 'Room air conditioner'
            '1' = Yes
            '2' = No
            (Note(s): I am not sure if this would be the best good variable for this) 

    Year built
        BUILT
            1919 = 1919 or earlier
            1920 = 1920 to 1929
            1930 = 1930 to 1939
            1940 = 1940 to 1949
            1950 = 1950 to 1959
            1960 = 1960 to 1969
            1970 = 1970 to 1974
            1975 = 1975 to 1979
            1980 = 1980 to 1984
            1985 = 1985 to 1989
            1990 = 1990
            1991 = 1991
            1992 = 1992
            1993 = 1993
            1994 = 1994
            1995 = 1995
            1996 = 1996
            1997 = 1997
            (Table 1 note(s):
                <1940 = 1919,1920,1930
                1940-1949 = 1940
                1950-1959 = 1950
                1960-1969 = 1960
                1970-1979 = 1970
                1980-1989 = 1980, 1985
                >1990 = 1990,1991,1992,1993,1994,1995,1996,1997)
            (Table 2 Note(s):
                <1940 = 1919,1920,1930
                1940-1969 = 1940,1950,1960
                1970-1989 = 1970,1980,1985
                1990-1997 = 1990,1991,1992,1993,1994,1995,1996,1997) 

    Garage or carport
        GARAGE
            ' ' = Not reported (note: I'm not sure on this one)
            '-9' (note: this is not listed as an value should a 'D' or 'R')
            '1' = Yes
            '2' = No

    Foundations type
        CELLAR 'Unit has a basement'
            '1' = With a basement under all of the house
            '2' = With a basement under part of the house
            '3' = With a crawl space
            '4' = On a concrete slab
            '5' = In some other way (SPECIFY)
            '-6' = Not Applicable 
            (Table 1 note(s):
                Basement = '1','2' 
                Crawl space = '3'
                Slab = '4')  

    Number of stories
        FLOORS
            (Files shows values of:
            1 = 
            2 = 
            3 = 
            4 = 
            5 = 
            But I have no idea what the vaules mean.
            The ahsformat.txt stated that the vaules should be :
            1 = 1 to 20
            21 = 21 or more)

    # of units in building
        WELDUS
            '-6' = not applicable (note: this is not a lised a variable, should be 'B')
            '1' = Only this home
            '2' = 2 to 5 units
            '3' = 6 to 9 units
            '4' = 10 to 14 units
            '5' = 15 or more units
            (Table 2 Note(s): do not line up well with table 2)

"""
""" ahs 2019
    Unit type
        BLD
            '1' = Mobile home or trailer
            '2' = One-family house, detached
            '3' = One-family house, attached
            '4' = 2 apartments
            '5' = 3 to 4 apartments
            '6' = 5 to 9 apartments
            '7' = 10 to 19 apartments
            '8' = 20 to 49 apartments
            '9' = 50 or more apartments
            '10' = Boat, RV, van, etc.
            (Table 1 Note:
                Apartment = '4','5','6','7','8','9')

    Region
        DIVISION
            '1' = New England
            '2' = Middle Atlantic
            '3' = East North Central
            '4' = West North Central
            '5' = South Atlantic
            '6' = East South Central
            '7' = West South Central
            '8' = Mountain
            '9' = Pacific
            (Table 1 Note:
                Northeast = '1','2'
                Midwest = '3','4'
                South = '5','6','7'
                West = '8','9')

    Forced-air distribution
        HEATTYPE
            '1' = Forced warm-air furnace
            '2' = Steam or hot water system
            '3' = Electric heat pump
            '4' = Built-in electric baseboard, electric coils
            '5' = Floor, wall, other pipeless furnace
            '6' = Vented room heaters
            '7' = Unvented room heater[s]
            '8' = Potable electric heater[s]
            '9' = Wood burning, pot belly, Franklin stove
            '10' = Fireplace with inserts
            '11' = Fireplace without inserts
            '12' = Other
            '13' = None
            '14' = Cooking stove used for heating
            (Table 1 Note(s):
                Yes = '01'
                No = '02','03','04','05','06','07','08','09','10','11','12','13','14')
            
    Floor area
        UNITSIZE
            '-9' = Not reported
            '1' = Less than 500 square feet
            '2' = 500 to 749 square feet
            '3' = 750 to 999 square feet
            '4' = 1,000 to 1,499 square feet
            '5' = 1,500 to 1,999 square feet
            '6' = 2,000 to 2,499 square feet
            '7' = 2,500 to 2,999 square feet
            '8' = 3,000 to 3,999 square feet
            '9' = 4,000 square feet or more
            (Table 1 Note(s):
                < 93 m2 (1000 ft2) = '1','2','3'
                93 m2 to186 m2 (1000 ft2 to 1999 ft2) = '4','5'
                186 m2 to 279 m2 (2000 ft2 to 2999 ft2) = '6','7'
                > 279 m2 (3000 ft2) = '8','9')
            (Table 2 Note(s): For Single family (attached and detached) (*needs to break at 500s*)
                < 149 (1600) = '1','2','3','4' 
                149 to 223 (1600 to 2399) = '5','6'
                > 223 (2400) = '7','8','9'
                For Apartments
                < 93 (1000) = '1','2','3'
                > 93 (1000) = '4','5','6','7','8','9'
                For Manufacutured homes
                < 149 (1600) = '1','2','3','4' 
                > 149 (1600) = '5','6','7','8','9')
            
    Occupants per household
        NUMPEOPLE
            -6 = Not applicable
            1 = 1 person
            2 = 2 persons
            3 = 3 persons
            4 = 4 persons
            5 = 5 persons
            6 = 6 persons
            7 = 7 persons or more
            8 = (Not Specified)
            9 = (Not Specified)
            10 = (Not Specified)
            11 = (Not Specified)
            12 = (Not Specified)
            13 = (Not Specified)
            14 = (Not Specified)
            15 = (Not Specified)
            18 = (Not Specified)
            (Note(s): 8-18 are not listed anywhere in the text files for the file.)
            (Table 1 Note(s): data is >7 so the 7-10 and >10 are not avalible
                1 = 1
                2 = 2
                3-4 = 3,4
                5-6 = 5,6
                7-10 = 
                >10 = )

    Central air conditioning
        ACPRIMARY
            '1' = Electric powered central air conditioning system
            '2' = Piped gas powered central air conditioning system
            '3' = LP (liquid petroleum) gas powered central air conditioning system
            '4' = Other fuel source powered air conditioning system
            '5' = 1 room air conditioner
            '6' = 2 room air conditioners
            '7' = 3 room air conditioners
            '8' = 4 room air conditioners
            '9' = 5 room air conditioners
            '10' = 6 room air conditioners
            '11' = 7 or more room air conditioners
            '12' = No air conditioning
            (Table 1 note(s):
                Yes = '1','2','3','4'
                No = '5','6','7','8','9','10','11','12')

    Year built
        YRBUILT
            1919 = 1919 or earlier
            1920 = 1920 to 1929
            1930 = 1930 to 1939
            1940 = 1940 to 1949
            1950 = 1950 to 1959
            1960 = 1960 to 1969
            1970 = 1970 to 1979
            1980 = 1980 to 1989
            1990 = 1990 to 1999
            2000 = 2000 to 2009
            2010 = 2010
            2011 = 2011
            2012 = 2012
            2013 = 2013
            2014 = 2014
            2015 = 2015
            2016 = 2016
            2016 = 2016
            2017 = 2017
            2018 = 2018
            2019 = 2019
            (Table 1 note(s):
                <1940 = 1919,1920,1930
                1940-1949 = 1094
                1950-1959 = 1950
                1960-1969 = 1960
                1970-1979 = 1970
                1980-1989 = 1980
                >1990 = 1990,2000,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019
                New range will need to be developed)

    Garage or carport
        GARAGE
            '-9' (note: this is not listed as an value should a 'M' or 'N')
            '1' = Yes
            '2' = No

    Foundations type
        FOUNDTYPE  
            '-6' = Not applicable
            '1' = Basement under all of the house
            '2' = Basement under part of the house
            '3' = Crawl space
            '4' = Concrete slab
            '5' = Mobile home set up on a masonry foundation
            '6' = Mobile home resting on a concrete pad
            '7' = Mobile home up on blocks, but not on a concrete pad
            '8' = Foundation set up in some other way
            '9' = Mobile home foundation not reported
            (Table 1 note(s):
                Basement = '1','2' 
                Crawl space = '3'
                Slab = '4')  

    Number of stories
        (Note(s): This does not look to be a survey item anymore)

    # of units in building
        BLD (note(s): this is the same variable for unit type)
            '4' = 2 apartments
            '5' = 3 to 4 apartments
            '6' = 5 to 9 apartments
            '7' = 10 to 19 apartments
            '8' = 20 to 49 apartments
            '9' = 50 or more apartments
            (Table 2 note(s): data is 20-49 and >50 so the 20-39 and >40 are not avalible
                2-4 = '4','5'
                5-9 = '6'
                10-19 = '7'
                20-39 = 
                >40 = )

"""

# %% Drop all un needed columns
recs_1997 = recs_1997[['TYPEHUQ', 'NWEIGHT', 'REGIONC', 'EQUIPM', 'SQFTEST', 'NHSLDMEM', 'COOLTYPE', 'YEARMADE', 'PRKGPLCE', 'GARAGE1C', 'GARAGE2C', 'GARAGE3C', 'CELLAR', 'CRAWL', 'CONCRETE', 'STORIES', 'UNITS', 'NUMFLRS']]
recs_2020 = recs_2020[['TYPEHUQ', 'NWEIGHT', 'REGIONC', 'EQUIPM', 'SQFTRANGE', 'NHSLDMEM', 'ACEQUIPM_pub', 'YEARMADERANGE', 'PRKGPLC1', 'SIZEOFGARAGE', 'CELLAR', 'CRAWL', 'CONCRETE', 'STORIES','WALLTYPE','BASEFIN','ATTICFIN','RANGE','COOKTOP','OVEN','RANGEFUEL','RCOOKUSE','ROVENUSE','COOKTOPFUEL', 'COOKTOPUSE', 'OVENFUEL','OVENUSE','HOUSEFAN']]
ahs_1997 = ahs_1997[['NUNIT2', 'WEIGHT', 'REGION', 'HEQUIP', 'UNITSF', 'BUILT', 'GARAGE', 'CELLAR', 'FLOORS', 'WELDUS', 'AIR']]
ahs_2021 = ahs_2021[['BLD', 'WEIGHT', 'DIVISION', 'HEATTYPE', 'UNITSIZE', 'NUMPEOPLE', 'ACPRIMARY', 'YRBUILT', 'GARAGE', 'STORIES', 'FOUNDTYPE', 'COOKFUEL']]

# %% Testing/validating 1997 RECS data
RECS_1997_Unit_type = recs_1997.groupby('TYPEHUQ')['NWEIGHT'].sum()
RECS_1997_Region = recs_1997.groupby('REGIONC')['NWEIGHT'].sum()
#Forcedair_distribution = recs_1997.groupby('ACDUCTS')['NWEIGHT'].sum() #This does not look like the correct variable
RECS_1997_Forcedair_distribution = recs_1997.groupby('EQUIPM')['NWEIGHT'].sum() #This is more correct, but still off
RECS_1997_Floor_area = recs_1997.groupby('SQFTEST')['NWEIGHT'].sum()
RECS_1997_Occupants_per_household = recs_1997.groupby('NHSLDMEM')['NWEIGHT'].sum()
RECS_1997_Central_air_conditioning = recs_1997.groupby('COOLTYPE')['NWEIGHT'].sum() #This does not seem to be correct but is somewhat close
RECS_1997_Year_built = recs_1997.groupby('YEARMADE')['NWEIGHT'].sum()
RECS_1997_Garage_or_carport = recs_1997.groupby('PRKGPLCE')['NWEIGHT'].sum()
RECS_1997_Foundations_type = recs_1997.groupby('CELLAR')['NWEIGHT'].sum(), recs_1997.groupby('CRAWL')['NWEIGHT'].sum(), recs_1997.groupby('CONCRETE')['NWEIGHT'].sum()
RECS_1997_Number_of_stories = recs_1997.groupby('STORIES')['NWEIGHT'].sum()

# %% Testing/validating 2020 RECS data
RECS_2020_Unit_type = recs_2020.groupby('TYPEHUQ')['NWEIGHT'].sum()
RECS_2020_Region = recs_2020.groupby('REGIONC')['NWEIGHT'].sum()
RECS_2020_Forcedair_distribution = recs_2020.groupby('EQUIPM')['NWEIGHT'].sum() #This is more correct, but still off
RECS_2020_Floor_area = recs_2020.groupby('SQFTRANGE')['NWEIGHT'].sum()
RECS_2020_Occupants_per_household = recs_2020.groupby('NHSLDMEM')['NWEIGHT'].sum()
RECS_2020_Central_air_conditioning = recs_2020.groupby('ACEQUIPM_pub')['NWEIGHT'].sum() #This does not seem to be correct but is somewhat close
RECS_2020_Year_built = recs_2020.groupby('YEARMADERANGE')['NWEIGHT'].sum()
RECS_2020_Garage_or_carport = recs_2020.groupby('PRKGPLC1')['NWEIGHT'].sum()
RECS_2020_Foundations_type = recs_2020.groupby('CELLAR')['NWEIGHT'].sum(), recs_2020.groupby('CRAWL')['NWEIGHT'].sum(), recs_2020.groupby('CONCRETE')['NWEIGHT'].sum()
RECS_2020_Number_of_stories = recs_2020.groupby('STORIES')['NWEIGHT'].sum()

# %% Testing/validating 1997 AHS data
AHS_1997_Unit_type = ahs_1997.groupby('NUNIT2')['WEIGHT'].sum()
AHS_1997_Region = ahs_1997.groupby('REGION')['WEIGHT'].sum()
AHS_1997_Forcedair_distribution = ahs_1997.groupby('HEQUIP')['WEIGHT'].sum()
AHS_1997_Floor_area = ahs_1997.groupby('UNITSF')['WEIGHT'].sum()
#AHS_1997_Occupants_per_household = ahs_1997.groupby('')['WEIGHT'].sum() #Not sure what variable this should be
AHS_1997_Central_air_conditioning = ahs_1997.groupby('AIR')['WEIGHT'].sum()
AHS_1997_Year_built = ahs_1997.groupby('BUILT')['WEIGHT'].sum()
AHS_1997_Garage_or_carport = ahs_1997.groupby('GARAGE')['WEIGHT'].sum()
AHS_1997_Foundations_type = ahs_1997.groupby('CELLAR')['WEIGHT'].sum()
AHS_1997_Number_of_stories = ahs_1997.groupby('FLOORS')['WEIGHT'].sum() #Not sure what the result are for this
AHS_1997_Unit_Count = ahs_1997.groupby('WELDUS')['WEIGHT'].sum()

# %% Testing/validating 2019 AHS data
ahs_2021_Unit_type = ahs_2021.groupby('BLD')['WEIGHT'].sum()
ahs_2021_Region = ahs_2021.groupby('DIVISION')['WEIGHT'].sum()
ahs_2021_Forcedair_distribution = ahs_2021.groupby('HEATTYPE')['WEIGHT'].sum()
ahs_2021_Floor_area = ahs_2021.groupby('UNITSIZE')['WEIGHT'].sum()
ahs_2021_Occupants_per_household = ahs_2021.groupby('NUMPEOPLE')['WEIGHT'].sum()
ahs_2021_Central_air_conditioning = ahs_2021.groupby('ACPRIMARY')['WEIGHT'].sum()
ahs_2021_Year_built = ahs_2021.groupby('YRBUILT')['WEIGHT'].sum()
ahs_2021_Garage_or_carport = ahs_2021.groupby('GARAGE')['WEIGHT'].sum()
ahs_2021_Foundations_type = ahs_2021.groupby('FOUNDTYPE')['WEIGHT'].sum()
ahs_2021_Number_of_stories = ahs_2021.groupby('STORIES')['WEIGHT'].sum()
ahs_2021_Unit_Count = ahs_2021.groupby('BLD')['WEIGHT'].sum()

# %% Make workbook for each survey year
#Data type for ahs units is an object value
#AHS 1997
ahs_1997_detached = ahs_1997[ahs_1997.NUNIT2 == "'1'"]
ahs_1997_attached = ahs_1997[ahs_1997.NUNIT2 == "'2'"]
ahs_1997_apartment = ahs_1997[ahs_1997.NUNIT2 == "'3'"]
ahs_1997_mobile1 = ahs_1997[ahs_1997.NUNIT2 == "'4'"]
ahs_1997_mobile2 = ahs_1997[ahs_1997.NUNIT2 == "'5'"]
ahs_1997_mobile = pd.concat([ahs_1997_mobile1, ahs_1997_mobile2], ignore_index=True)

with pd.ExcelWriter('update_ahs_1997.xlsx') as writer:  
    ahs_1997_detached.to_excel(writer, sheet_name='detached')
    ahs_1997_attached.to_excel(writer, sheet_name='attached')
    ahs_1997_apartment.to_excel(writer, sheet_name='apartment')
    ahs_1997_mobile.to_excel(writer, sheet_name='mobile')

# %%
#AHS 2019
ahs_2021_mobile = ahs_2021[ahs_2021.BLD == "'01'"]
ahs_2021_detached = ahs_2021[ahs_2021.BLD == "'02'"]
ahs_2021_attached = ahs_2021[ahs_2021.BLD == "'03'"]
ahs_2021_apt1 = ahs_2021[ahs_2021.BLD == "'04'"]
ahs_2021_apt2 = ahs_2021[ahs_2021.BLD == "'05'"]
ahs_2021_apt3 = ahs_2021[ahs_2021.BLD == "'06'"]
ahs_2021_apt4 = ahs_2021[ahs_2021.BLD == "'07'"]
ahs_2021_apt5 = ahs_2021[ahs_2021.BLD == "'08'"]
ahs_2021_apt6 = ahs_2021[ahs_2021.BLD == "'09'"]
ahs_2021_apartment = pd.concat([ahs_2021_apt1, ahs_2021_apt2, ahs_2021_apt3, ahs_2021_apt4, ahs_2021_apt5, ahs_2021_apt6], ignore_index=True)

with pd.ExcelWriter('update_ahs_2021.xlsx') as writer:  
    ahs_2021_detached.to_excel(writer, sheet_name='detached')
    ahs_2021_attached.to_excel(writer, sheet_name='attached')
    ahs_2021_apartment.to_excel(writer, sheet_name='apartment')
    ahs_2021_mobile.to_excel(writer, sheet_name='mobile')

# %%
#RECS 1997
#Data type for recs units is an int64 value
recs_1997_mobile = recs_1997[recs_1997.TYPEHUQ == 1]
recs_1997_detached = recs_1997[recs_1997.TYPEHUQ == 2]
recs_1997_attached = recs_1997[recs_1997.TYPEHUQ == 3]
recs_1997_apt1 = recs_1997[recs_1997.TYPEHUQ == 4]
recs_1997_apt2 = recs_1997[recs_1997.TYPEHUQ == 5]
recs_1997_apartment = pd.concat([recs_1997_apt1, recs_1997_apt2], ignore_index=True)

with pd.ExcelWriter('update_recs_1997.xlsx') as writer:  
    recs_1997_detached.to_excel(writer, sheet_name='detached')
    recs_1997_attached.to_excel(writer, sheet_name='attached')
    recs_1997_apartment.to_excel(writer, sheet_name='apartment')
    recs_1997_mobile.to_excel(writer, sheet_name='mobile')

# %%
#RECS 2020
recs_2020_mobile = recs_2020[recs_2020.TYPEHUQ == 1]
recs_2020_detached = recs_2020[recs_2020.TYPEHUQ == 2]
recs_2020_attached = recs_2020[recs_2020.TYPEHUQ == 3]
recs_2020_apt1 = recs_2020[recs_2020.TYPEHUQ == 4]
recs_2020_apt2 = recs_2020[recs_2020.TYPEHUQ == 5]
recs_2020_apartment = pd.concat([recs_2020_apt1, recs_2020_apt2], ignore_index=True)

with pd.ExcelWriter('update_recs_2020.xlsx') as writer:  
    recs_2020_detached.to_excel(writer, sheet_name='detached')
    recs_2020_attached.to_excel(writer, sheet_name='attached')
    recs_2020_apartment.to_excel(writer, sheet_name='apartment')
    recs_2020_mobile.to_excel(writer, sheet_name='mobile')


# %%
