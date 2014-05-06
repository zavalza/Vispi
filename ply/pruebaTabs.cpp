#include "vispi.h"

using namespace std;
using namespace cv;

int led1;
int hMiqH = 1;
int led2;
int IsBhd = 4;
int pGwtk = 5;
int velocidad;
string FQtee = "test.jpg";
int boton;
int YrWBM = 25;
int x;
int sakWQ = 0;

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
x = hMiqH;
Mat prueba1;
Mat superPrueba;
Mat prueba2;
int y;
int x;
Mat prueba3;
y = x;
digitalWrite(15, hMiqH);
digitalWrite(16, sakWQ);
pwmWrite(12, YrWBM);
while ((y > x)) {
prueba1 = takePicture();
prueba2 = imLoad(FQtee);
prueba3 = addImages(prueba1,prueba2);
superPrueba = subImages(resizeDown(resizeUp(prueba3,pGwtk),IsBhd),prueba1);
print(x);
print(superPrueba);
}

return 0;
}
