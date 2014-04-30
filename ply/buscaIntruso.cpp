#include "vispi.h"

using namespace std;
using namespace cv;

bool led1;
int 1P3Nn = 1;
bool led2;
int Hy6KN = 4;
int M4DNX = 5;
int velocidad;
bool ivLkt = true;
string mensajeAlerta;
int KCcIb = 10;
float tsZaa = 1.2;
bool boton;
float aF2Bu = 45.0;
float DfOXG = 2.1;
int 1CfBu = 3;
int O0z7z = 20;
string yHfyT = "Alerta de intruso!";
int personas;
void main;
int comparaImagen;
Mat imgInicial;
int MyhJ3 = 85;

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
