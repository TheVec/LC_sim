#pragma once

#include "MemoryAllocation.h"
#include "CONFIG.h"
#include "struct.h"

#include <math.h>
#include <stdlib.h>
#include <stdio.h>

void performStep(double* prev, double* curr, double* next);

void permutePointers(double** prev, double** curr, double** next);