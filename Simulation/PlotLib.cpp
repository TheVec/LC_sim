#include "PlotLib.h"


/**
* plots a single state to WDIR\output\filename.png.
* NOTE: filename may not include spaces
*/
void plotSingleState(double* state, const char* filename, int index, const char* title)
{
	//generating dump path
	char dumpdir[1024];
	sprintf_s(dumpdir, "%s\\dump\\dumpSingleState.txt", WDIR);

	//creating file stream in write mode
	FILE* f;
	fopen_s(&f, dumpdir, "w");

	//printing column information
	fprintf_s(f, "depth[m]\ttemp[K]\n");

	//dumping data
	for (int i = 0; i < RESOLUTION; i++)
	{
		fprintf_s(f, "%e\t%e\n", -i * DELTA_X, state[i]);
	}

	//closing file stream
	fclose(f);

	//generating system call string
	char cmd[1024];
	sprintf_s(cmd, "python %s\\python\\plotSingleState.py %s %e %s_%04d \"%s\" %e %e", WDIR, WDIR, DELTA_X, filename, index, title, MIN_TEMP, MAX_TEMP);

	//running python script
	system(cmd);
}