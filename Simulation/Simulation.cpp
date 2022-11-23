// Simulation.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include "Simulation.h"

int main()
{
    double * curr, * next;


    printf("timestep %s\n", (DELTA_T < DELTA_X * DELTA_X / (4.0 * THERMAL_DIFFUSIVITY)) ? "ok" : "not ok");
    printf("equilibrium ratio (1-a)/epsilon = %.3lf\n", (1 - ALBEDO) / EPSILON);

    allocateStateArray(&curr);
    setArrayToInitialValue(curr);
    allocateStateArray(&next);
    setArrayToInitialValue(next);

    char title[1023];

    computePositionInEarthCoordinateSystem(54.12, -20.26);
    initializeXiYDelta();

    clock_t start = clock();


    for (int i = 0; i < TOTAL_TIMESTEPS; i++)
    {
        performStep(curr, next, i * DELTA_T);
        permutePointers(&curr, &next);

        if (i % TIMESTEPS_PER_FRAME == TIMESTEPS_PER_FRAME - 1)
        {
            printf("%.2lf%%\r", 100.0* (i /( (double) TOTAL_TIMESTEPS)));
            if (i / (TIMESTEPS_PER_FRAME * FRAMES_PER_YEAR) > START_SAVE_YEAR)
            {
                printf("\n");
                sprintf_s(title, "$t=%lf$ years", i * DELTA_T / (86400.0 * 365.2422));
                plotSingleState(curr, "firstSimulation", i / TIMESTEPS_PER_FRAME, title);
            }
        }
    }

    double millis = 1000.0 * (clock() - start) / (double)CLOCKS_PER_SEC;
    printf("%.3lfms\n", millis);



    //computePositionInEarthCoordinateSystem(0.0, -7.5);
    //initializeXiYDelta();

    //char path[1023];
    //sprintf_s(path, "%s\\dump\\angleDump.txt", WDIR);
    //FILE* f;
    //fopen_s(&f, path, "w");

    //if (f != 0)
    //{
    //    for (int i = 0; i < 36500; i++)
    //    {
    //        fprintf_s(f, "%.1lf\n", 360.0 * computeAngleOfIncidence(0.01 * i) / TAU);
    //    }
    //    
    //    fclose(f);
    //}   
}

