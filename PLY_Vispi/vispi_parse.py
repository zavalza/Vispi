from ply import *
from stack import Stack
import vispi_lex
tokens = vispi_lex.tokens

#Semantic cube
# order: type, type, operator
#   type order: <NULL>, bool, char, int, float, string, image, -1 means error
#       NULL operand is only valid on the first operand
#       -1 is only valid as a result
#   operator order: + - / * % > < <= >= != == && || ! 
semIndex1={'<NULL>':0, 'bool':1, 'char':2, 'int':3, 'float':4, 'string':5, 'image':6}
semIndex2={'bool':0, 'char':1, 'int':2, 'float':3, 'string':4, 'image':5}
semIndex3={'+':0,'-':1,'/':2,'*':3,'%':4,'>':5,'<':6, '<=':7, '>=':8, '!=':9, '==':10, '&&':11, '||':12, '!':13}
SemCube = [
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,'bool'],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
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
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['string',-1,-1,-1,-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['string',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['int','int','int','int','int','bool','bool','bool','bool','bool','bool',-1,-1,-1],
            ['float','float','float','float',-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['float','float','float','float',-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            ['float','float','float','float',-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['string','string','int',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], #string - char y string / char : a implementar
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['string',-1,-1,-1,-1,'bool','bool','bool','bool','bool','bool',-1,-1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        ],
        [
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,'image','image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            [-1,-1,'image','image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
            ['image','image',-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]   #comparaciones entre image?
        ]
    ]

#MACROS
paramList = 0
typeTable = 1
addrTable = 2

#Virtual Memory segment definitions
DS_base = 0                 #globales
DS_len = 1200
CS_base = DS_base + DS_len  #constantes
CS_len = 1200
SS_base = CS_base + CS_len  #locales
SS_len = 1200
ES_base = SS_base + SS_len  #temporales
ES_len = 1200

S_offsetTable = {'bool' : 0, 'char' : 200, 'int' : 400, 'float' : 600, 'string' : 800, 'image' : 1000}

#variable counters
DS_counterTable = {'bool' : 0, 'char' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0}
CS_counterTable = {'bool' : 0, 'char' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0}
SS_counterTable = {'bool' : 0, 'char' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0}
ES_counterTable = {'bool' : 0, 'char' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0}


#data structures
ProcTypes = {'Vispi':'prog'}
ProcSize = {'Vispi':0}
ProcAddr = {'Vispi':0}
        # parameter list, {variable types dict}, {variable address dict}
ProcVars = {'Vispi':[[],{},{}]}
ProcConst = {}

#variables
moduleName = 'Vispi'
typeOfData = 'VOID' #Used to store the last type detected

#quadruples
#fileQuadruples = open('quadruples.txt', 'w')
counterQuadruples = 0
Quadruples={}
branchStack = Stack()
operatorsStack = Stack()
operandsStack = Stack()
typesStack = Stack()
isCondition = False
#temporal variables
counterTemporals = 0
#constantes con contador para memoria

#Grammatic rules
def p_program(p):
    'program : programName hardware vars assign functions'
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
        print 'operatorsStack\n'
        print operatorsStack
        print 'operandsStack\n'
        print operandsStack
        print 'branchStack\n'
        print branchStack
    else:
        raise TypeError("'main' module was not defined")
def p_programName(p):
    'programName : PROGRAM ID NEWLINE'
    global counterQuadruples
    Quadruples[counterQuadruples]=["GOTO", -1, -1, -1]
    branchStack.push(counterQuadruples)
    counterQuadruples+=1

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
        Quadruples[counterQuadruples]=[p[1], operandsStack.pop(), -1, -1]
        counterQuadruples+=1

def p_ouputsDeclaration(p):
    '''outputsDeclaration : empty
					      | OUTPUT f_saveType pinList NEWLINE'''
    global counterQuadruples
    while(not operandsStack.isEmpty()):
        Quadruples[counterQuadruples]=[p[1], operandsStack.pop(), -1, -1]
        counterQuadruples+=1

def p_pwmDeclaration(p):
    '''pwmDeclaration : empty
				      | PWM f_saveType pinList NEWLINE'''
    global counterQuadruples
    while(not operandsStack.isEmpty()):
        Quadruples[counterQuadruples]=[p[1], operandsStack.pop(), -1, -1]
        counterQuadruples+=1

def p_pinList(p):
    '''pinList : C_INT COLON ID
               | C_INT COLON ID COMMA pinList'''
    ProcVars['Vispi'][typeTable][p[3]] = typeOfData
    ProcVars['Vispi'][addrTable][p[3]] = DS_base + S_offsetTable[typeOfData] + DS_counterTable[typeOfData]
    DS_counterTable[typeOfData] += 1 # falta validar que no nos pasemos del tamanio del segmento
    operandsStack.push(p[1])


def p_vars(p):
    '''vars : tipo idList NEWLINE vars
            | empty'''

#def p_isDeclaration(p):
#    'isDeclaration :'
#    global declaration
#    declaration = True

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
            | CHAR f_saveType
            | STRING f_saveType
            | IMAGE f_saveType'''

def p_functions(p):
    '''functions : DEF tipo ID f_saveModule LPAREN RPAREN COLON NEWLINE block functions
                 | DEF tipo ID f_saveModule LPAREN tipo ID f_addToParam parameterList RPAREN COLON NEWLINE block functions
                 | DEF VOID ID f_saveModule LPAREN RPAREN COLON NEWLINE block functions
                 | DEF VOID ID f_saveModule LPAREN tipo ID f_addToParam parameterList RPAREN COLON NEWLINE block functions
                 | DEF VOID MAIN f_saveModule LPAREN RPAREN COLON NEWLINE block functions
                 | DEF VOID MAIN f_saveModule LPAREN tipo ID f_addToParam parameterList RPAREN COLON NEWLINE block functions
                 | empty'''

def p_f_saveModule(p):
    'f_saveModule :'
    SS_counterTable = {'bool' : 0, 'char' : 0, 'int' : 0, 'float' : 0, 'string' : 0, 'image' : 0}
    global moduleName
    moduleName = p[-1]
    if ProcTypes.has_key(moduleName):
        raise TypeError("'%s' is already defined" %(moduleName))
    else:
        ProcTypes[moduleName] = p[-2]
        #ProcSize
        #ProcAddr
        ProcVars[moduleName] = [[],{},{}]

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
    '''assign : ID f_checkID EQUAL expression NEWLINE f_generateEqual assign
              | empty'''

def p_f_generateEqual(p):
    'f_generateEqual :'
    global counterQuadruples
    #Falta validar que sea una igualdad con tipos correctos
    #Sacar dos operandos y validarlos
    operand2 = operandsStack.pop()
    operand1 = operandsStack.pop()
    Quadruples[counterQuadruples]=['=', operand2, -1, operand1]
    counterQuadruples+=1

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
             | TAB newline_tab statement moreStatements'''

def p_moreStatements(p):
    '''moreStatements : empty
                      | TAB newline_tab statement moreStatements'''

def p_newline_tab(p):
    '''newline_tab : empty
                    | NEWLINE TAB newline_tab'''

def p_statement(p):
    '''statement : vars 
                 | assign
                 | condition
                 | cycle
                 | funct NEWLINE
                 | RETURN expression NEWLINE'''

def p_condition(p):
    '''condition : IF f_isCondition expression COLON NEWLINE block
                 | IF f_isCondition expression COLON NEWLINE block ELSE COLON NEWLINE block'''

def p_cycle(p):
    '''cycle : WHILE f_isCondition expression COLON NEWLINE block
             | DO COLON NEWLINE block WHILE f_isCondition expression NEWLINE'''

def p_f_isCondition(p):
    'f_isCondition : '
    global isCondition
    isCondition = True

def p_funct(p):
    '''funct : ID LPAREN RPAREN
             | ID LPAREN expression expressionList RPAREN'''

def p_expressionList(p):
    '''expressionList : empty
                      | COMMA expression expressionList'''

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
    if(isCondition):
        isCondition = False
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
            | C_CHAR f_isConst
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
