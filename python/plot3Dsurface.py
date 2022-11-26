import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm
from datetime import datetime
from mpl_toolkits.axes_grid1 import AxesGrid
import matplotlib.ticker as ticker

import sys

import time

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

fig = plt.figure(figsize=(16,12))

ax = fig.add_subplot(111, projection='3d')

ax.view_init(30, 340)

ax.set_box_aspect(aspect = (4,2,1))
# plot a 3D surface like in the example mplot3d/surface3d_demo
Y = -np.arange(0, (resolution) * deltax, deltax)
Y, X = np.meshgrid(Y, X)

plt.subplots_adjust(bottom=0.0, right=1.0, top=1.0, left = 0.0)

ax.set_xlabel('Time')
ax.set_ylabel('Depth')
ax.set_zlabel('Temperature')
#ax.set_ylim(np.min(X), np.max(X))

#surf = ax.plot_surface(X, Y, Z-273.15, rstride=1, cstride=1, cmap=cm.nipy_spectral, linewidth=0, antialiased=False)
surf = ax.plot_surface(X, Y, Z-273.15, rstride=1, cstride=1, cmap=cm.CMRmap, linewidth=0, antialiased=False)


fig.colorbar(surf, shrink=0.5, aspect=10)
print("Saving image file to " + savepath)
plt.savefig(savepath, dpi = 600)