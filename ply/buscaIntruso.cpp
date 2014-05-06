#include "vispi.h"

using namespace std;
using namespace cv;

int FsfRA = 0;
int atfrB = 1;
int BzWkF = 2;
int WUOQN = 5;
int velocidad;
int tSrYX = 25;
int led1;
int led2;
int personas;
Mat imgInicial;
string mensajeAlerta;
int GimcP = 75;
int boton;
string mOWnL = "Alerta de intruso!";

void comparaImagen (int i, float a) {
Mat tempImg;
Mat diferencias;
tempImg = takePicture();
diferencias = subImages(imgInicial,tempImg);
print(diferencias);

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
personas = WUOQN;
mensajeAlerta = mOWnL;
imgInicial = takePicture();
Mat tempImg;
while ((personas > WUOQN)) {
if (digitalRead(22)) {
comparaImagen();
digitalWrite(16, atfrB);
pwmWrite(12, tSrYX);
}
else {
tempImg = takePicture();
if ((BzWkF > personas)) {
print(mensajeAlerta);
digitalWrite(15, FsfRA);
pwmWrite(12, GimcP);
}
}

return 0;
}
