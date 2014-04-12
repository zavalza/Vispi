#include <stdio.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <map>

using namespace std;

int counterSections = 0;
map<int,string> memory;

void parse(string line){
	if(line=="%%")
    {
    	counterSections++;

    }
    else
    {
    	switch(counterSections)
	    {
	    	case 0: break;
	    	case 1: 
	    	{

	    	 int separator = line.find(',');
	  		//Guardar cada valor de acuerdo a su tipo? Ahora solo se guardan como strings
	    	 string value = line.substr(0, separator);
	    	 int address = atoi(line.substr(separator+1).c_str());
	    	 memory[address] = value;
	    	 //cout<<value<<endl;
	    	 //cout<<address<<endl;

	    	 break;
	    	}
	    	case 2: break;
	    	default:break;
	    } 
    }
    //cout<<line<<endl;
}


int main (int argc, char *argv[])
{
	ifstream objFile;
	string line;
    objFile.open("../ply/vispi.obj", ios::in);
    while(getline(objFile, line))
    {
    	parse(line);
    }
    cout<<"Cantidad de variables guardadas: "<<memory.size()<<endl;
    objFile.close();
	return 0;
}