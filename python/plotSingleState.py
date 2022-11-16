import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.ticker as ticker

import sys

plt.ticklabel_format(style='sci', axis='x', scilimits=(-5,100))
plt.rcParams['font.size'] = '30'
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]})
plt.rc('font', family='serif') 
plt.rc('font', serif='Helvetica') 

wdir = sys.argv[1]
deltax = float(sys.argv[2])
filename = sys.argv[3]
title = sys.argv[4]
min_temp = float(sys.argv[5])
max_temp = float(sys.argv[6])

dumppath = wdir + r"\dump\dumpSingleState.txt"
savepath = wdir + r'\output\\' + filename

print("Reading data from " + dumppath)


depth = np.loadtxt(dumppath, skiprows = 1, usecols = [0])
temp = np.loadtxt(dumppath, skiprows = 1, usecols = [1])

fig = plt.figure(figsize = (14,12), dpi = 120)
ax = plt.gca()
plt.plot(temp, depth, linewidth = 5)
plt.xlabel("Temperature $T$ [K]")
plt.ylabel("Depth $z$ [m]")
plt.title(title)
ax.set_xlim(left = min_temp, right = max_temp)

print("Saving image file to " + savepath)
plt.savefig(savepath)
