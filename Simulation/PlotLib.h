#pragma once
#include "WDIR.h"
#include "CONFIG.h"

#include <stdio.h>
#include <stdlib.h>

void plotSingleState(double* state, const char* filename, int index, const char* title);

void clearMultiStateDumpFile();

void appendStateToDumpFile(double* state, double time);

void plotMultiState(const char* filename, const char* title);