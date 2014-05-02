#include "vispi.h"

using namespace std;
using namespace cv;

bool led1;
int a;
int AJTbq = 2;
bool led2;
int HExrV = 5;
int velocidad;
int NJbyz = 1;
string mensajeAlerta;
bool boton;
string sKXAo = "Alerta de intruso!";
int personas;
Mat imgInicial;

personas = HExrV;
mensajeAlerta = sKXAo;
int factorial (int i) {
if ((i < AJTbq)) {
}
else {
}

}

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
int x;
x = factorial;

return 0;
}
