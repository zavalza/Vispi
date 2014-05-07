#include "vispi.h"

using namespace std;
using namespace cv;

const int LYIXx = 0;
const int LIxdK = 1;
const int XYvvk = 5;
const int BcRhD = 10;
int ledAmarillo;
const int UCLdj = 30;
int angle;
const int YhesO = 170;
int boton;
const int ACPWT = 90;
int ledRojo;

VideoCapture Cam(0); // open the default camera
Mat mueveDerecha () {
Mat der;
if((LIxdK==0) || (LIxdK==1)){
digitalWrite(4, LIxdK);
}
while ((angle < YhesO)) {
if(((angle + LIxdK)>23) && ((angle + LIxdK)<127)){
pwmWrite(1, (angle + LIxdK));
delay(20);
pwmWrite(1,0);
}
delay(XYvvk);
}
der = takePicture(Cam);
if((LYIXx==0) || (LYIXx==1)){
digitalWrite(4, LYIXx);
}

}

Mat mueveIzquierda () {
Mat izq;
if((LIxdK==0) || (LIxdK==1)){
digitalWrite(3, LIxdK);
}
while ((angle > UCLdj)) {
if(((angle - LIxdK)>23) && ((angle - LIxdK)<127)){
pwmWrite(1, (angle - LIxdK));
delay(20);
pwmWrite(1,0);
}
delay(XYvvk);
}
izq = takePicture(Cam);
if((LYIXx==0) || (LYIXx==1)){
digitalWrite(3, LYIXx);
}

}

int main () {

	wiringPiSetup(); //allow the use of wiringPi interface library
	if(!Cam.isOpened()) // check if we succeeded
	 return -1;

Cam.set(CV_CAP_PROP_FRAME_WIDTH, 320); 
Cam.set(CV_CAP_PROP_FRAME_HEIGHT, 240); 

pullUpDnControl(6, PUD_DOWN); //Enable PullUp Resistor connected to GND 
pinMode(6, INPUT); 
pullUpDnControl(3, PUD_OFF); //Disable PullUp Resistor
pinMode(3, OUTPUT); 
pullUpDnControl(4, PUD_OFF); //Disable PullUp Resistor
pinMode(4, OUTPUT); 
pullUpDnControl(1, PUD_OFF); //Disable PullUp Resistor
pinMode(1, PWM_OUTPUT); 
pwmSetMode(PWM_MODE_MS); 
pwmSetClock(400);
pwmSetRange(200);
Mat im1;
Mat im2;
Mat temp;
if((LYIXx==0) || (LYIXx==1)){
digitalWrite(4, LYIXx);
}
if((LYIXx==0) || (LYIXx==1)){
digitalWrite(3, LYIXx);
}
if((ACPWT>23) && (ACPWT<127)){
pwmWrite(1, ACPWT);
delay(20);
pwmWrite(1,0);
}
do {
temp = takePicture(Cam);
print(temp);
delay(BcRhD);
} while((digitalRead(6) == LYIXx));
im1 = mueveDerecha();
im2 = mueveIzquierda();
while ((digitalRead(6) == LYIXx)) {
print(addImages(im1,im2));
}

return 0;
}
