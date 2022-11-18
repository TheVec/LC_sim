// Simulation.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include "Simulation.h"

int main()
{
    double* prev, * curr, * next;

    allocateStateArray(&prev);
    allocateStateArray(&curr);
    allocateStateArray(&next);

    for (int i = 0; i < 100000000; i++)
    {
        performStep(prev, curr, next);
        permutePointers(&prev, &curr, &next);

        if (i % 1000000 == 0 )
        {
            plotSingleState(curr, "firstSimulation", i / 1000000, "Title");
        }
    }


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

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
