#include "PlotLib.h"

int rowcount = 0;
int firstcolumn = 1;

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
	sprintf_s(cmd, "python %s\\python\\plotSingleState.py %s %e %s_%04d \"%s\" %e %e %e", WDIR, WDIR, DELTA_X, filename, index, title, MIN_TEMP, MAX_TEMP, DISPLAY_DEPTH);

	//running python script
	system(cmd);
}

void clearMultiStateDumpFile()
{
	char dumpdir[1024];
	sprintf_s(dumpdir, "%s\\dump\\dumpMultiState.txt", WDIR);

	//creating file stream in write mode
	FILE* f;
	fopen_s(&f, dumpdir, "w");

	fprintf_s(f, "");

	fclose(f);
}

void appendStateToDumpFile(double* state, double time)
{
	//generating dump path
	char dumpdir[1024];
	sprintf_s(dumpdir, "%s\\dump\\dumpMultiState.txt", WDIR);

	//creating file stream in write mode
	FILE* f;
	fopen_s(&f, dumpdir, "a");

	fprintf_s(f, "%e\t", time);

	//dumping data
	for (int i = 0; i < RESOLUTION; i++)
	{
		double depth = i * DELTA_X;
		if (depth < DISPLAY_DEPTH)
		{
			if (firstcolumn)
			{
				rowcount++;
			}
			fprintf_s(f, "%e\t", state[i]);
		}
	}
	firstcolumn = 0;
	fprintf_s(f, "\n");
	//closing file stream
	fclose(f);
}

void plotMultiState(const char* filename, const char* title)
{
	//generating system call string
	char cmd[1024];
	printf("%d\n", rowcount);
	sprintf_s(cmd, "python %s\\python\\plot3Dsurface.py %s %e %s \"%s\" %e %e %e %d", WDIR, WDIR, DELTA_X, filename, title, MIN_TEMP, MAX_TEMP, DISPLAY_DEPTH, rowcount);

	//running python script
	system(cmd);
}