#include "vispi.h"

using namespace std;
using namespace cv;

int TCkTD = 0;
int AXSKw = 1;
int BWONR = 2;
int OyxUo = 5;
int velocidad;
int bQBPH = 25;
int led1;
int led2;
int personas;
Mat imgInicial;
string mensajeAlerta;
int kYEFJ = 75;
int boton;
string rXMtj = "Alerta de intruso!";

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

pullUpDnControl(6, PUD_DOWN); //Enable PullUp Resistor connected to GND 
pinMode(6, INPUT); 
pullUpDnControl(3, PUD_OFF); //Disable PullUp Resistor
pinMode(3, OUTPUT); 
pullUpDnControl(4, PUD_OFF); //Disable PullUp Resistor
pinMode(4, OUTPUT); 
pullUpDnControl(1, PUD_OFF); //Disable PullUp Resistor
pinMode(1, PWM_OUTPUT); 
personas = OyxUo;
mensajeAlerta = rXMtj;
imgInicial = takePicture();
Mat tempImg;
while ((personas > OyxUo)) {
if (digitalRead(6)) {
comparaImagen();
digitalWrite(4, AXSKw);
pwmWrite(1, bQBPH);
}
else {
tempImg = takePicture();
if ((BWONR > personas)) {
print(mensajeAlerta);
digitalWrite(3, TCkTD);
pwmWrite(1, kYEFJ);
}
}
}

return 0;
}
