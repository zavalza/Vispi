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
TypeMap = ['bool', 'int', 'float', 'string', 'Mat', 'void']
MemSectionMap = ['globals', 'constants', 'locals', 'temporals']
GPIO = {7:7, 11:0, 12:1, 13:2, 15:3, 16:4, 22:6} #physical pins of the RaspberryPi mapped to GPIOpins
VarDict={}  #dictionary to find name of GLOBAL and CONSTANT variable using its address
GlobalAdd={} #dictionary to find GLOBAL and CONSTANT address using its name
HwVars = {} #dictionary to find pin number using names
HwModes={}   #dictionary to find hardware mode using names
ProcBegin={} #dictionary to map the begin of each proccedure, addresses are keys, modules are values
LocalVarName = {} #dictonary to fine name of LOCAL variable by address
procVars = {} #directory of procedures, as is in the parse file
TemporalMemory = {} #dictionary, returns values using a temporal address
Functions = {} #dictionary of Vispi Functions
#structure to find name of image functions according to operators and operands
#first operand is always image
imgOperand={'bool':0, 'int':1, 'float':2, 'string':3, 'Mat':4} #second operand
imgOperator={'+':0,'-':1,'/':2,'*':3,'%':4,'>':5,'<':6, '<=':7, '>=':8, '!=':9, '==':10, '&&':11, '||':12, '!':13}
imgFunctions= [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,'resizeDown','resizeUp',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['addImages','subImages',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #comparaciones entre image?
            ]
#############
LinfMap = []
LsupMap = []
MemBase = 0
MemLen = 0
VarNames = []
counterOfUserProcedures = 0
operatorAuxList = ['+','-','/','*','%','>','<','<=','>=','!=','==','&&','||']
GotoFList = []
paramString = ''
mainFileIsOpen = False

def resolveType(address):
    address = (address - MemBase) % MemLen #check just the offset
    for i in range(len(TypeMap)):
        if(address>=LinfMap[i] and address<=LsupMap[i]):
            return TypeMap[i]
    return 'void' #default

def resolveLocalAddr(type):
    return MemLen * 2 + MemBase + LinfMap[TypeMap.index(type)]

def resolveMemSection(address):
    section = (address - MemBase) / MemLen
    return MemSectionMap[section] 

def getRandomName():
    name = ''.join(random.choice(string.letters) for i in xrange(5))
    while(name in VarNames):
        name = os.urandom(5)
    return name


if len(sys.argv) == 2:
    data = open(sys.argv[1]).read()
    prog = vispi_parse.parse(data)

    OBJ = open('vispi.obj', 'r')
    Name = OBJ.readline().splitlines()[0]
    CPP = open('vispi.cpp', 'w')
    CPP.write('#include "vispi.h"\n\nusing namespace std;\nusing namespace cv;\n\n')
    MAIN = open('tempMain.cpp', 'w')
    mainFileIsOpen = True

    OBJ.readline()  #reads the %%
    Functions = eval(OBJ.readline().splitlines()[0])

    MemBase = int(OBJ.readline().splitlines()[0])
    MemLen = int(OBJ.readline().splitlines()[0])
    print MemBase
    print MemLen
    for i in range(6):
    	LinfMap.append(int(OBJ.readline().splitlines()[0]))

    for i in range(5):
    	LsupMap.append(LinfMap[i+1] - 1)

    LsupMap.append(MemLen - 1)

    print LinfMap
    print LsupMap
    procAdd= eval(OBJ.readline().splitlines()[0])
    addresses = procAdd.values()
    modules = procAdd.keys()
    for i in range(len(modules)):
        ProcBegin[addresses[i]]=modules[i]
    print ProcBegin

    procVars = eval(OBJ.readline().splitlines()[0])
    paramList = 0
    typeTable = 1
    addrTable = 2

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
            if (not procAdd.has_key(name)) and (not Functions.has_key(name)):
                CPP.write('%s %s;\n'%(typeOfData,name))
        elif(resolveMemSection(address)=='constants'):
            value = (data[0])
            name = getRandomName()
            CPP.write('%s %s = %s;\n'%(typeOfData,name,value))
        else:
            print "Error" #we are suppose to have only globals and constants in this section
        
        VarDict[address] = name
        GlobalAdd[name] = address
    	#print data
    	line = OBJ.readline().splitlines()[0]
    CPP.write('\n')
    print VarDict


    quadruples = []
    for line in OBJ:    #reads rest of the file
        quadruples.append(eval(line.splitlines()[0]))
    
    print quadruples
    MAIN.write('\n\twiringPiSetup(); //allow the use of wiringPi interface library\n\t');
    #how to print correctly the tabs?
    #interpret each quadruple to instructions in main of cpp
    for number, quadruple in enumerate(quadruples):

        if(ProcBegin.has_key(number)):
            if(ProcBegin[number] is not 'Vispi'): # if this is a user function
                global counterOfUserProcedures
                global LocalVarName
                LocalVarName = {} #RESET local variables
                #create the new module in CPP
                name = ProcBegin[number]
                listOfParameters = []

                if not counterOfUserProcedures == 0:
                    CPP.write('\n}\n\n')
                if name is 'main':
                    CPP.write('int %s (' %(name) )
                else:
                    CPP.write('%s %s (' %(procVars['Vispi'][typeTable][name],name) )

                addresses = procVars[name][addrTable].values()
                varnames = procVars[name][addrTable].keys()
                for i in range(len(addresses)):
                    LocalVarName[addresses[i]]=varnames[i]

                counterOfParametersOfEachType = {'bool':0, 'int':0, 'float':0, 'string':0, 'image':0}
                for n, parameterType in enumerate(procVars[name][paramList]):
                    x = counterOfParametersOfEachType[parameterType]
                    parameterName = LocalVarName[resolveLocalAddr(parameterType) + x]
                    listOfParameters.append(parameterName)
                    counterOfParametersOfEachType[parameterType] = x + 1

                    if n > 0:
                        CPP.write(', ')
                    if parameterType == 'image':
                        parameterType = 'Mat'
                    CPP.write('%s %s' %(parameterType, parameterName))
                
                CPP.write(') {\n')

                if (name is 'main'):
                    MAIN.close();
                    mainFileIsOpen = False
                    MAIN = open('tempMain.cpp', 'r')
                    CPP.write(MAIN.read())
                    MAIN.close();
                
                #Local variable declaration
                for i in range(len(addresses)):
                    ty = resolveType(addresses[i])
                    nm = varnames[i]
                    if nm not in listOfParameters and not resolveMemSection(addresses[i]) == 'temporals':
                        CPP.write('%s %s;\n' %(ty, nm))

                counterOfUserProcedures = counterOfUserProcedures + 1
            #################################################################################

        if(quadruple[0] == 'CAM'):
            if(quadruple[1] == 'webcam'):
                print "webcam"
                #MAIN.write('VideoCapture cap(0); // open the default camera\nif(!cap.isOpened()) // check if we succeeded\n\treturn -1;\n\n');
            else: #raspicam
                print"raspicam"
        if(quadruple[0] == 'INPUT'):
            pin = int(quadruple[3])
            if(GPIO.has_key(pin)): #validate pin
                name = quadruple[1]
                MAIN.write('pullUpDnControl(%s, PUD_DOWN); //Enable PullUp Resistor connected to GND \n'%(GPIO[pin]))
                MAIN.write('pinMode(%s, INPUT); \n'%(GPIO[pin]))
                HwModes[name]= 'input'
                HwVars[name] = pin
                address = GlobalAdd[name]
                VarDict[address] = 'digitalRead(%s)'%(GPIO[pin])
            else:
                raise TypeError("Pin %s is not a valid GPIO pin"%(pin))
        if(quadruple[0] == 'OUTPUT'):
            pin = int(quadruple[3])
            if(GPIO.has_key(pin)):
                name = quadruple[1]
                MAIN.write('pullUpDnControl(%s, PUD_OFF); //Disable PullUp Resistor\n'%(GPIO[pin]));
                MAIN.write('pinMode(%s, OUTPUT); \n'%(GPIO[pin]))
                HwModes[name]= 'output'
                HwVars[name] = pin
            else:
                raise TypeError("Pin %s is not a valid GPIO pin"%(pin))
        if(quadruple[0] == 'PWM'):
            pin = int(quadruple[3])
            if (pin == 12): #validate pin, with wiringPi only the GPIO1 can be used for PWM
                name = quadruple[1]
                MAIN.write('pullUpDnControl(%s, PUD_OFF); //Disable PullUp Resistor\n'%(GPIO[pin]))
                MAIN.write('pinMode(%s, PWM_OUTPUT); \n'%(GPIO[pin]))
                HwModes[name]= 'pwm'
                HwVars[name] = pin
            else:
                raise TypeError("Only pin #12 can be used as pwm")

        if(quadruple[0] is '='):
            origAdd = quadruple[1]
            destAdd = quadruple[3]
            origTyp = resolveType(origAdd)
            destTyp = resolveType(destAdd)
            origZone = resolveMemSection(origAdd)
            destZone = resolveMemSection(destAdd)

            # if origTyp is 'Mat' or destTyp is 'Mat':
            #     print 'x'                               # CODIGO DE MAT
            #else:
            if destZone is 'temporals' and origZone is 'temporals':
                TemporalMemory[destAdd] = TemporalMemory[origAdd]
            elif destZone is 'temporals' and (origZone is 'globals' or origZone is 'constants'):
                TemporalMemory[destAdd] = VarDict[origAdd]
                VarDict[origAdd] = VarDict[origAdd].split('(')[0]
            elif destZone is 'temporals' and origZone is 'locals':
                TemporalMemory[destAdd] = LocalVarName[origAdd]
            elif destZone is 'globals' and origZone is 'temporals':
                x = VarDict[destAdd]
                y = TemporalMemory[origAdd]
                if mainFileIsOpen:
                    if HwModes.has_key(x):
                        mode = HwModes[x]
                        pin = HwVars[x]
                        if mode is 'output':
                            MAIN.write('digitalWrite(%s, %s);\n' %(GPIO[pin], y))
                        elif mode is 'pwm':
                            MAIN.write('pwmWrite(%s, %s);\n' %(GPIO[pin], y))
                    else:
                        MAIN.write('%s = %s;\n' %(x, y))
                else:
                    if HwModes.has_key(x):
                        mode = HwModes[x]
                        pin = HwVars[x]
                        if mode is 'output':
                            CPP.write('digitalWrite(%s, %s);\n' %(GPIO[pin], y))
                        elif mode is 'pwm':
                            CPP.write('pwmWrite(%s, %s);\n' %(GPIO[pin], y))
                    else:
                        CPP.write('%s = %s;\n' %(x, y))
            elif destZone is 'globals' and (origZone is 'globals' or origZone is 'constants'):
                x = VarDict[destAdd]
                y = VarDict[origAdd]
                if mainFileIsOpen:
                    if HwModes.has_key(x):
                        mode = HwModes[x]
                        pin = HwVars[x]
                        if mode is 'output':
                            MAIN.write('digitalWrite(%s, %s);\n' %(GPIO[pin], y))
                        elif mode is 'pwm':
                            MAIN.write('pwmWrite(%s, %s);\n' %(GPIO[pin], y))
                    elif HwModes.has_key(y):
                        mode = HwModes[y]
                        if mode is not 'input':
                            raise TypeError("Reading with not input mode")
                    else:
                        MAIN.write('%s = %s;\n' %(x, y))
                else:
                    if HwModes.has_key(x):
                        mode = HwModes[x]
                        pin = HwVars[x]
                        if mode is 'output':
                            CPP.write('digitalWrite(%s, %s);\n' %(GPIO[pin], y))
                        elif mode is 'pwm':
                            CPP.write('pwmWrite(%s, %s);\n' %(GPIO[pin], y))
                    elif HwModes.has_key(y):
                        mode = HwModes[y]
                        if mode is not 'input':
                            raise TypeError("Reading with not input mode")
                    else:
                        CPP.write('%s = %s;\n' %(x, y))
            elif destZone is 'globals' and origZone is 'locals':
                x = VarDict[destAdd]
                y = LocalVarName[origAdd]
                if mainFileIsOpen:
                    if HwModes.has_key(x):
                        mode = HwModes[x]
                        pin = HwVars[x]
                        if mode is 'output':
                            MAIN.write('digitalWrite(%s, %s);\n' %(GPIO[pin], y))
                        elif mode is 'pwm':
                            MAIN.write('pwmWrite(%s, %s);\n' %(GPIO[pin], y))
                    else:
                        MAIN.write('%s = %s;\n' %(x, y))
                else:
                    if HwModes.has_key(x):
                        mode = HwModes[x]
                        pin = HwVars[x]
                        if mode is 'output':
                            CPP.write('digitalWrite(%s, %s);\n' %(GPIO[pin], y))
                        elif mode is 'pwm':
                            CPP.write('pwmWrite(%s, %s);\n' %(GPIO[pin], y))
                    else:
                        CPP.write('%s = %s;\n' %(x, y))
            elif destZone is 'locals' and origZone is 'temporals':
                x = LocalVarName[destAdd]
                y = TemporalMemory[origAdd]
                CPP.write('%s = %s;\n' %(x, y))
            elif destZone is 'locals' and (origZone is 'globals' or origZone is 'constants'):
                x = LocalVarName[destAdd]
                y = VarDict[origAdd]
                if HwModes.has_key(y):
                    mode = HwModes[y]
                    pin = HwVars[y]
                    if mode is not 'input':
                        raise TypeError("Reading with not input mode")
                CPP.write('%s = %s;\n' %(x, y))
            elif destZone is 'locals' and origZone is 'locals':
                x = LocalVarName[destAdd]
                y = LocalVarName[origAdd]
                CPP.write('%s = %s;\n' %(x, y))

        if(quadruple[0] in operatorAuxList):
            orig1Add = quadruple[1]
            orig2Add = quadruple[2]
            destAdd = quadruple[3]

            orig1Typ = resolveType(orig1Add)
            orig2Typ = resolveType(orig2Add)
            destTyp = resolveType(destAdd)

            orig1Zone = resolveMemSection(orig1Add)
            orig2Zone = resolveMemSection(orig2Add)
            destZone = resolveMemSection(destAdd)

            operator = quadruple[0]

            if orig1Zone is 'temporals':
                x = TemporalMemory[orig1Add]
            elif (orig1Zone is 'globals' or orig1Zone is 'constants'):
                x = VarDict[orig1Add]
                if HwModes.has_key(x):
                    raise TypeError("Mix of pins with arithmetic is not allowed")
            elif orig1Zone is 'locals':
                x = LocalVarName[orig1Add]

            if orig2Zone is 'temporals':
                y = TemporalMemory[orig2Add]
            elif (orig2Zone is 'globals' or orig2Zone is 'constants'):
                y = VarDict[orig2Add]
                if HwModes.has_key(y):
                    raise TypeError("Mix of pins with arithmetic is not allowed")
            elif orig2Zone is 'locals':
                y = LocalVarName[orig2Add]

            if orig1Typ is 'Mat': # specialImageFunctions
                functName = imgFunctions[imgOperand[orig2Typ]][imgOperator[operator]] 
                TemporalMemory[destAdd] = '%s(%s,%s)'%(functName,x,y)
            else:
                TemporalMemory[destAdd] = '(' + x + ' ' + operator + ' ' + y + ')'
        
        elif (quadruple[0] is '!'):
            orig1Add = quadruple[1]
            destAdd = quadruple[3]

            orig1Typ = resolveType(orig1Add)
            destTyp = resolveType(destAdd)

            orig1Zone = resolveMemSection(orig1Add)
            destZone = resolveMemSection(destAdd)

            operator = quadruple[0]

            if orig1Zone is 'temporals':
                x = TemporalMemory[orig1Add]
            elif (orig1Zone is 'globals' or orig1Zone is 'constants'):
                x = VarDict[orig1Add]
                if HwModes.has_key(x):
                    raise TypeError("Mix of pins with arithmetic is not allowed")
            elif orig1Zone is 'locals':
                x = LocalVarName[orig1Add]

            # NOT Mat is not accepted
            TemporalMemory[destAdd] = '(' + operator + x + ')'


        if (quadruple[0] is 'RETURN'):
            origAdd = quadruple[1]
            destAdd = quadruple[3]
            origTyp = resolveType(origAdd)
            destTyp = resolveType(destAdd)
            origZone = resolveMemSection(origAdd)
            destZone = resolveMemSection(destAdd)

            if origZone is 'temporals':
                CPP.write('return %s;\n' %(TemporalMemory[origAdd]))
            elif (origZone is 'globals' or origZone is 'constants'):
                CPP.write('return %s;\n' %(VarDict[origAdd]))
            elif origZone is 'locals':
                CPP.write('return %s;\n' %(LocalVarName[origAdd]))

        if (quadruple[0] is 'PARAM'):
            global paramString
            numberOfParam = quadruple[3]
            origAdd = quadruple[1]
            origZone = resolveMemSection(origAdd)

            if (numberOfParam is 0):
                if origZone is 'temporals':
                    paramString = TemporalMemory[origAdd]
                elif (origZone is 'globals' or origZone is 'constants'):
                    paramString = VarDict[origAdd]
                elif origZone is 'locals':
                    paramString = LocalVarName[origAdd]
            else:
                if origZone is 'temporals':
                    paramString += ', ' + TemporalMemory[origAdd]
                elif (origZone is 'globals' or origZone is 'constants'):
                    paramString += ', ' + VarDict[origAdd]
                elif origZone is 'locals':
                    paramString += ', ' + LocalVarName[origAdd]

        if (quadruple[0] is 'GOSUB'):
            global paramString
            quadNumber = quadruple[1]
            moduleName = ProcBegin[quadNumber]
            if procVars['Vispi'][typeTable][moduleName] is 'void':
                CPP.write('%s(%s);\n' %(moduleName, paramString))
            else:
                addrOfModuleGlobal = procVars['Vispi'][addrTable][moduleName]
                VarDict[addrOfModuleGlobal] += '(' + paramString + ')'
            paramString = ''

        if(quadruple[0] is 'CALL'):
            global paramString
            functName = quadruple[1]
            if procVars['Vispi'][typeTable][functName] is 'void':
                CPP.write('%s(%s);\n' %(functName, paramString))
            else:
                addrOfModuleGlobal = procVars['Vispi'][addrTable][functName]
                VarDict[addrOfModuleGlobal] += '(' + paramString + ')'
            paramString = ''
        # Leave the following quadruples at the end. More quadruples go above here /\

        if(quadruple[0] is 'GOTOF'):
            conditionAdd = quadruple[1]
            typeOfCondition = quadruple[2]
            GotoFList.append(quadruple[3])

            conditionZone = resolveMemSection(conditionAdd)

            if conditionZone is 'temporals':
                x = TemporalMemory[conditionAdd]
            elif (conditionZone is 'globals' or conditionZone is 'constants'):
                x = VarDict[conditionAdd]
            elif conditionZone is 'locals':
                x = LocalVarName[conditionAdd]

            CPP.write('%s (%s) {\n' %(typeOfCondition, x))

        if number + 1 in GotoFList:
            while True:
                CPP.write('}\n')
                GotoFList.remove(number + 1)
                if number + 1 not in GotoFList:
                    break
            
        if(quadruple[0] is 'GOTO'):
            typeOfCondition = quadruple[2]

            if typeOfCondition is 'else':
                CPP.write('else {\n')
                GotoFList.append(quadruple[3])

        if(quadruple[0] is 'DO') :
            CPP.write('do {\n')

        if(quadruple[0] is 'GOTOT'):
            conditionAdd = quadruple[1]
            conditionZone = resolveMemSection(conditionAdd)

            if conditionZone is 'temporals':
                x = TemporalMemory[conditionAdd]
            elif (conditionZone is 'globals' or conditionZone is 'constants'):
                x = VarDict[conditionAdd]
            elif conditionZone is 'locals':
                x = LocalVarName[conditionAdd]

            CPP.write('} while(%s);\n' %(x))

    # Quadruples have ended
        #insert MAIN
    CPP.write('\nreturn 0;\n}\n')
    CPP.close()


    #while line != '%%':        while not eof() ?

        # read the line and save it as it is in a list

        #line = OBJ.readline().splitlines()[0]
    
else:
    print 'Error: syntax is "python vispi.py <source code>"'