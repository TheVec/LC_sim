# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 13:48:41 2022

@author: Thierry
"""

import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams['font.size'] = '15'
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]})
plt.rc('font', family='serif') 
plt.rc('font', serif='Helvetica') 

DEPTH = 30

filepath = os.path.realpath(os.path.dirname(__file__))
filepath = filepath + '\\comp_speed_data.txt'
resolution = np.loadtxt(filepath, usecols = [3], skiprows = 1)
frames_per_year = np.loadtxt(filepath, usecols = [0], skiprows = 1)
timesteps_per_frame = np.loadtxt(filepath, usecols = [1], skiprows = 1)
years = np.loadtxt(filepath, usecols = [2], skiprows = 1)
k = np.loadtxt(filepath, usecols = [4], skiprows = 1)
dur_imp = np.loadtxt(filepath, usecols = [5], skiprows = 1)
dur_exp = np.loadtxt(filepath, usecols = [6], skiprows = 1)

total_time_steps = years * frames_per_year * timesteps_per_frame

delta_x = DEPTH/(resolution-1)
delta_t = (86400.0 * 365.2422 / (frames_per_year * timesteps_per_frame))
fig = plt.figure(figsize = (20,15))
plt.grid(True)
plt.title('Computation speed quotient', fontsize = 50)
# plt.plot(delta_x*delta_x/(2*k*delta_t), dur_exp/dur_imp, 'o')
plt.plot(resolution, (dur_exp/dur_imp),'o')
plt.xlabel(r'$\frac{(\Delta x)^2}{2K\Delta t}$', fontsize = 35)
plt.ylabel(r'$\frac{t_{exp}}{t_{imp}}$', fontsize = 35)
plt.savefig(os.path.realpath(os.path.dirname(__file__))+'\\..\\output\\timetest.png')
plt.close(fig)