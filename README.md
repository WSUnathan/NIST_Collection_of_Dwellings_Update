# NIST_Collection_of_Dwellings_Update
# Collection of Dwelling

## Overview

The Collection of Dwelling repository contains a collection of Python scripts for managing and processing dwelling-related data. This repository is designed to provide a centralized location for storing and sharing scripts related to dwelling data.

## Repository Structure

The repository is structured as follows:

* `scripts/`: This directory contains the Python scripts for managing and processing dwelling data.

## Scripts

The following Python scripts are included in the `scripts/` directory:

### Data Analysis and Processing Scripts

* `ahs21_weighted_average.py`: Calculates weighted averages for AHS 2021 data.
* `ahs_recs_data_comparison.py`: Compares AHS and RECS data.
* `characteristic_distribution.py`: Analyzes the distribution of dwelling characteristics.
* `recs20_sqft_weighted_average.py`: Calculates weighted averages for RECS 2020 data by square footage.
* `recs_characteristic_distribution.py`: Analyzes the distribution of RECS dwelling characteristics.
* `recs_characteristic_distribution_test(ahs).py`: Tests the distribution of RECS dwelling characteristics against AHS data.
* `recs_characteristic_distribution_test(year).py`: Tests the distribution of RECS dwelling characteristics by year.
* `update_values_recs97.py`: Updates values in RECS 1997 data.

### Data Visualization Scripts

* `collectionofdwelling_piechart.py`: Creates a pie chart for dwelling data.
* `nist_housing_visualization.py`: Visualizes NIST housing data.
* `nist_housing_viz_fixed.py`: Visualizes NIST housing data with fixes.

### Other Scripts

* `manufacured_house_us_rep.py`: Analyzes manufactured house data in the US.
* `us_air_leakage_distribution.py`: Analyzes air leakage distribution in US dwellings.
* `wap_calc.py`: Calculates WAP (Weatherization Assistance Program) data.

## Usage

To use the scripts in this repository, follow these steps:

1. Clone the repository to your local machine using `git clone https://gitlab.com/your-username/collection-of-dwelling.git`.
2. Navigate to the `scripts/` directory.
3. Run the desired Python script using `python script_name.py`.

For example, to calculate weighted averages for AHS 2021 data, run:
```bash
python ahs21_weighted_average.py
```

## Requirements 

The scripts in this repository require the following dependencies: 

Python 3.x
pandas library for data manipulation and analysis
matplotlib library for data visualization
numpy library for numerical computations