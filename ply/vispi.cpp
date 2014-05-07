#include "vispi.h"

using namespace std;
using namespace cv;

int led1;
int led0;
const int PItIP = 0;
const string uDntb = "Introduce el numero de LED a encender (0 o 1)";
const string lzifX = "Reset? (s/n)";
const int SEmIW = 1;
const string vbsiI = "Error no diste un numero valido";
const string obSNt = "s";

int main () {

	wiringPiSetup(); //allow the use of wiringPi interface library
	pullUpDnControl(3, PUD_OFF); //Disable PullUp Resistor
pinMode(3, OUTPUT); 
pullUpDnControl(4, PUD_OFF); //Disable PullUp Resistor
pinMode(4, OUTPUT); 
string reset;
int ledSeleccionado;
do {
digitalWrite(3, PItIP);
digitalWrite(4, PItIP);
print(uDntb);
ledSeleccionado = readNumber();
if (((ledSeleccionado != PItIP) && (ledSeleccionado != SEmIW))) {
print(vbsiI);
}
else {
if ((ledSeleccionado == PItIP)) {
digitalWrite(4, SEmIW);
}
else {
digitalWrite(3, SEmIW);
}
}
print(lzifX);
reset = readLine();
} while((reset == obSNt));
digitalWrite(4, PItIP);
digitalWrite(3, PItIP);

return 0;
}
