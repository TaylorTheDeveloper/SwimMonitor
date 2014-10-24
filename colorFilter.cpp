#include <iostream>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"

using namespace cv;
using namespace std;

 int main( int argc, char** argv )
 {
    string filename = "MVI_7026_1.avi";// Make arv1, probably should
    //VideoCapture cam(0); //capture the video from web cam
	VideoCapture cam(filename);//Open File
    if ( !cam.isOpened() ) { // if not success, exit program
         cout << "Cannot open the web cam or file" << endl;
         return -1;
    }

    namedWindow("Control",CV_WINDOW_AUTOSIZE); //create a window called "Control"

	int lowH = 0;
	int highH = 105;//Hardcoded 

	int lowS = 95;//Hardcoded
	int highS = 255;

	int lowV = 0;
	int highV = 255;

	int sample = 0;//sample rate

	//Create trackbars in "Control" window
	cvCreateTrackbar("LowH", "Control", &lowH, 179); //Hue (0 - 179)
	cvCreateTrackbar("HighH", "Control", &highH, 179);

	cvCreateTrackbar("LowS", "Control", &lowS, 255); //Saturation (0 - 255)
	cvCreateTrackbar("HighS", "Control", &highS, 255);

	cvCreateTrackbar("LowV", "Control", &lowV, 255);//Value (0 - 255)
	cvCreateTrackbar("HighV", "Control", &highV, 255);


	cvCreateTrackbar("FrameSampler", "Control", &sample, 50);

    while (true)
    {
        Mat imgOriginal,imgHSV,imgMask,imgRes;
        //Mat imgResize;
        //Size size(100,100);
        //resize(imgOriginal,imgResize, size);

        //bool bSuccess = cam.read(imgOriginal); // read a new frame from video
        cam >> imgOriginal;

        if(imgOriginal.empty()){
            break;
		}

		cvtColor(imgOriginal, imgHSV, COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV
	
		inRange(imgHSV, Scalar(lowH, lowS, lowV), Scalar(highH, highS, highV), imgMask); //Threshold the image
      
		//morphological opening (removes small objects from the foreground)
		//Erode and Expand the edges of the mask to eliminate small artifacts
		erode(imgMask, imgMask, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) );
		dilate( imgMask, imgMask, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) ); 

		//morphological closing
		//Expand Mask and shrnk mask to smooth edges
		dilate( imgMask, imgMask, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) ); 
		erode(imgMask, imgMask, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)) );

		bitwise_and(imgOriginal,imgOriginal,imgRes,imgMask);

		imshow("Res",imgRes);

		// imshow("Mask", imgMask); //show the thresholded image
		// imshow("Original", imgOriginal); //show the original image

        if (waitKey(30) == 27){
            break; 
       }

    }

   return 0;
}