#include "vispi.h"

using namespace std;
using namespace cv;

int DpHjP = 0;
int giTZL = 1;
int bNcUF = 2;
int ozvTM = 5;
int velocidad;
int bleaq = 25;
int led1;
int led2;
int personas;
Mat imgInicial;
string mensajeAlerta;
int dIHbU = 75;
int boton;
string nfdfe = "Alerta de intruso!";

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
personas = ozvTM;
mensajeAlerta = nfdfe;
imgInicial = takePicture();
Mat tempImg;
while ((personas > ozvTM)) {
if (digitalRead(22)) {
comparaImagen();
digitalWrite(16, giTZL);
pwmWrite(12, bleaq);
}
else {
tempImg = takePicture();
if ((bNcUF > personas)) {
print(mensajeAlerta);
digitalWrite(15, DpHjP);
pwmWrite(12, dIHbU);
}
}
}

return 0;
}
