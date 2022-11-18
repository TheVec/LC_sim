#pragma once
#define RESOLUTION 1024 //amount of grid points of the simulation grid
#define DEPTH 1000.0 //depth of the simulation region in meters
#define DELTA_X (DEPTH/(RESOLUTION - 1)) //spatial step
#define DELTA_T 0.1 //seconds
#define MIN_TEMP 0.0   //lower boundary of plot temperature range in Kelvin
#define MAX_TEMP 300.0 //upper boundary of plot temperature range in Kelvin

#define DISTANCE_TO_SUN 1.496e11 //meters
#define EARTH_RADIUS 6.371e6 //meters

#define DELTA (23.5 * TAU / 360.0) //earth rotation axis inclination

#define OMEGA_D (TAU) //in radians per day
#define OMEGA_Y (TAU/365.2422) //in radians per day

//math constants
#define TAU 6.28318530718
#define PI 3.14159265358979323846

