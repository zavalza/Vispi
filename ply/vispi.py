import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import vispi_lex
import vispi_parse
import random
import string
# If a filename has been specified, we try to run it.
# If a runtime error occurs, we bail out and enter
# the other mode below
TypeMap = ['bool', 'int', 'float', 'string', 'Mat']
MemSectionMap = ['globals', 'constants', 'locals', 'temporals']
GPIO = [7, 11, 12, 13, 15, 16, 22] #GPIO pins of the RaspberryPi, we are using the physical number (header pin)
VarDict={}  #dictionary to find name using address
HwVars={}   #dictionary to find pins using names
LinfMap = []
LsupMap = []
MemBase = 0
MemLen = 0
VarNames = []

def resolveType(address):
    address = (address - MemBase) % MemLen #check just the offset
    for i in range(len(TypeMap)):
        if(address>=LinfMap[i] and address<=LsupMap[i]):
            return TypeMap[i]
    return 'void' #default

def resolveMemSection(address):
    section = (address - MemBase) / MemLen
    return MemSectionMap[section] 

def getRandomName():
    name = ''.join(random.choice(string.letters+string.digits) for i in xrange(5))
    while(name in VarNames):
        name = os.urandom(5)
    return name


if len(sys.argv) == 2:
    data = open(sys.argv[1]).read()
    prog = vispi_parse.parse(data)

    OBJ = open('vispi.obj', 'r')
    Name = OBJ.readline().splitlines()[0]
    CPP = open('%s.cpp' %(Name), 'w')
    CPP.write('#include "vispi.h"\n\nusing namespace std;\nusing namespace cv;\n\n')

    MemBase = int(OBJ.readline().splitlines()[0])
    MemLen = int(OBJ.readline().splitlines()[0])
    print MemBase
    print MemLen
    for i in range(5):
    	LinfMap.append(int(OBJ.readline().splitlines()[0]))

    for i in range(4):
    	LsupMap.append(LinfMap[i+1] - 1)

    LsupMap.append(MemLen - 1)

    print LinfMap
    print LsupMap

    OBJ.readline()	#reads the %%

    #Define constants and globals in cpp
    line = OBJ.readline().splitlines()[0]
    while line != '%%':
    	data = line.split(',')
        address = int(data[1])
        typeOfData = resolveType(address)
        name = " "
        if(resolveMemSection(address)=='globals'):
            name = data[0]
            CPP.write('%s %s;\n'%(typeOfData,name))
        elif(resolveMemSection(address)=='constants'):
            value = (data[0])
            name = getRandomName()
            CPP.write('%s %s = %s;\n'%(typeOfData,name,value))
        else:
            print "Error" #we are suppose to have only globals and constants in this section
        
        VarDict[address] = name  
    	print data
    	line = OBJ.readline().splitlines()[0]
    CPP.write('\n')
    print VarDict


    quadruples = []
    for line in OBJ:    #reads rest of the file
        quadruples.append(eval(line.splitlines()[0]))
    
    #print quadruples
    CPP.write('int main()\n{\n\twiringPiSetup(); //allow the use of wiringPi interface library\n\t');
    #how to print correctly the tabs?
    #interpret each quadruple to instructions in main of cpp
    for quadruple in quadruples:
        if(quadruple[0] == 'GOTO'):
            print "GOTO"
        if(quadruple[0] == 'CAM'):
            if(quadruple[1] == 'webcam'):
                CPP.write('VideoCapture cap(0); // open the default camera\nif(!cap.isOpened()) // check if we succeeded\nreturn -1;\n\n');
            else: #raspicam
                print"raspicam"
        if(quadruple[0] == 'INPUT'):
            pin = int(quadruple[3])
            if(pin in GPIO): #validate pin
                CPP.write('pullUpDnControl(%s, PUD_DOWN); //Enable PullUp Resistor connected to GND \n'%(pin))
                CPP.write('pinMode(%s, INPUT); \n'%(pin))
                HwVars[quadruple[1]]= pin
            else:
                print "Pin %s is not a valid GPIO pin"%(pin)
        if(quadruple[0] == 'OUTPUT'):
            pin = int(quadruple[3])
            if(pin in GPIO):
                CPP.write('pullUpDnControl(%s, PUD_OFF); //Disable PullUp Resistor\n'%(pin));
                CPP.write('pinMode(%s, OUTPUT); \n'%(pin))
                HwVars[quadruple[1]]= pin
            else:
                print "Pin %s is not a valid GPIO pin"%(pin)
        if(quadruple[0] == 'PWM'):
            pin = int(quadruple[3])
            if (pin == 12): #validate pin, with wiringPi only the GPIO1 can be used for PWM
                CPP.write('pullUpDnControl(%s, PUD_OFF); //Disable PullUp Resistor\n'%(pin))
                CPP.write('pinMode(%s, PWM_OUTPUT); \n'%(pin))
                HwVars[quadruple[1]]= pin
            else:
                print "Only pin #12 can be used as pwm"

    print HwVars


    #while line != '%%':        while not eof() ?

        # read the line and save it as it is in a list

        #line = OBJ.readline().splitlines()[0]
    
else:
    print 'Error: syntax is "python vispi.py <source code>"'