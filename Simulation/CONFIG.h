#pragma once
#define RESOLUTION 1024 //amount of grid points of the simulation grid
#define DEPTH 1000.0 //depth of the simulation region in meters
#define DELTA_X (DEPTH/(RESOLUTION - 1)) //spatial step
#define DELTA_T 0.1 //seconds
#define MIN_TEMP 0.0   //lower boundary of plot temperature range in Kelvin
#define MAX_TEMP 300.0 //upper boundary of plot temperature range in Kelvin
