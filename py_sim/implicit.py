# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 07:29:15 2022

@author: Thierry

"""
import numpy as np
import time as t
import matplotlib.pyplot as plt
import math as m
import os

plt.rcParams['font.size'] = '25'
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]})
plt.rc('font', family='serif') 
plt.rc('font', serif='Helvetica') 


#Simulation constants
FRAMES_PER_YEAR = 10
TIMESTEPS_PER_FRAME = 20
YEAR_COUNT = 1    
DEPTH = 30 #[meters]
RESOLUTION = 200  #array size, number of gridpoints 
DELTA_X = DEPTH/(RESOLUTION-1)
T_BOT = 273.15 + 9.4 #temp at z=-30m [K]
DELTA_T = (86400.0 * 365.2422 / (FRAMES_PER_YEAR * TIMESTEPS_PER_FRAME)) #[sec], to be replaced with actual expression
THERMAL_DIFFUSIVITY = 2e-6 
T_TOP = 300 #might add sun-power and stuff later on
global COEFF_MAT_IMP_INV #coefficient matrix for implicit solver
global COEFF_MAT_EXP #coefficient matrix for explicit solver
TOTAL_TIMESTEPS = YEAR_COUNT * FRAMES_PER_YEAR * TIMESTEPS_PER_FRAME
global c
c = DELTA_T*THERMAL_DIFFUSIVITY/(DELTA_X**2) #helper constant
print('c: ',c)


""" Computes the coefficient matrix for the matrix equation to be solved in every
    timestep (Ax_n+1 = x_n)
"""
def computeCoeffMatImp():
    A = np.zeros((RESOLUTION,RESOLUTION))
    for i in range(1,RESOLUTION-1):
        A[i][i] = 1 + 2*c
        A[i][i-1] = -c
        A[i][i+1] = -c
    A[0][0] = 1
    A[RESOLUTION-1][RESOLUTION-1] = 1
    return A

def computeCoeffMatExp():
    A = np.zeros((RESOLUTION,RESOLUTION))
    for i in range(1,RESOLUTION-1):
        A[i][i] = 1 - 2*c
        A[i][i-1] = c
        A[i][i+1] = c
    A[0][0] = 1
    A[RESOLUTION-1][RESOLUTION-1] = 1
    return A
""" Computes Array of next step
"""
def computeNextTimeStepImp(time, current_array):
    current_array = COEFF_MAT_IMP_INV@current_array
    return current_array
    
def computeNextTimeStepExp(time, current_array):
    current_array = COEFF_MAT_EXP@current_array
    return current_array


def computeAnalytical(time, x_arr):
    y = 0
    for i in range(1,6):
        y += (-1)**(i+1)/i * np.sin(i*np.pi*x_arr)*np.exp((-1)*time*(i**2)*(np.pi**2))
    return y


""" Initialize global constants 
"""
filepath = os.path.realpath(os.path.dirname(__file__))
depth = np.linspace(0,-1*DEPTH, RESOLUTION)

""" Implicit solver
"""
start_time = t.time()
COEFF_MAT_IMP_INV = np.linalg.inv(computeCoeffMatImp())

curr_arr = np.zeros(RESOLUTION)
curr_arr[0] = T_TOP
curr_arr[RESOLUTION-1] = T_BOT

print("DELTA_T = ", DELTA_T)
print("DELTA_X^2/2K", DELTA_X*DELTA_X/(2*THERMAL_DIFFUSIVITY))
print("Implicit: ")
for i in range(0,TOTAL_TIMESTEPS):
    curr_arr = computeNextTimeStepImp(i*DELTA_T, curr_arr)
    """ Used for stability testing, commented out for computation speed test
        since matplotlib is quite slow
    """
    # if (i%TIMESTEPS_PER_FRAME == 0):
    #     savepath = filepath + '\\..\\output\\stabilitytest_imp' + str(i%TIMESTEPS_PER_FRAME)
    #     fig = plt.figure(figsize = (10,5))
    #     plt.grid(True)
    #     plt.plot(curr_arr, depth)
    #     plt.savefig(savepath)
    #     plt.close(fig)
end_time = t.time()
imp_result = curr_arr
print("Time needed: ", end_time-start_time, "s")

""" Explicit Solver
"""
print("Explicit:")
start_time = t.time()
COEFF_MAT_EXP = computeCoeffMatExp()
curr_arr1 = np.zeros(RESOLUTION)
curr_arr1[0] = T_TOP
curr_arr1[RESOLUTION-1] = T_BOT
for i in range(0, TOTAL_TIMESTEPS):
    """ Used for stability testing, commented out for computation speed test
        since matplotlib is quite slow
    """
    if (i%TIMESTEPS_PER_FRAME == 0):
        savepath = filepath + '\\..\\output\\stabilitytest_exp' + str(i)
        fig = plt.figure(figsize = (20,15))
        plt.grid(True)
        plt.title('Example unstable Simulation parameters', fontsize = 50)
        plt.plot(curr_arr1, depth)
        plt.xlabel('Temp [K]', fontsize = 25)
        plt.ylabel('Depth [m]', fontsize = 25)
        plt.savefig(savepath)
        plt.close(fig)
    curr_arr1 = computeNextTimeStepExp(i*DELTA_T, curr_arr1)
end_time = t.time()
exp_result = curr_arr1
print("Time needed: ", end_time - start_time, "s")

""" Plotting
"""
filepath = os.path.realpath(os.path.dirname(__file__))
filepath = filepath + '\\..\\output\\'
print(filepath)
depth = np.linspace(0,-1*DEPTH, RESOLUTION)
fig = plt.figure(figsize=(20,10))
plt.grid(True)
plt.title('Stability Test for $\Delta t = $ '+str( DELTA_T )+'and $ (\Delta x)^2 / 2\cdot K = $' +str(DELTA_X*DELTA_X/(2*THERMAL_DIFFUSIVITY)), fontsize = 30)
plt.plot(imp_result, depth, color = 'green', label = 'implicit')
plt.plot(exp_result, depth, color = 'red', label = 'explicit')
plt.legend(fontsize = 15)
plt.xlabel('Temp [K]', fontsize = 20)
plt.ylabel('Depth [m]', fontsize = 20)
plt.savefig(filepath+'stabilitytest.png')
plt.close(fig)





