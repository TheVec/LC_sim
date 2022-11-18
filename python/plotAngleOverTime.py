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

data = np.loadtxt(r'X:\LC\LC_sim\LC_sim\dump\angleDump.txt')

time = np.linspace(0.0, 365.0, len(data))

plt.figure(figsize = (36,16), dpi = 60)

plt.plot(time, data)