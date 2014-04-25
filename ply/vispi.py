import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import vispi_lex
import vispi_parse

# If a filename has been specified, we try to run it.
# If a runtime error occurs, we bail out and enter
# the other mode below
TypeMap = ['bool', 'int', 'float', 'string', 'image']
LinfMap = []
LsupMap = []
MemBase = 0
MemLen = 0

if len(sys.argv) == 2:
    data = open(sys.argv[1]).read()
    prog = vispi_parse.parse(data)

    OBJ = open('vispi.obj', 'r')
    Name = OBJ.readline().splitlines()[0]
    CPP = open('%s.cpp' %(Name), 'w')
    CPP.write('#include "vispi.h"\n\nusing namespace std;\nusing namespace cv;\n\n')

    MemBase = int(OBJ.readline().splitlines()[0])
    MemLen = int(OBJ.readline().splitlines()[0])
    for i in range(5):
    	LinfMap.append(int(OBJ.readline().splitlines()[0]))

    for i in range(4):
    	LsupMap.append(LinfMap[i+1] - 1)

    LsupMap.append(MemLen - 1)

    OBJ.readline()	#reads the %%

    line = OBJ.readline().splitlines()[0]
    while line != '%%':
    	data = line.split(',')
    	


    	line = OBJ.readline().splitlines()[0]

    line = OBJ.readline().splitlines()[0]
    #while line != '%%':        while not eof() ?

        # read the line and save it as it is in a list

        #line = OBJ.readline().splitlines()[0]
    
else:
    print 'Error: syntax is "python vispi.py <source code>"'