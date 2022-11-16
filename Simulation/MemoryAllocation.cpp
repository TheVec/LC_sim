#include "MemoryAllocation.h"

void allocateStateArray(double** ptr)
{
	*ptr = (double*)calloc(RESOLUTION, sizeof(double));
}