#include <iostream>
#include <string>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
using namespace cv;
using namespace std;

float readNumber();
string readLine();
Mat readImage(string);
Mat takePicture(VideoCapture inputCam);
Mat imBW(Mat);
Mat imGray(Mat);
Mat resizeUp(Mat,int);
Mat resizeDown(Mat,int);
Mat filterColor(Mat, string); /*Incompleta*/
Mat addImage(Mat, Mat);
Mat subImage(Mat, Mat);
Mat removeBackground(Mat);
bool findLight(Mat);
void showInfo(Mat);
void print(Mat);
void print(int);
void print(double);
void print(String);
void delay(int);

float readNumber()
{
	float value = 0;
	cin>>value;
	return value;
}

string readLine()
{
	string value;
	cin>>value;
	return value;
}

Mat readImage(String name)
{
	Mat image = imread(name, 1);
	if (!image.data){
		image = imread("Error.jpg");
	}
	return image;
}

Mat takePicture(VideoCapture inputCam)
{
	Mat frame;
	inputCam >> frame;
	return frame;
}


void showInfo(Mat image)
{
	cout << "Ancho: ";
	cout << image.cols;
	cout << " pixeles \n";
	cout << "Largo: ";
	cout << image.rows;
	cout << " pixeles \n";
}

void print(Mat image)
{
	string name = "Image";
	namedWindow(name, CV_WINDOW_AUTOSIZE);
	imshow(name, image);
	waitKey(30);
}

void print(int num)
{
	cout << num;
	cout << '\n';
}

void print(double num)
{
	cout << num;
	cout << '\n';
}

void print(bool var)
{
	cout << var;
	cout << '\n';
}

void print(string name)
{
	cout << name + '\n';
}

Mat imBW(Mat image)
{
	Mat newImage, imageBin, channel[3];
	cvtColor(image, newImage, CV_BGR2YCrCb);
	split(newImage, channel);
	threshold(channel[0], imageBin, 150, 255, CV_THRESH_BINARY);
	return imageBin;
}

Mat imGray(Mat image)
{
	Mat grayImage;
	cvtColor(image, grayImage, CV_RGB2GRAY);
	return grayImage;
}

Mat resizeUp(Mat image, int num)
{
	Mat imageUp;
	resize(image, imageUp, Size(image.cols*num, image.rows*num), 0, 0, INTER_CUBIC);
	return imageUp;
}

Mat resizeDown(Mat image, int num)
{
	Mat imageDown;
	resize(image, imageDown, Size(image.cols/num, image.rows/num), 0, 0, INTER_CUBIC);
	return imageDown;
}

Mat filterColor(Mat image, string color)
{
	int iLowH, iLowS, iLowV;
	int iHighH, iHighS, iHighV;
	int k = color.length();
	unsigned char Error = 0;
	Mat imgHSV, imgThresholded, imgBGR;

	for (; k != 0; k--)
	{
		color[k - 1] = tolower(color[k - 1]);
	}

	if (!color.compare("red")){
		iLowH = 160;
		iHighH = 179;
	}
	else if (!color.compare("green")){
		iLowH = 38;
		iHighH = 75;
	}
	else if (!color.compare("blue")){
		iLowH = 75;
		iHighH = 130;
	}
	else if (!color.compare("orange")){
		iLowH = 0;
		iHighH = 22;
	}
	else if (!color.compare("yellow")){
		iLowH = 22;
		iHighH = 38;
	}
	else if (!color.compare("violet")){
		iLowH = 130;
		iHighH = 160;
	}
	else {
		cout << "Color not supported by this function.";
		Error == 1;
	}

	cvtColor(image, imgHSV, COLOR_BGR2HSV);
	inRange(imgHSV, Scalar(iLowH, iLowS, iLowV), Scalar(iHighH, iHighS, iHighV), imgThresholded);

	erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
	dilate(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
	dilate(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
	erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
	
	cvtColor(imgThresholded, imgBGR, COLOR_HSV2BGR);
	return imgBGR;
}

Mat addImage(Mat image1, Mat image2)
{
	Mat result;
	if(image1.cols > image2.cols) || (image1.rows > image2.rows)
	{
		resize(image1, image1, Size(image2.cols, image2.rows), 0, 0, INTER_CUBIC);
	}
	else if(image2.cols > image1.cols) || (image2.rows > image1.rows)
	{
		resize(image2, image2, Size(image1.cols, image1.rows), 0, 0, INTER_CUBIC);
	}
	addWeighted(image1, 0.5, image2, 0.5, 0.0,result);

	return result;
}

Mat subImage(Mat, Mat)
{
	Mat result;
	if(image1.cols > image2.cols) || (image1.rows > image2.rows)
	{
		resize(image1, image1, Size(image2.cols, image2.rows), 0, 0, INTER_CUBIC);
	}
	else if(image2.cols > image1.cols) || (image2.rows > image1.rows)
	{
		resize(image2, image2, Size(image1.cols, image1.rows), 0, 0, INTER_CUBIC);
	}

	return result;

}

Mat removeBackground(Mat image)
{
	Mat fgMaskMOG; 
	Ptr< BackgroundSubtractor> pMOG; //MOG Background subtractor  
	pMOG = new BackgroundSubtractorMOG();  

	pMOG->apply(image, fgMaskMOG);
	return fgMaskMOG;

}

void delay(int ms)
{
	delay(ms);
}

void showInfo(Mat image)
{
	cout<<"Buenfil haz tu trabajo"<<endl;
}