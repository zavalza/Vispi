#include <iostream>
#include <string>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
//#include <conio.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
// llenar con las librer'ias necesarias para openCV
using namespace cv;
using namespace std;

Mat takePicture(void);
Mat imBW(Mat);
Mat imLoad(string);
Mat imGray(Mat);
Mat resizeUp(Mat,int);
Mat resizeDown(Mat,int);
Mat filterColor(Mat, string); /*Incompleta*/
void print(Mat); /*Incompleta*/
void print(int);
void print(double);
void print(String);
void imDisplay(Mat);


Mat takePicture(void)
{
	Mat frame;
	VideoCapture inputCam(0);
	inputCam >> frame;
	return frame;
}

void imDisplay(Mat image)
{
	string name = "Image" + std::to_string(rand());
	namedWindow(name, CV_WINDOW_AUTOSIZE);
	imshow(name, image);
	waitKey(30);
}

Mat imLoad(String name)
{
	Mat image = imread(name, 1);
	if (!image.data){
		image = imread("Error.jpg");
	}
	return image;
}

void print(Mat image)
{
	cout << "Ancho: ";
	cout << image.cols;
	cout << " pixeles \n";
	cout << "Largo: ";
	cout << image.rows;
	cout << " pixeles \n";
	cout << "Dimensiones: ";
	cout << image.cols;
	cout << "x";
	cout << image.rows;
	cout << '\n';
	/*Pendiente el tamaño que ocupa la imagen*/

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