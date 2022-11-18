#pragma once
#define RESOLUTION 128 //amount of grid points of the simulation grid
#define DEPTH 10.0 //depth of the simulation region in meters
#define DELTA_X (DEPTH/(RESOLUTION - 1)) //spatial step
#define DELTA_T 0.00000001 //days
#define MIN_TEMP 0.0   //lower boundary of plot temperature range in Kelvin
#define MAX_TEMP 300.0 //upper boundary of plot temperature range in Kelvin

#define DISTANCE_TO_SUN 1.496e11 //meters
#define EARTH_RADIUS 6.371e6 //meters

#define THERMAL_DIFFUSIVITY 1.15 * 0.0864 // first number is in mm^2/s
#define HEAT_CAPACITY 2.1e6 //J/(m^3 K)
#define POWER 1361.0 * 86400.0 //J/(m^2 d)

#define DELTA (23.5 * TAU / 360.0) //earth rotation axis inclination

#define OMEGA_D (TAU) //in radians per day
#define OMEGA_Y (TAU/365.2422) //in radians per day

//math constants
#define TAU 6.28318530718
#define PI 3.14159265358979323846

