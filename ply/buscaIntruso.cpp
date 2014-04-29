#include "vispi.h"

using namespace std;
using namespace cv;

bool led1;
int UluJB = 1;
bool led2;
int EDHLt = 4;
int pfIIh = 5;
int velocidad;
bool EhRnm = true;
string mensajeAlerta;
int Dqw5v = 10;
float 6Y0Kj = 1.2;
bool boton;
float tdw6H = 45.0;
float ZX9fI = 2.1;
int 1tavt = 3;
int ofRPM = 20;
string U51nK = "Alerta de intruso!";
int personas;
Mat main;
int comparaImagen;
Mat imgInicial;
int n7DGC = 85;

int main()
{
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
