#include "vispi.h"

using namespace std;
using namespace cv;

const int mkWyg = 0;
const int sDDFJ = 1;
int ledAmarillo;
const string bHYvQ = "end";
const string oFjyx = "d";
const string sZXha = "Suelta el boton One Shot";
const string hRWgh = "Agrandar o dividir? (a/d)";
int boton;
const string YjegN = "Dame el factor";
int ledRojo;
const string qzwUp = "a";
const string MEVAn = "perfil.jpg";

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
if((mkWyg==0) || (mkWyg==1)){
digitalWrite(4, mkWyg);
}
if((mkWyg==0) || (mkWyg==1)){
digitalWrite(3, mkWyg);
}
do {
temp = takePicture(Cam);
print(temp);
} while((digitalRead(6) == mkWyg));
while ((digitalRead(6) == sDDFJ)) {
print(sZXha);
}
im1 = takePicture(Cam);
im2 = readImage(MEVAn);
temp = addImages(im1,im2);
while ((digitalRead(6) == mkWyg)) {
print(temp);
}
do {
print(hRWgh);
operacion = readLine();
} while(((operacion != qzwUp) && (operacion != oFjyx)));
print(YjegN);
factor = readNumber();
if ((operacion == qzwUp)) {
resultado = resizeUp(im2,factor);
}
else {
resultado = resizeDown(im2,factor);
}
resultado = imGray(resultado);
do {
print(resultado);
entrada = readLine();
} while((entrada != bHYvQ));

return 0;
}
