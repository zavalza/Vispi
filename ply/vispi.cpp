#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main () {

	ifstream Obj;
	Obj.open("vispi.obj", ifstream::in);

	while (!Obj.eof()) {
		string linea;
		getline(Obj, linea);
		cout << linea << endl;
	}

	Obj.close();

	return 0;
}