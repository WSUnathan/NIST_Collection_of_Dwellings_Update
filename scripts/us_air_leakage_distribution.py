# -*- coding: utf-8 -*-
#%% RUN 
# import needed modules
print('Importing needed modules')
import os
import numpy as np
import pandas as pd
import math
import scipy.stats as stats
from bokeh.plotting import figure, output_file, show
from bokeh.models.tools import HoverTool, CrosshairTool, Span
from bokeh.layouts import gridplot
from bokeh.models import CrosshairTool, Span

#%% RUN User defines directory path for datset, dataset used, and dataset final location
# User set absolute_path
absolute_path = 'C:/Users/nml/OneDrive - NIST/Documents/NIST/suit_of_homes_research/' #USER ENTERED PROJECT PATH
os.chdir(absolute_path)

# ln(NL) = B_area * Area + B_h * H + B_year * I_year + B_IL * I_IL + B_e * I_e
#  + B_cz * I_cz + B_slab * I_slab + B_floor1 * I_floor1 + B_floor2 * Ifloor2
#  + B_cond * I_cond + B_duct1 * I_duct1 + B_duct2 * I_duct2 + e

# to get NL take math.exp(ln(LN))
#%%
B_area = -0.00208
B_h = 0.064
B_year_5 = -0.250 #before 1960
B_year_4 = -0.433 #1960-69
B_year_3 = -0.452 #1970-79
B_year_2 = -0.654 #1980-89
B_year_1 = -0.915 #1990-99
B_year_0 = -1.058 #2000 and after
B_IL = 0.420
B_e = -0.384
B_slab = -0.037
B_floor1 = 0.109
B_floor2 = 0.180
B_cond = -0.124
B_duct1 = 0.071
B_duct2 = 0.181
#needed for e
mu = 0 #values give in paper
variance = 0.2 #values give in paper
sigma = math.sqrt(variance)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
#plt.plot(x, stats.norm.pdf(x, mu, sigma))
#plt.show()
e = stats.norm.pdf(x, mu, sigma)

# %%
NL = math.exp(B_area*92.9+B_year_5*5)
# %%
p = figure(max_width=800, height=400)

p.line()