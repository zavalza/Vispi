from ply import *
from stack import Stack
import vispi_lex
tokens = vispi_lex.tokens
counterTabs = 0
expectedTabulation=0
#Semantic cube
# order: type, type, operator
#   type order: <NULL>, bool, int, float, string, image, -1 means error
#       NULL operand is only valid on the first operand
#       -1 is only valid as a result
#   operator order: + - / * % > < <= >= != == && || ! 
semIndex1={'<NULL>':0, 'bool':1, 'int':2, 'float':3, 'string':4, 'image':5}
semIndex2={'bool':0, 'int':1, 'float':2, 'string':3, 'image':4}
semIndex3={'+':0,'-':1,'/':2,'*':3,'%':4,'>':5,'<':6, '<=':7, '>=':8, '!=':9, '==':10, '&&':11, '||':12, '!':13}
SemCube = [
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,'bool'],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,'image']
        ],
        [
            [-1,-1,-1,-1,-1,'bool','bool','bool','bool','bool','bool','bool','bool',-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['int','int','int','int','int','bool','bool','bool','bool','bool','bool',-1,-1,-1],
            ['float','float','float','float',-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['float','float','float','float',-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            ['float','float','float','float',-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['string',-1,-1,-1,-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,'image','image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,'image','image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['image','image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] #comparaciones entre image?
        ]
    ]

ValidAssign = {'bool':['bool'], 
                'int':['int','float'],
                'float':['int','float'],
                'string':['string'],
                'image':['image']}


#MACROS
paramList = 0
typeTable = 1
addrTable = 2

#Virtual Memory segment definitions
S_len = 1000

DS_base = 0                #globales
CS_base = DS_base + S_len  #constantes
SS_base = CS_base + S_len  #locales
ES_base = SS_base + S_len  #temporales

S_offsetTable = {'bool' : 0, 'int' : 200, 'float' : 400, 'string' : 600, 'image' : 800, 'void': 900}

#variable counters
DS_counterTable = {'bool' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0, 'void': 0}
CS_counterTable = {'bool' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0, 'void': 0}
SS_counterTable = {'bool' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0, 'void': 0}
ES_counterTable = {'bool' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0, 'void': 0}


#data structures
ProcTypes = {'Vispi':'prog'}
ProcSize = {'Vispi':[0,0,0,0,0,0,0,0,0,0]} #primero variables loc. y luego temporales
ProcAddr = {'Vispi':0}
        # parameter list, {variable types dict}, {variable address dict}
ProcVars = {'Vispi':[[],{},{}]}

#variables
moduleName = 'Vispi'
typeOfData = 'VOID' #Used to store the last type detected

#quadruples
fileQuadruples = open('vispi.obj', 'w')
programName = ''
counterQuadruples = 0
Quadruples={}
branchStack = Stack()
operatorsStack = Stack()
operandsStack = Stack()
typesStack = Stack()
isCondition = False
typeOfCondition = ""
isDoWhile = False
counterParam = 0
functName = ''
functType = ''
isAssign = False
#temporal variables
counterTemporals = 0
#constantes con contador para memoria

#Grammatic rules
def p_program(p):
    'program : programName hardware vars assign functions'
    global counterQuadruples
    Quadruples[counterQuadruples] = ['ENDPROC', -1, -1, -1]
    counterQuadruples += 1

    if ProcTypes.has_key('main'):
        print "programa exitoso"
        print ProcTypes
        print '\n'
        print ProcSize
        print '\n'
        print ProcAddr
        print '\n'
        print ProcVars
        print '\n'
        #print SemCube
        print '\n'
        print Quadruples
        print '\n'
        print 'operatorsStack'
        print operatorsStack
        print '\n'
        print 'operandsStack'
        print operandsStack
        print '\n'
        print 'typesStack'
        print typesStack
        print '\n'
        print 'branchStack'
        print branchStack
        print '\n'

        #guardar en archivo:
        #   Dir. de Procs //no
        #   %%
        #   Constantes (addr, tipo y valor)
        #   %%
        #   Cuadruplos
        fileQuadruples.write("%s\n" %(programName))
        fileQuadruples.write("%d\n" %(DS_base))
        fileQuadruples.write("%d\n" %(S_len))
        fileQuadruples.write("%d\n" %(S_offsetTable['bool']))
        fileQuadruples.write("%d\n" %(S_offsetTable['int']))
        fileQuadruples.write("%d\n" %(S_offsetTable['float']))
        fileQuadruples.write("%d\n" %(S_offsetTable['string']))
        fileQuadruples.write("%d\n" %(S_offsetTable['image']))
        fileQuadruples.write("%d\n" %(S_offsetTable['void']))
        fileQuadruples.write("%s\n" %(ProcAddr))
        fileQuadruples.write("%s\n" %(ProcVars))

        fileQuadruples.write("%%\n")
        
        keys = ProcVars['Vispi'][addrTable].keys()
        values = ProcVars['Vispi'][addrTable].values()
        for i in range(len(keys)):
            fileQuadruples.write("%s,%s\n" %(keys[i], values[i]))

        fileQuadruples.write("%%\n")

        for i in range(counterQuadruples):
            line = str(Quadruples[i])
            #line = line.replace('[','{')
            #line = line.replace(']','}')
            #line = line.replace("'",'"')
            fileQuadruples.write("%s\n" %line)
        fileQuadruples.close()

    else:
        raise TypeError("'main' module was not defined")
def p_programName(p):
    'programName : PROGRAM ID NEWLINE'
    global counterQuadruples
    global programName
    Quadruples[counterQuadruples]=["GOTO", -1, 'main', -1]
    #branchStack.push(counterQuadruples)
    counterQuadruples+=1
    programName = p[2]

def p_empty(p):
    'empty :'
    pass

def p_hardware(p):
	'hardware : camDeclaration inputsDeclaration outputsDeclaration pwmDeclaration'

def p_camDeclaration(p):
    '''camDeclaration : empty
				      | CAM WEBCAM COLON ID NEWLINE
                      | CAM PICAM COLON ID NEWLINE'''
    global counterQuadruples
    if(len(p)>2):
        Quadruples[counterQuadruples]=["CAM", p[2], -1, -1]
        counterQuadruples+=1

def p_inputsDeclaration(p):
    '''inputsDeclaration : empty
					     | INPUT f_saveType pinList NEWLINE'''
    global counterQuadruples
    while(not operandsStack.isEmpty()):
        Quadruples[counterQuadruples]=[p[1], operandsStack.pop(), -1, operandsStack.pop()]
        counterQuadruples+=1

def p_ouputsDeclaration(p):
    '''outputsDeclaration : empty
					      | OUTPUT f_saveType pinList NEWLINE'''
    global counterQuadruples
    while(not operandsStack.isEmpty()):
        Quadruples[counterQuadruples]=[p[1], operandsStack.pop(), -1, operandsStack.pop()]
        counterQuadruples+=1

def p_pwmDeclaration(p):
    '''pwmDeclaration : empty
				      | PWM f_saveType pinList NEWLINE'''
    global counterQuadruples
    while(not operandsStack.isEmpty()):
        Quadruples[counterQuadruples]=[p[1], operandsStack.pop(), -1, operandsStack.pop()]
        counterQuadruples+=1

def p_pinList(p):
    '''pinList : C_INT COLON ID
               | C_INT COLON ID COMMA pinList'''
    ProcVars['Vispi'][typeTable][p[3]] = typeOfData
    ProcVars['Vispi'][addrTable][p[3]] = DS_base + S_offsetTable[typeOfData] + DS_counterTable[typeOfData]
    DS_counterTable[typeOfData] += 1 # falta validar que no nos pasemos del tamanio del segmento
    operandsStack.push(p[1])
    operandsStack.push(p[3])


def p_vars(p):
    '''vars : f_checkTab tipo idList NEWLINE f_resetTab vars
            | empty'''

def p_f_saveType(p):
    'f_saveType :'
    global typeOfData
    if((p[-1]=='INPUT')or(p[-1]=='OUTPUT')):
        typeOfData = 'bool'
    else:
        if(p[-1]=='PWM'):
            typeOfData = 'int'
        else:
            typeOfData = p[-1]


def p_idList(p):
    '''idList : ID
              | ID COMMA idList'''
    if ProcVars.has_key(moduleName): #falta validar si ya existe el ID
        ProcVars[moduleName][typeTable][p[1]] = typeOfData
        if moduleName == 'Vispi':
            ProcVars[moduleName][addrTable][p[1]] = DS_base + S_offsetTable[typeOfData] + DS_counterTable[typeOfData]
            DS_counterTable[typeOfData] += 1
        else:
            ProcVars[moduleName][addrTable][p[1]] = SS_base + S_offsetTable[typeOfData] + SS_counterTable[typeOfData]
            SS_counterTable[typeOfData] += 1 # falta validar que no nos pasemos del tamanio del segmento
    else:
        raise TypeError("'%s' module is not defined" %(moduleName))

def p_tipo(p):
    '''tipo : BOOL f_saveType
            | INT  f_saveType
            | FLOAT f_saveType
            | STRING f_saveType
            | IMAGE f_saveType'''

def p_functions(p):
    '''functions : DEF tipo ID f_saveModule LPAREN RPAREN COLON NEWLINE f_resetTab f_incTab block f_endModule functions
                 | DEF tipo ID f_saveModule LPAREN tipo ID f_addToParam parameterList RPAREN COLON NEWLINE f_resetTab f_incTab block f_endModule functions
                 | DEF VOID f_setVoid ID f_saveModule LPAREN RPAREN COLON NEWLINE f_resetTab f_incTab block f_endModule functions
                 | DEF VOID f_setVoid ID f_saveModule LPAREN tipo ID f_addToParam parameterList RPAREN COLON NEWLINE f_resetTab f_incTab block f_endModule functions
                 | DEF VOID f_setVoid MAIN f_saveModule LPAREN RPAREN COLON NEWLINE f_resetTab f_incTab block f_endModule functions
                 | DEF VOID f_setVoid MAIN f_saveModule LPAREN tipo ID f_addToParam parameterList RPAREN COLON NEWLINE f_resetTab f_incTab block f_endModule functions
                 | empty'''

def p_f_setVoid(p):
    'f_setVoid : '
    global typeOfData
    typeOfData = 'void'

def p_f_endModule(p):
    'f_endModule : '
    global counterQuadruples

    ProcSize[moduleName] = [
        SS_counterTable['bool'],
        SS_counterTable['int'],
        SS_counterTable['float'],
        SS_counterTable['string'],
        SS_counterTable['image'],
        ES_counterTable['bool'],
        ES_counterTable['int'],
        ES_counterTable['float'],
        ES_counterTable['string'],
        ES_counterTable['image']
    ]
    SS_counterTable['bool'] = SS_counterTable['int'] = SS_counterTable['float'] = SS_counterTable['string'] = SS_counterTable['image'] = 0
    ES_counterTable['bool'] = ES_counterTable['int'] = ES_counterTable['float'] = ES_counterTable['string'] = ES_counterTable['image'] = 0

    Quadruples[counterQuadruples] = ['RET', -1, -1, -1]
    counterQuadruples += 1

def p_f_saveModule(p):
    'f_saveModule :'
    global moduleName
    moduleName = p[-1]
    if ProcTypes.has_key(moduleName):
        raise TypeError("'%s' is already defined" %(moduleName))
    else:
        ProcTypes[moduleName] = typeOfData
        ProcSize[moduleName] = [0,0,0,0,0,0,0,0,0,0]
        ProcAddr[moduleName] = counterQuadruples
        ProcVars[moduleName] = [[],{},{}]
        if not ProcVars['Vispi'][addrTable].has_key(moduleName):
            ProcVars['Vispi'][typeTable][moduleName] = typeOfData
            ProcVars['Vispi'][addrTable][moduleName] = DS_base + S_offsetTable[typeOfData] + DS_counterTable[typeOfData]
            DS_counterTable[typeOfData] += 1
        else:
            raise TypeError('Function name is the same as global variable')

def p_parameterList(p):
    '''parameterList : empty
                     | COMMA tipo ID f_addToParam parameterList'''

def p_f_addToParam(p):
    'f_addToParam :'
    ProcVars[moduleName][typeTable][p[-1]] = typeOfData
    ProcVars[moduleName][addrTable][p[-1]] = SS_base + S_offsetTable[typeOfData] + SS_counterTable[typeOfData]
    SS_counterTable[typeOfData] += 1 # falta validar que no nos pasemos del tamanio del segmento
    ProcVars[moduleName][paramList].append(typeOfData)


def p_assign(p):
    '''assign : f_checkTab ID f_checkID EQUAL f_isAssign expression NEWLINE f_resetTab f_generateEqual assign
              | empty'''
    global isAssign
    isAssign = False
    #f_checkTab ID f_checkID EQUAL f_isAssign expression assign NEWLINE f_resetTab f_generateEqual
    #f_checkTab ID f_checkID EQUAL f_moreIDs f_isAssign expression NEWLINE f_resetTab f_generateEqual assign

#def p_f_moreIDs(p):
#    '''f_moreIDs : empty
#                | ID f_checkID EQUAL'''

def p_f_isAssign(p):
    'f_isAssign : '
    global isAssign 
    isAssign = True

def p_f_generateEqual(p):
    'f_generateEqual :'
    global counterQuadruples
    #Sacar dos operandos y validarlos
    operand2 = operandsStack.pop()
    operand1 = operandsStack.pop()
    type2 = typesStack.pop()
    type1 = typesStack.pop()
    if type2 in ValidAssign[type1]:
        Quadruples[counterQuadruples]=['=', operand2, -1, operand1]
        counterQuadruples+=1
    else:
        raise TypeError("Invalid types in assignment")

def p_f_checkID(p):
    'f_checkID : '
    if not ProcVars[moduleName][typeTable].has_key(p[-1]):
        if not ProcVars['Vispi'][typeTable].has_key(p[-1]):
            raise TypeError("variable '%s' not declared" %(p[-1]))
        else: 
            operandsStack.push(ProcVars['Vispi'][addrTable][p[-1]])
            typesStack.push(ProcVars['Vispi'][typeTable][p[-1]])
    else:
        operandsStack.push(ProcVars[moduleName][addrTable][p[-1]])
        typesStack.push(ProcVars[moduleName][typeTable][p[-1]])
# def p_main(p):
#     '''main : DEF VOID MAIN f_saveModule LPAREN RPAREN COLON NEWLINE block 
# 			| DEF VOID MAIN f_saveModule LPAREN tipo ID f_addToParam parameterList RPAREN COLON NEWLINE block'''

def p_block(p):
    '''block : empty
             | TAB f_addTab moreTabs statement moreStatements'''
    global expectedTabulation 
    global counterTabs
    expectedTabulation-=1
    counterTabs = 0

def p_moreStatements(p):
    '''moreStatements : empty
                      | TAB f_addTab moreTabs statement moreStatements'''

def p_moreTabs(p):
    '''moreTabs : empty
                    | TAB f_addTab moreTabs
                    | NEWLINE f_resetTab TAB f_addTab moreTabs'''

def p_f_incTab(p):
    'f_incTab : '
    global expectedTabulation
    expectedTabulation +=1

def p_f_addTab(p):
    'f_addTab : '
    global counterTabs
    counterTabs +=1
    if(counterTabs>expectedTabulation):
        print counterTabs
        print expectedTabulation
        raise TypeError("Unexpected indent")

def p_f_resetTab(p):
    'f_resetTab : '
    global counterTabs
    counterTabs = 0

def p_f_checkTab(p):
    'f_checkTab : '
    if(counterTabs < expectedTabulation):
        print counterTabs
        print expectedTabulation
        raise TypeError("Identation error")


def p_statement(p):
    '''statement : vars 
                 | assign
                 | f_checkTab condition
                 | f_checkTab cycle
                 | f_checkTab doCycle
                 | f_checkTab funct NEWLINE f_resetTab
                 | f_checkTab RETURN expression f_return NEWLINE f_resetTab'''

def p_f_return(p):
    'f_return : '
    global counterQuadruples

    if ProcTypes[moduleName]=='void':
        raise TypeError("Unexpected return in void function")

    retVal = operandsStack.pop() # hay que sacar tipo y valor del stack al final de un proc?
    typ = typesStack.pop()
    globalAddr = ProcVars['Vispi'][addrTable][moduleName]
    globalType = ProcVars['Vispi'][typeTable][moduleName]
    if typ == globalType:
        Quadruples[counterQuadruples] = ['RETURN', retVal, -1, globalAddr]
        counterQuadruples += 1
    else:
        raise TypeError("Type missmatch: function return value")
    operandsStack.push(retVal)      ###########   Not sure if
    typesStack.push(typ)            ###########   fixed the return problem

def p_condition(p):
    '''condition : IF f_isCondition expression COLON NEWLINE f_resetTab f_incTab block
                 | IF f_isCondition expression COLON NEWLINE f_resetTab f_incTab block ELSE f_popIf COLON NEWLINE f_resetTab f_incTab block'''
    end = branchStack.pop()
    Quadruples[end][3]=counterQuadruples

def p_cycle(p):
    'cycle : WHILE f_isCondition expression COLON NEWLINE f_resetTab f_incTab block'
    global counterQuadruples
    end = branchStack.pop()
    condition = branchStack.pop()
    Quadruples[counterQuadruples]=['GOTO', -1, 'while', condition]
    counterQuadruples+=1
    Quadruples[end][3]=counterQuadruples

def p_doCycle(p):
    'doCycle : DO f_pushDo COLON NEWLINE f_resetTab f_incTab block WHILE f_isDoWhile f_isCondition expression NEWLINE f_resetTab'

def p_f_popIf(p):
    'f_popIf : '
    global counterQuadruples
    Quadruples[counterQuadruples] = ['GOTO', -1, 'else', -1]
    counterQuadruples+=1
    endFalse = branchStack.pop()
    Quadruples[endFalse][3]=counterQuadruples
    branchStack.push(counterQuadruples-1)

def p_f_pushDo(p):
    'f_pushDo : '
    global counterQuadruples
    branchStack.push(counterQuadruples)
    Quadruples[counterQuadruples] = ['DO', -1, -1, -1]
    counterQuadruples += 1

def p_f_isDoWhile(p):
    'f_isDoWhile : '
    global isDoWhile
    global typeOfCondition
    isDoWhile=True
    typeOfCondition = 'do'

def p_f_isCondition(p):
    'f_isCondition : '
    global isCondition
    global typeOfCondition
    global isDoWhile
    isCondition = True
    if(not isDoWhile):
        typeOfCondition = p[-1]
        if(typeOfCondition == 'while'):
            branchStack.push(counterQuadruples)
    isDoWhile=False ################################################ not sure
    #print typeOfCondition

def p_funct(p):
    '''funct : ID f_checkProc LPAREN RPAREN
             | ID f_checkProc LPAREN expression f_genParam expressionList RPAREN'''
    global counterQuadruples
    global counterTemporals


    Quadruples[counterQuadruples] = ['GOSUB', ProcAddr[functName], -1, -1]
    counterQuadruples += 1

    if (not functType == 'void') and isAssign:
        globalAddr = ProcVars['Vispi'][addrTable][functName]
        temporalVariable = "Temporal%s" %counterTemporals
        if not ProcVars[moduleName][addrTable].has_key(temporalVariable):
            ProcVars[moduleName][typeTable][temporalVariable] = functType
            ProcVars[moduleName][addrTable][temporalVariable] = ES_base + S_offsetTable[functType] + ES_counterTable[functType]
            ES_counterTable[functType] += 1
        temporalAddress=ProcVars[moduleName][addrTable][temporalVariable]
        operandsStack.push(temporalAddress)
        typesStack.push(functType)
        Quadruples[counterQuadruples] = ['=', globalAddr, -1, temporalAddress]
        counterTemporals+=1
        counterQuadruples+=1
        print operandsStack
        

def p_f_checkProc(p):
    'f_checkProc : '
    global counterQuadruples
    global counterParam
    global functName
    global functType

    functName = p[-1]
    if not ProcVars.has_key(functName):
        raise TypeError("Function not declared")

    functType = ProcTypes[functName]
    Quadruples[counterQuadruples] = ['ERA', ProcSize[functName], -1, -1]
    counterQuadruples += 1

    counterParam = 0

def p_expressionList(p):
    '''expressionList : empty
                      | COMMA expression f_genParam expressionList'''
    paramList = ProcVars[functName][0]  #traemos la lista de parametros del proc.
    if not len(paramList) == counterParam:
        raise TypeError("Invalid number of parameters")

def p_f_genParam(p):
    'f_genParam : '
    global counterParam
    global counterQuadruples

    arg = operandsStack.pop()
    typ = typesStack.pop()

    paramList = ProcVars[functName][0]  #traemos la lista de parametros del proc.
    if not typ == paramList[counterParam]:
        raise TypeError("Type mismatch on function call")
    else:
        #counterParam empieza en 0: primer parametro es param0
        Quadruples[counterQuadruples] = ['PARAM', arg, -1, counterParam]
        counterParam += 1
        counterQuadruples += 1

def p_expression(p):
    '''expression : exp
                  | exp compareToken exp f_popComparation'''

def p_f_popComparation(p):
    'f_popComparation : '
    global counterTemporals
    global counterQuadruples
    operator = operatorsStack.pop()
    if(operator== '>')or(operator == '<')or(operator == '>=')or(operator == '<=')or(operator == '!=')or(operator == '=='):
        operand2=operandsStack.pop()
        operand1=operandsStack.pop()

        type2=typesStack.pop()
        type1=typesStack.pop()
        typeResult = SemCube[semIndex1[type1]][semIndex2[type2]][semIndex3[operator]]

        if(typeResult==-1):
            raise TypeError("Type mismatch")

        else:
            temporalVariable = "Temporal%s" %counterTemporals
            if not ProcVars[moduleName][addrTable].has_key(temporalVariable):
                ProcVars[moduleName][typeTable][temporalVariable] = typeResult
                ProcVars[moduleName][addrTable][temporalVariable] = ES_base + S_offsetTable[typeResult] + ES_counterTable[typeResult]
                ES_counterTable[typeResult] += 1
            temporalAddress=ProcVars[moduleName][addrTable][temporalVariable]
            operandsStack.push(temporalAddress)
            typesStack.push(typeResult)
            Quadruples[counterQuadruples]=[operator, operand1, operand2, temporalAddress]
            counterTemporals+=1
            counterQuadruples+=1
    else:
        operatorsStack.push(operator)

def p_compareToken(p):
    '''compareToken : GREATER_THAN
                    | LESS_THAN
                    | LESS_EQUAL_THAN
                    | GREATER_EQUAL_THAN
                    | NOT_EQUAL_THAN
                    | SAME_AS'''
    operatorsStack.push(p[1])

def p_exp(p):
    'exp : term moreTerms'

def p_moreTerms(p):
    '''moreTerms : empty
                 | PLUS f_pushOperator term f_popTerm moreTerms
                 | MINUS f_pushOperator term f_popTerm moreTerms'''

def p_f_popTerm(p):
    'f_popTerm : '
    global counterTemporals
    global counterQuadruples
    operator = operatorsStack.pop()
    if(operator== '+')or(operator == '-'):
        operand2=operandsStack.pop()
        operand1=operandsStack.pop()

        type2=typesStack.pop()
        type1=typesStack.pop()
        typeResult = SemCube[semIndex1[type1]][semIndex2[type2]][semIndex3[operator]]

        if(typeResult==-1):
            raise TypeError("Type dismatch")

        else:
            temporalVariable = "Temporal%s" %counterTemporals
            if not ProcVars[moduleName][addrTable].has_key(temporalVariable):
                ProcVars[moduleName][typeTable][temporalVariable] = typeResult
                ProcVars[moduleName][addrTable][temporalVariable] = ES_base + S_offsetTable[typeResult] + ES_counterTable[typeResult]
                ES_counterTable[typeResult] += 1
            temporalAddress=ProcVars[moduleName][addrTable][temporalVariable]
            operandsStack.push(temporalAddress)
            typesStack.push(typeResult)
            Quadruples[counterQuadruples]=[operator, operand1, operand2, temporalAddress]
            counterTemporals+=1
            counterQuadruples+=1
    else:
        operatorsStack.push(operator)

def p_term(p):
    'term : factor moreFactors'

def p_moreFactors(p):
    '''moreFactors : empty
                   | DIVIDE f_pushOperator factor f_popFactor moreFactors
                   | TIMES f_pushOperator factor f_popFactor moreFactors
                   | MOD f_pushOperator factor f_popFactor moreFactors'''

def p_factor(p):
    '''factor : LPAREN f_pushOperator expression RPAREN f_popOperator 
              | cvar
              | funct'''

def p_f_pushOperator(p):
    'f_pushOperator : '
    if(not isCondition):
        operatorsStack.push(p[-1])

def p_f_popOperator(p):
    'f_popOperator : '
    global isCondition
    global counterQuadruples

    if(isCondition):
        isCondition = False
        operand = operandsStack.pop()
        typeVariable = typesStack.pop()
        if(typeVariable == 'bool'):
            #print typeOfCondition
            if (typeOfCondition == 'if' or typeOfCondition=='while'):
                Quadruples[counterQuadruples]=["GOTOF", operand, typeOfCondition, -1]
                branchStack.push(counterQuadruples)
                counterQuadruples+=1
            elif(typeOfCondition=='do'):
                code = branchStack.pop()
                Quadruples[counterQuadruples]=['GOTOT', operand, typeOfCondition, code]
                counterQuadruples+=1
            else:
                #print typeOfCondition
                raise TypeError("Not a valid condition")
        else:
            raise TypeError("Result of condition is not bool")
    else:
        operatorsStack.pop()

def p_f_popFactor(p):
    'f_popFactor : '
    global counterTemporals
    global counterQuadruples
    operator = operatorsStack.pop()
    if(operator== '*')or(operator == '/')or(operator=='%'):
        operand2=operandsStack.pop()
        operand1=operandsStack.pop()

        type2=typesStack.pop()
        type1=typesStack.pop()
        typeResult = SemCube[semIndex1[type1]][semIndex2[type2]][semIndex3[operator]]

        if(typeResult==-1):
            raise TypeError("Type dismatch")

        else:
            temporalVariable = "Temporal%s" %counterTemporals
            if not ProcVars[moduleName][addrTable].has_key(temporalVariable):
                ProcVars[moduleName][typeTable][temporalVariable] = typeResult
                ProcVars[moduleName][addrTable][temporalVariable] = ES_base + S_offsetTable[typeResult] + ES_counterTable[typeResult]
                ES_counterTable[typeResult] += 1
            temporalAddress=ProcVars[moduleName][addrTable][temporalVariable]
            operandsStack.push(temporalAddress)
            typesStack.push(typeResult)
            Quadruples[counterQuadruples]=[operator, operand1, operand2, temporalAddress]
            counterTemporals+=1
            counterQuadruples+=1
    else:
        operatorsStack.push(operator)
# def p_f_pushFF(p):
#     'f_pushFF : '
#     operandsStack.push(p[-1])

# def p_f_popFF(p):
#     'f_popFF : '
    #operandsStack.pop()

def p_cvar(p):
    '''cvar : ID f_isID
            | C_BOOL f_isConst
            | C_INT f_isConst
            | C_FLOAT f_isConst
            | C_STRING f_isConst'''

def p_f_isID(p):
    'f_isID : '
    if ProcVars[moduleName][addrTable].has_key(p[-1]):
        address = ProcVars[moduleName][addrTable][p[-1]]
        operandsStack.push(address)
        typesStack.push(ProcVars[moduleName][typeTable][p[-1]])
    elif ProcVars['Vispi'][addrTable].has_key(p[-1]):
        address = ProcVars['Vispi'][addrTable][p[-1]]
        operandsStack.push(address)
        typesStack.push(ProcVars['Vispi'][typeTable][p[-1]])
    else:
        raise TypeError("variable '%s' not declared" %(p[-1]))

def p_f_isConst(p):
    'f_isConst : '
    value = p[-1]
    constType = type(value)
    typeStr = ''
    if constType is int:
        typeStr = 'int'
    elif constType is float:
        typeStr = 'float'
    elif constType is str:
        if value == 'true' or value == 'false':
            typeStr = 'bool'
        else:
            typeStr = 'string'

    if not ProcVars['Vispi'][addrTable].has_key(value):
        ProcVars['Vispi'][typeTable][value] = typeStr
        ProcVars['Vispi'][addrTable][value] = CS_base + S_offsetTable[typeStr] + CS_counterTable[typeStr]
        CS_counterTable[typeStr] += 1

    operandsStack.push(ProcVars['Vispi'][addrTable][value])
    typesStack.push(ProcVars['Vispi'][typeTable][value])   


### Following code is Little Duck code ###

def p_error(p):
    if p:
        print("Syntax error at '%s'" %(p.value))
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()

def parse(data):
    parser.error = 0
    p = parser.parse(data, debug=1, tracking=True)
    if parser.error: return None
    return p

# while 1:
#     try:
#         s = raw_input('calc > ')
#     except EOFError:
#         break
#     if not s: continue
#     yacc.parse(s)line
