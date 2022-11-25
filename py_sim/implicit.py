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

#Constants needed for sun sim
EARTH_RADIUS = 6.371e6 #Earth radius [meters]
DISTANCE_TO_SUN = 1.496e11 #average distance to sun [meters]
DELTA = m.radians(23.5) #rotaion axis inclination [rad]
OMEGA_D = 2*m.pi/86400 #[rad/s]
OMEGA_Y = 2*m.pi/(365.2422 * 86400) #[rad/s]
global POS_ON_EARTH

#Simulation constants
FRAMES_PER_YEAR = 100
TIMESTEPS_PER_FRAME = 2000    
YEAR_COUNT = 3   
DEPTH = 30 #[meters]
RESOLUTION = 1024  #array size, number of gridpoints 
DELTA_X = DEPTH/(RESOLUTION-1)
T_BOT = 273.15 + 9.4 #temp at z=-30m [K]
DELTA_T = (86400.0 * 365.2422 / (FRAMES_PER_YEAR * TIMESTEPS_PER_FRAME)) #[sec], to be replaced with actual expression
THERMAL_DIFFUSIVITY = 2e-6
HEAT_CAPACITY = 2
ALBEDO = 0
EPSILON = 1
SUN_POWER = 1000
T_TOP = 300 #might add sun-power and stuff later on
global COEFF_MAT_IMP_INV #coefficient matrix for implicit solver
global COEFF_MAT_EXP_INV #coefficient matrix for explicit solver
TOTAL_TIMESTEPS = YEAR_COUNT * FRAMES_PER_YEAR * TIMESTEPS_PER_FRAME
global c
c = DELTA_T*THERMAL_DIFFUSIVITY/(DELTA_X**2) #helper constant
print('c: ',c)


""" earth coordinates from given longi-/latitude angles, taken in degrees

    longitude = north/south; positive = north
    latitude = east/west; positive = east

    comment: has minor floating point errors, e.g. (-90, 0) does not yield (0, 0, -EARTH_RADIUS)
    as would be expected, but instead gives (~4e-10, 0, -EARTH_RADIUS). 
"""
def positionOnEarth(longitude,latitude):
    posVector = [0,0,0] #(x,y,z)
    longitude = m.radians(longitude)
    latitude = m.radians(latitude)
    posVector[0] = EARTH_RADIUS*m.cos(longitude)*m.cos(latitude)
    posVector[1] = EARTH_RADIUS*m.cos(longitude)*m.sin(latitude)
    posVector[2] = EARTH_RADIUS*m.sin(longitude)
    return posVector

""" angle in radians
    bonus feature: floating point errors coming from trigonmetric functions
"""
def computeRotMatZax(angle):
    M = np.zeros((3,3))
    M[0][0] = m.cos(angle)
    M[0][1] = -m.sin(angle)
    M[1][0] = m.sin(angle)
    M[1][1] = m.cos(angle)
    M[2][2] = 1
    return M

""" angle in radians
"""
def computeRotMatYax(angle):
    M = np.zeros((3,3))
    M[0][0] = m.cos(angle)
    M[0][2] = m.sin(angle)
    M[1][1] = 1
    M[2][0] = -m.sin(angle)
    M[2][2] = m.cos(angle)
    return M

""" unit of time is seconds
"""
def computeNormalVec(time):
    day_rotation = computeRotMatZax(OMEGA_D*time)
    year_rotation = computeRotMatZax(OMEGA_Y*time)
    result = np.matmul(year_rotation, np.matmul(computeRotMatYax(DELTA), np.matmul(day_rotation, POS_ON_EARTH)))
    return result

def computeAngleOfIncidence(time):
    norm = computeNormalVec(time)
    diff = [DISTANCE_TO_SUN, 0, 0] - norm
    
    numerator = norm@diff
    norm_sq = norm@norm
    diff_sq = diff@diff
    
    return m.asin(numerator/(m.sqrt(norm_sq*diff_sq)))

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

def computeT_TOP(time, T_TOP_prev):
    inc_angle = computeAngleOfIncidence(time)
    if inc_angle < 0:
        power_fac = 0
    else:
        power_fac = m.sin(inc_angle)
    T_TOP_a = power_fac*(1-ALBEDO)*SUN_POWER
    return T_TOP_a

""" Initialize global constants 
"""
POS_ON_EARTH = positionOnEarth(0, 0) #this has to be done first
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
    if (i%TIMESTEPS_PER_FRAME == 0):
        savepath = filepath + '\\..\\output\\stabilitytest_imp' + str(i%TIMESTEPS_PER_FRAME)
        fig = plt.figure(figsize = (10,5))
        plt.grid(True)
        plt.plot(curr_arr, depth)
        plt.savefig(savepath)
        plt.close(fig)
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
    curr_arr1 = computeNextTimeStepExp(i*DELTA_T, curr_arr1)
    """ Used for stability testing, commented out for computation speed test
        since matplotlib is quite slow
    """
    if (i%TIMESTEPS_PER_FRAME == 0):
        savepath = filepath + '\\..\\output\\stabilitytest_exp' + str(i%TIMESTEPS_PER_FRAME)
        fig = plt.figure(figsize = (10,5))
        plt.grid(True)
        plt.plot(curr_arr1, depth)
        plt.savefig(savepath)
        plt.close(fig)
end_time = t.time()
exp_result = curr_arr1
print("Time needed: ", end_time - start_time, "s")

""" Plotting
"""
filepath = os.path.realpath(os.path.dirname(__file__))
filepath = filepath + '\\..\\output\\stabilitytest.png'
print(filepath)
depth = np.linspace(0,-1*DEPTH, RESOLUTION)
# fig = plt.figure(figsize=(20,10))
# plt.grid(True)
# plt.title('Stability Test for $\Delta t = $ '+str( DELTA_T )+'and $ (\Delta x)^2 / 2\cdot K = $' +str(DELTA_X*DELTA_X/(2*THERMAL_DIFFUSIVITY)), fontsize = 30)
# plt.plot(imp_result, depth, color = 'green', label = 'implicit')
# plt.plot(exp_result, depth, color = 'red', label = 'explicit')
# plt.legend(fontsize = 15)
# plt.xlabel('Temp [K]', fontsize = 20)
# plt.ylabel('Depth [m]', fontsize = 20)
# plt.savefig(filepath)
# plt.close(fig)