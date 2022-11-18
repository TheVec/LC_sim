#pragma once
#include "CONFIG.h"
#include "struct.h"

#include <math.h>
#include <stdio.h>

double computeAngleOfIncidence(double time);

void computePositionInEarthCoordinateSystem(double theta_deg, double phi_deg);

void initializeXiYDelta();