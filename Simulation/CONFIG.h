#pragma once
#define RESOLUTION 1024 //amount of grid points of the simulation grid
#define DEPTH 30.0 //depth of the simulation region in meters
#define DELTA_X (DEPTH/(RESOLUTION - 1)) //spatial step
#define FRAMES_PER_YEAR (2*52)
#define TIMESTEPS_PER_FRAME 2000
#define DELTA_T (86400.0 * 365.2422 / (FRAMES_PER_YEAR * TIMESTEPS_PER_FRAME)) //seconds
#define YEAR_COUNT 400l
#define START_SAVE_YEAR 398l
#define TOTAL_TIMESTEPS YEAR_COUNT * FRAMES_PER_YEAR * TIMESTEPS_PER_FRAME
#define MIN_TEMP 200.0   //lower boundary of plot temperature range in Kelvin
#define MAX_TEMP 600.0 //upper boundary of plot temperature range in Kelvin

#define DISTANCE_TO_SUN 1.496e11 //meters
#define EARTH_RADIUS 6.371e6 //meters

#define THERMAL_DIFFUSIVITY 1.15 * 1e-6 // first number is in mm^2/s
#define HEAT_CAPACITY 1.84e6 //J/(m^3 K)
#define SOLAR_POWER 1361.0 //W/(m^2)
#define CORE_POWER 0.087 //W/(m^2)
#define EPSILON 1.0
#define SIGMA 5.67e-8 //W/(m^2 K^4) Stefan-Boltzmann constant
#define INITIAL_TEMPERATURE 250.0 //Kelvin
#define ALBEDO 0.434 

#define DELTA (23.5 * TAU / 360.0) //earth rotation axis inclination

#define OMEGA_D (TAU / 86400) //in radians per second
#define OMEGA_Y (TAU / (365.2422 * 86400)) //in radians per second

//math constants
#define TAU 6.28318530718
#define PI 3.14159265358979323846

