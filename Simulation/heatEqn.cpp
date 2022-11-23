#include "heatEqn.h"

//performs a simulation time step for indices within the simulation domain
inline void performSingleIndexStepInner(int index, double* curr, double* next)
{
	double finite_difference = curr[index - 1] - 2.0 * curr[index] + curr[index + 1];

	next[index] = curr[index] + (THERMAL_DIFFUSIVITY * DELTA_T / (DELTA_X * DELTA_X)) * finite_difference;
} 

//performs a simulation time step for the upper boundary (z=0)
inline void performSingleIndexStepUpperBoundary(double* curr, double* next, double time)
{
	double currsq = curr[0] * curr[0];
	double currquart = currsq * currsq;

	double sunAngle = computeAngleOfIncidence(time);

	double powerFac = (sunAngle < 0.0) ? 0.0 : sin(sunAngle);

	next[0] = curr[0] + (DELTA_T * ((1-ALBEDO) * powerFac * SOLAR_POWER - EPSILON * SIGMA * currquart) / HEAT_CAPACITY) + (THERMAL_DIFFUSIVITY * DELTA_T / (DELTA_X * DELTA_X)) * (curr[1] - curr[0]);
}

//performs a simulation time step for the lower boundary (z=-zmax)
inline void performSingleIndexStepLowerBoundary(double* curr, double* next)
{	
	//next[RESOLUTION - 1] = curr[RESOLUTION - 1] + ((DELTA_T * CORE_POWER) / HEAT_CAPACITY);
	next[RESOLUTION - 1] = LOWER_CONSTANT_TEMPERATURE;
}

//performs a simulation time step for all indices.
void performStep(double* curr, double* next, double time)
{
	performSingleIndexStepUpperBoundary(curr, next, time);
	for (int i = 1; i < RESOLUTION - 1; i++)
	{
		performSingleIndexStepInner(i, curr, next);
	}
	performSingleIndexStepLowerBoundary(curr, next);
}

void permutePointers(double** curr, double** next)
{
	double* dummy;
	dummy = *curr;
	*curr = *next;
	*next = dummy;
}

void setArrayToInitialValue(double* state)
{
	for (int i = 0; i < RESOLUTION; i++)
	{
		state[i] = INITIAL_SURFACE_TEMPERATURE + (LOWER_CONSTANT_TEMPERATURE - INITIAL_SURFACE_TEMPERATURE) * (i/((double)RESOLUTION));
	}
}