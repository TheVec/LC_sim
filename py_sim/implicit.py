# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 07:29:15 2022

@author: Thierry
"""
import numpy as np
import time as t
import matplotlib.pyplot as plt
import math as m

#Constants needed for sun sim
EARTH_RADIUS = 6.371e6 #Earth radius [meters]
DISTANCE_TO_SUN = 1.496e11 #average distance to sun [meters]
DELTA = m.radians(23.5) #rotaion axis inclination [rad]
OMEGA_D = 2*m.pi/86400 #[rad/s]
OMEGA_Y = 2*m.pi/(365.2422 * 86400) #[rad/s]
global POS_ON_EARTH

#Simulation constants
DEPTH = 30 #[meters]
RESOLUTION = 1024 #array size, number of gridpoints 
DELTA_X = DEPTH/(RESOLUTION-1)
T_BOT = 273.15 + 9.4 #temp at z=-30m [K]
DELTA_T = 1 #[sec], to be replaced with actual expression

#Plot constants
DISPLAY_DEPTH = 25 #[meters]

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

def computeTimeStepUpper():
    pass

def computeTimeStepLower():
    pass

def computeTimeStep():
    pass




POS_ON_EARTH = positionOnEarth(0, 0) #this has to be done first







