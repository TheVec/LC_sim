#include "heatEqn.h"

//performs a simulation time step for indices within the simulation domain
void performSingleIndexStepInner(int index, double* prev, double* curr, double* next)
{
	double finite_difference = curr[index - 1] - 2.0 * curr[index] + curr[index + 1];

	next[index] = prev[index] + (2 * THERMAL_DIFFUSIVITY * DELTA_T / (DELTA_X * DELTA_X)) * finite_difference;
} 

//performs a simulation time step for the upper boundary (z=0)
void performSingleIndexStepUpperBoundary(double* prev, double* curr, double* next)
{
	next[0] = prev[0] + (2.0 * DELTA_T * POWER / HEAT_CAPACITY);
}

//performs a simulation time step for the lower boundary (z=-zmax)
void performSingleIndexStepLowerBoundary(double* prev, double* curr, double* next)
{	
	next[RESOLUTION - 1] = 0.0;
}

//performs a simulation time step for all indices.
void performStep(double* prev, double* curr, double* next)
{
	performSingleIndexStepUpperBoundary(prev, curr, next);
	for (int i = 1; i < RESOLUTION - 1; i++)
	{
		performSingleIndexStepInner(i, prev, curr, next);
	}
	performSingleIndexStepLowerBoundary(prev, curr, next);
}

void permutePointers(double** prev, double** curr, double** next)
{
	double* dummy;
	dummy = *prev;
	*prev = *curr;
	*curr = *next;
	*next = dummy;
}