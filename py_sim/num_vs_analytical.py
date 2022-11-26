# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 14:48:14 2022

@author: Thierry
"""

import numpy as np
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
DEPTH = 1 #[meters]
RESOLUTION = 1000  #array size, number of gridpoints 
DELTA_X = DEPTH/(RESOLUTION-1)
DELTA_T = 5e-7 #[sec], to be replaced with actual expression
THERMAL_DIFFUSIVITY = 1
c = DELTA_T/(DELTA_X**2)
print(DELTA_X**2/(2*DELTA_T))

global COEFF_MAT_EXP
global COEFF_MAT_IMP_INV

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

def computeNextTimeStepImp(current_array):
    current_array = COEFF_MAT_IMP_INV@current_array
    return current_array
    
def computeNextTimeStepExp(current_array):
    current_array = COEFF_MAT_EXP@current_array
    return current_array

def computeAnalytical(time, x_arr):
    y = 0
    for i in range(1,6):
        y += (-1)**(i+1)/i * np.sin(i*np.pi*x_arr)*np.exp((-1)*time*(i**2)*(np.pi**2))
    return y

""" Calc Globals
"""
COEFF_MAT_EXP = computeCoeffMatExp()
COEFF_MAT_IMP_INV = np.linalg.inv(computeCoeffMatImp())

x = np.linspace(0, DEPTH, RESOLUTION)
analytical_at_0 = computeAnalytical(0, x)

num_arr_imp = analytical_at_0
num_arr_exp = analytical_at_0

imp_max_res = list()
exp_max_res = list()
timelist = list()
n=0
while DELTA_T*n<0.1:
    if(n%1000 == 0):
        imp_max_res.append(np.max(np.abs(num_arr_imp-computeAnalytical(n*DELTA_T, x))))
        exp_max_res.append(np.max(np.abs(num_arr_exp-computeAnalytical(n*DELTA_T, x))))
        timelist.append(n*DELTA_T) 
    num_arr_exp = computeNextTimeStepExp(num_arr_exp)
    num_arr_imp = computeNextTimeStepImp(num_arr_imp)
    n += 1
print(n-1)
filepath = os.path.realpath(os.path.dirname(__file__))
fig = plt.figure(figsize =(20,15))
plt.plot(timelist, imp_max_res, label = 'Max deviation, implicit')
plt.plot(timelist, exp_max_res, label = 'Max deviation, explicit')
plt.grid(True)
plt.legend()
plt.savefig(filepath + '\\..\\output\\analyticalvexplicit.png')
plt.close(fig)