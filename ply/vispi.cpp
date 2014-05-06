#include "vispi.h"

using namespace std;
using namespace cv;

int led1;
int a;
int led2;
int LmLrP = 1;
int KvOah = 5;
int AHNJS = 6;
Mat imgInicial;
string mensajeAlerta;
int button;
int GYBoP = 0;
string nsfKV = "Alerta de intruso!";
int personas;
int LePOe = 3;

int main () {

	wiringPiSetup(); //allow the use of wiringPi interface library
	//VideoCapture cap(0); // open the default camera
//if(!cap.isOpened()) // check if we succeeded
	//return -1;

pullUpDnControl(6, PUD_DOWN); //Enable PullUp Resistor connected to GND 
pinMode(6, INPUT); 
pullUpDnControl(3, PUD_OFF); //Disable PullUp Resistor
pinMode(3, OUTPUT); 
pullUpDnControl(4, PUD_OFF); //Disable PullUp Resistor
pinMode(4, OUTPUT); 
personas = KvOah;
mensajeAlerta = nsfKV;
int x;
Mat prueba;
print(mensajeAlerta);
digitalWrite(4, LmLrP);
while ((personas < AHNJS)) {
x = LePOe;
if (digitalRead(6)) {
digitalWrite(3, LmLrP);
digitalWrite(4, GYBoP);
}
}

return 0;
}
