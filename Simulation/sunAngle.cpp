#include "sunAngle.h"

vec3 positionOnEarth;
mat3x3 xi_y_delta;

/*
* theta_deg = North/South angle, North = positive, in degrees
* phi_deg = West/East angle, West = positive, in degrees
*/
void computePositionInEarthCoordinateSystem(double theta_deg, double phi_deg)
{
	double theta = TAU * (theta_deg / 360.0);
	double phi = TAU * (phi_deg) / 360.0;

	positionOnEarth.x = EARTH_RADIUS * cos(phi) * cos(theta);
	positionOnEarth.y = EARTH_RADIUS * sin(phi) * cos(theta);
	positionOnEarth.z = EARTH_RADIUS * sin(theta);
}

//angle in radians
mat3x3 computeZaxisRotationMatrix(double angle)
{
	mat3x3 result;

	result.m[0][0] = cos(angle);
	result.m[0][1] = -sin(angle);
	result.m[0][2] = 0.0;
	result.m[1][0] = sin(angle);
	result.m[1][1] = cos(angle);
	result.m[1][2] = 0.0;
	result.m[2][0] = 0.0;
	result.m[2][1] = 0.0;
	result.m[2][2] = 1.0;

	return result;
}

mat3x3 computeYaxisRotationMatrix(double angle)
{
	mat3x3 result;

	result.m[0][0] = cos(angle);
	result.m[0][1] = 0.0;
	result.m[0][2] = sin(angle);
	result.m[1][0] = 0.0;
	result.m[1][1] = 1.0;
	result.m[1][2] = 0.0;
	result.m[2][0] = -sin(angle);
	result.m[2][1] = 0.0;
	result.m[2][2] = cos(angle);

	return result;
}

void initializeXiYDelta()
{
	xi_y_delta = computeYaxisRotationMatrix(DELTA);
}

vec3 computeMatrixVecProduct(mat3x3 mat, vec3 v)
{
	vec3 result;
	
	result.x = mat.m[0][0] * v.x + mat.m[0][1] * v.y + mat.m[0][2] * v.z;
	result.y = mat.m[1][0] * v.x + mat.m[1][1] * v.y + mat.m[1][2] * v.z;
	result.z = mat.m[2][0] * v.x + mat.m[2][1] * v.y + mat.m[2][2] * v.z;

	return result;
}

//unit of time is seconds
vec3 computeNormalVector(double time)
{
	mat3x3 day_rotation = computeZaxisRotationMatrix((OMEGA_D) * time);
	mat3x3 year_rotation = computeZaxisRotationMatrix((OMEGA_Y) * time);

	vec3 result = positionOnEarth;
	//printf("(%.1lf, %.1lf, %.1lf)\n", result.x, result.y, result.z);
	result = computeMatrixVecProduct(day_rotation, result);
	//printf("(%.1lf, %.1lf, %.1lf)\n", result.x, result.y, result.z);
	result = computeMatrixVecProduct(xi_y_delta, result);
	//printf("(%.1lf, %.1lf, %.1lf)\n", result.x, result.y, result.z);
	result = computeMatrixVecProduct(year_rotation, result);
	//printf("(%.1lf, %.1lf, %.1lf)\n", result.x, result.y, result.z);
	//printf("------------------------------------------\n");

	return result;
}

/*
* unit of time is seconds
* initializeXiYDelta() MUST be ran once before this.
*/
double computeAngleOfIncidence(double time)
{
	vec3 normal = computeNormalVector(time);

	vec3 diff;
	diff.x = DISTANCE_TO_SUN - normal.x;
	diff.y = -normal.y;
	diff.z = -normal.z; //NOTE: DISTANCE_TO_SUN could be replaced by a more complex function to account for changes in distance over the course of a year

	double numerator = normal.x * diff.x + normal.y * diff.y + normal.z * diff.z;
	double normal_abs_sq = normal.x * normal.x + normal.y * normal.y + normal.z * normal.z;
	double diff_abs_sq = diff.x * diff.x + diff.y * diff.y + diff.z * diff.z;

	double result = asin(numerator / (sqrt(normal_abs_sq * diff_abs_sq)));
	return result;
}