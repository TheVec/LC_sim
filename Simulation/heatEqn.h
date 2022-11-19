#pragma once

#include "MemoryAllocation.h"
#include "CONFIG.h"
#include "struct.h"
#include "sunAngle.h"

#include <math.h>
#include <stdlib.h>
#include <stdio.h>

void performStep(double* curr, double* next, double time);

void permutePointers(double** curr, double** next);

void setArrayToInitialValue(double* state);