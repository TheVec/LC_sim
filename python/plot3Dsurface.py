import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.ticker as ticker

import sys

import time

plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.rcParams['font.size'] = '25'
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]})
plt.rc('font', family='serif') 
plt.rc('font', serif='Helvetica') 

hfont = {'fontname':'Helvetica'}

wdir = sys.argv[1]
deltax = float(sys.argv[2])
filename = sys.argv[3]
title = sys.argv[4]
min_temp = float(sys.argv[5])-273.15
max_temp = float(sys.argv[6])-273.15
display_depth = float(sys.argv[7])
resolution = int(sys.argv[8])

dumppath = wdir + r"\dump\dumpMultiState.txt"
savepath = wdir + r'\output\\' + filename

X = np.loadtxt(dumppath, usecols = [0])
Z = np.loadtxt(dumppath, usecols = range(1,resolution+1))

fig = plt.figure(figsize=(16,7))

ax = fig.add_subplot(111)

# plot a 3D surface like in the example mplot3d/surface3d_demo
Y = -np.arange(0, (resolution) * deltax, deltax)
Y, X = np.meshgrid(Y, X)

plt.subplots_adjust(bottom=0.05, right=1.0, top=0.95, left = 0.1)
ax.set_title(title, fontsize = 35)
ax.set_xlabel('Time [years]')
ax.set_ylabel('Depth [m]')
#ax.set_ylim(np.min(X), np.max(X))

timesteps = Z.size//resolution

#surf = ax.plot_surface(X, Y, Z-273.15, rstride=1, cstride=1, cmap=cm.nipy_spectral, linewidth=0, antialiased=False)

#for yearly dependence
#im = ax.imshow(np.transpose(Z)-273.15, cmap = 'inferno', aspect=0.05, extent = [0.0, 1.0, -display_depth, 0.0])

#for daily dependence
im = ax.imshow(np.transpose(Z[:][range(3*timesteps//4,timesteps)])-273.15, cmap = 'inferno', aspect=0.05, extent = [0.0, 0.25, -display_depth, 0.0])

fig.colorbar(im, shrink=0.5, aspect=15, label = r"Temperature [$^\circ$C]")
print("Saving image file to " + savepath)
plt.savefig(savepath, dpi = 180)