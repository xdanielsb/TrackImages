#include <opencv2/core/core.hpp>
#include <opencv2/core/mat.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/highgui/highgui_c.h>
#include <opencv2/imgproc.hpp>

#include <stdio.h>
#include <cstdlib>
#include <iostream>
#include <string>

#include "constants.hpp"
#include "util.hpp"

using namespace cv;
using namespace std;

/*
 * Variables
 */
int NUM_IMAGE = 0;
bool DEBUG = false;
bool TRACKING = false;
bool PAUSED = false;
int THRESH_VALUE = 50;

int displayOptions(Mat frame) {
	char filename[200];
	char key = (char) waitKey(30);

	if (key == 'q' || key == 'Q' || key == 27) {
		return 0;
	} else if (key == ' ') {
		sprintf(filename, "image%.3d.jpg", NUM_IMAGE++);
		imwrite(filename, frame);
		printf("Saved %c", filename);
		fflush(stdout);
	} else if (key == 'd' || key == 'D') {
		DEBUG = !DEBUG;
		printf(DEBUG ? "DEBUG Mode Enable\n" : "DEBUG Mode Disabled\n");
		fflush(stdout);
	} else if (key == 't' || key == 'T') {
		TRACKING = !TRACKING;
		printf(TRACKING ? "TRACKING Mode Enable\n" : "TRACKING Mode Disabled\n");
		fflush(stdout);
	} else if (key == 'p' || key == 'P') {
		PAUSED = !PAUSED;
		printf(PAUSED ? "The program is PAUSED\n" : "The program is running.\n");
		fflush(stdout);
	}

}

void showFrame(string WINDOW_NAME, Mat frame) {
	imshow(WINDOW_NAME, frame);
}

void Start() {

	VideoCapture capture(CAMERA_LAPTOP);

	if (!capture.isOpened()) {
		capture.open(CAMERA_LAPTOP);
	}

	if (!capture.isOpened()) {
		cerr << "Failed to open camera" << endl;
	}

	namedWindow(WINDOW_NAME, CV_WINDOW_KEEPRATIO);

	Mat frame1, frame2, grayImg, diffImg, threshImg;
	printf("%s", INSTRUCTIONS.c_str());
	fflush(stdout);
	for (;;) {
		capture.read(frame1);
		capture.read(frame2);

		toGray(frame1, grayImg);
		diff(frame2, frame1, diffImg);
		thresh(diffImg, threshImg, THRESH_VALUE);



		if (!PAUSED) {
			if (frame1.empty())
				break;
			showFrame(WINDOW_NAME, threshImg);
		}

		displayOptions(frame1);
	}

}
