#include "vispi.h"

using namespace std;
using namespace cv;

const int ALMqH = 0;
const int dZaGH = 1;
int ledAmarillo;
const string dPVdg = "end";
const string hiaob = "d";
const string PICSP = "Suelta el boton One Shot";
const string VbnWQ = "Agrandar o dividir? (a/d)";
int boton;
const string ccBnE = "Dame el factor";
int ledRojo;
const string lPppa = "a";
const string aYJiC = "perfil.jpg";

VideoCapture Cam(0); // open the default camera
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
int factor;
string operacion;
Mat resultado;
Mat temp;
Mat im1;
Mat im2;
string entrada;
if((ALMqH==0) || (ALMqH==1)){
digitalWrite(4, ALMqH);
}
if((ALMqH==0) || (ALMqH==1)){
digitalWrite(3, ALMqH);
}
do {
temp = takePicture(Cam);
print(temp);
} while((digitalRead(6) == ALMqH));
while ((digitalRead(6) == dZaGH)) {
print(PICSP);
}
im1 = takePicture(Cam);
im2 = readImage(aYJiC);
temp = addImages(im1,im2);
while ((digitalRead(6) == ALMqH)) {
print(temp);
}
do {
print(VbnWQ);
operacion = readLine();
} while(((operacion != lPppa) && (operacion != hiaob)));
print(ccBnE);
factor = readNumber();
if ((operacion == lPppa)) {
resultado = resizeUp(im2,factor);
}
else {
resultado = resizeDown(im2,factor);
}
resultado = imGray(resultado);
do {
print(resultado);
entrada = readLine();
} while((entrada != dPVdg));

return 0;
}
