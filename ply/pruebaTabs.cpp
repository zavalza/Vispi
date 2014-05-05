#include "vispi.h"

using namespace std;
using namespace cv;

bool led1;
int UsVxR = 1;
bool led2;
int velocidad;
bool boton;
int x;
int EQsnx = 0;

int main () {

	wiringPiSetup(); //allow the use of wiringPi interface library
	VideoCapture cap(0); // open the default camera
if(!cap.isOpened()) // check if we succeeded
	return -1;

pullUpDnControl(22, PUD_DOWN); //Enable PullUp Resistor connected to GND 
pinMode(22, INPUT); 
pullUpDnControl(15, PUD_OFF); //Disable PullUp Resistor
pinMode(15, OUTPUT); 
pullUpDnControl(16, PUD_OFF); //Disable PullUp Resistor
pinMode(16, OUTPUT); 
pullUpDnControl(12, PUD_OFF); //Disable PullUp Resistor
pinMode(12, PWM_OUTPUT); 
x = UsVxR;
int y;
int x;
y = x;
while ((y > x)) {
y = EQsnx;
}

return 0;
}
