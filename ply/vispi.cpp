#include "vispi.h"

using namespace std;
using namespace cv;

int SKpeb = 0;
int zTDXn = 1;
int UPDRi = 3;

int factorial (int i) {
int result;
result = i;
i = (i - zTDXn);
while ((i > SKpeb)) {
result = (result * i);
i = (i - zTDXn);
return result;
}

}

int main () {

	wiringPiSetup(); //allow the use of wiringPi interface library
	int x;
x = factorial(UPDRi);

return 0;
}
